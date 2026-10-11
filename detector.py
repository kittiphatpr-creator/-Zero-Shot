import os
import re
import numpy as np
from PIL import Image
from thai_knowledge_base import analyze_and_expand_thai_query, COLOR_MAP

CLASS_COLORS = [
    "#ef4444", "#3b82f6", "#10b981", "#f59e0b",
    "#8b5cf6", "#ec4899", "#06b6d4", "#84cc16",
    "#f97316", "#6366f1", "#14b8a6", "#e11d48",
    "#0284c7", "#d97706", "#7c3aed", "#059669"
]

def calibrate_confidence(raw_conf: float) -> float:
    """
    Calibrates raw open-vocabulary cosine similarity scores into intuitive probability percentages.
    In open-vocabulary zero-shot models, true positives often range from 0.018 - 0.35.
    This maps them cleanly into 25% - 98% range so standard sliders (e.g. 20% - 40%) detect accurately.
    """
    if raw_conf <= 0.018:
        return max(0.10, round(raw_conf * 5.5, 3))
    elif raw_conf <= 0.15:
        val = 0.25 + (raw_conf - 0.018) / (0.15 - 0.018) * (0.75 - 0.25)
        return round(val, 3)
    elif raw_conf <= 0.35:
        val = 0.75 + (raw_conf - 0.15) / (0.35 - 0.15) * (0.92 - 0.75)
        return round(val, 3)
    else:
        val = min(0.99, 0.92 + (raw_conf - 0.35) * 0.12)
        return round(val, 3)

def parse_user_queries(prompt_text: str) -> list:
    """
    Intelligently splits user input into clean object query terms.
    Handles commas, semicolons, newlines, Thai conjunctions (และ, กับ), and spaces.
    """
    text = prompt_text.strip()
    if not text:
        return ["object"]

    # Replace common delimiters
    for sep in [",", "،", ";", "\n", "\r", "\t", " และ ", " กับ ", " หรือ "]:
        text = text.replace(sep, ",")

    raw_items = [p.strip() for p in text.split(",") if p.strip()]
    final_queries = []

    for item in raw_items:
        if " " in item:
            has_color = any(c in item for c in COLOR_MAP.keys()) or any(c in item.lower() for c in ["red", "blue", "green", "yellow", "black", "white"])
            if not has_color and any(ord(ch) > 128 for ch in item):
                sub_parts = [s.strip() for s in item.split(" ") if s.strip()]
                final_queries.extend(sub_parts)
                continue
        final_queries.append(item)

    seen = set()
    cleaned = []
    for q in final_queries:
        if q and q not in seen:
            seen.add(q)
            cleaned.append(q)

    return cleaned if cleaned else ["object"]


class HighAccuracyZeroShotDetector:
    def __init__(self):
        self.yolo_world = None
        self.custom_model = None
        self.is_loaded = False
        self.custom_weights_path = "runs/detect/train/weights/best.pt"
        print("HighAccuracyZeroShotDetector initialized.")

    def load_models(self):
        """Loads YOLO-World v2 and optionally custom fine-tuned model if available."""
        try:
            from ultralytics import YOLO
            world_weights = "yolov8s-worldv2.pt"
            print(f"Loading SOTA YOLO-World model ({world_weights})...")
            self.yolo_world = YOLO(world_weights)
            self.is_loaded = True
            print("YOLO-World loaded successfully!")

            # Check if custom fine-tuned weights exist
            if os.path.exists(self.custom_weights_path):
                try:
                    print(f"Loading custom fine-tuned model ({self.custom_weights_path})...")
                    self.custom_model = YOLO(self.custom_weights_path)
                    print("Custom fine-tuned model loaded successfully!")
                except Exception as ex:
                    print(f"Could not load custom model: {ex}")

            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False

    def reload_custom_model(self):
        """Reloads custom model after a new training run."""
        if os.path.exists(self.custom_weights_path):
            try:
                from ultralytics import YOLO
                self.custom_model = YOLO(self.custom_weights_path)
                print(f"Custom model reloaded from {self.custom_weights_path}")
                return True
            except Exception as e:
                print(f"Failed to reload custom model: {e}")
                return False
        return False

    def detect(self, image: Image.Image, raw_queries: list, conf_thresh: float = 0.25, iou_thresh: float = 0.45, model_mode: str = "zero_shot"):
        """
        Runs accurate Object Detection.
        Supports:
        - model_mode="zero_shot": YOLO-World v2 with calibrated multi-domain confidence
        - model_mode="custom": Custom fine-tuned YOLO model
        """
        if not self.is_loaded:
            self.load_models()

        if model_mode == "custom" and self.custom_model is not None:
            return self._detect_custom(image, raw_queries, conf_thresh, iou_thresh)
        else:
            return self._detect_zero_shot(image, raw_queries, conf_thresh, iou_thresh)

    def _detect_zero_shot(self, image: Image.Image, raw_queries: list, conf_thresh: float, iou_thresh: float):
        """Zero-shot open-vocabulary detection using YOLO-World with calibrated confidence."""
        all_english_classes = []
        term_to_user_label = {}

        for raw_q in raw_queries:
            clean_q = raw_q.strip()
            if not clean_q:
                continue
            candidates = analyze_and_expand_thai_query(clean_q)
            for cand in candidates:
                cand_lower = cand.lower().strip()
                if cand_lower not in all_english_classes:
                    all_english_classes.append(cand_lower)
                term_to_user_label[cand_lower] = clean_q

        if not all_english_classes:
            all_english_classes = ["object"]
            term_to_user_label["object"] = "object"

        try:
            self.yolo_world.set_classes(all_english_classes)
            # Use raw threshold of 0.018 and 1024px resolution for maximum fine-grained detection
            results = self.yolo_world.predict(image, conf=0.018, iou=iou_thresh, imgsz=1024, max_det=300, verbose=False)

            raw_detections = []
            if results and len(results) > 0:
                res = results[0]
                for box_obj in res.boxes:
                    cls_id = int(box_obj.cls[0])
                    raw_conf = float(box_obj.conf[0])
                    calibrated_score = calibrate_confidence(raw_conf)
                    coords = box_obj.xyxy[0].cpu().numpy().tolist()
                    en_term = res.names[cls_id].lower()
                    user_label = term_to_user_label.get(en_term, en_term)

                    raw_detections.append({
                        "label": user_label,
                        "label_en": en_term,
                        "box": [round(c) for c in coords],
                        "score": calibrated_score,
                        "raw_score": round(raw_conf, 3),
                        "color": CLASS_COLORS[abs(hash(user_label)) % len(CLASS_COLORS)]
                    })

            # Non-Maximum Suppression (both same-class and cross-class collision)
            final_detections = []
            for det in sorted(raw_detections, key=lambda x: -x["score"]):
                if det["score"] < conf_thresh:
                    continue

                is_duplicate = False
                for existing in final_detections:
                    iou = calculate_iou(det["box"], existing["box"])
                    # Same label with moderate overlap -> duplicate
                    if existing["label"] == det["label"] and iou > 0.35:
                        is_duplicate = True
                        break
                    # Different label with very high overlap -> suppressed by higher score hero
                    if existing["label"] != det["label"] and iou > 0.65:
                        is_duplicate = True
                        break

                if not is_duplicate:
                    final_detections.append(det)

            return final_detections

        except Exception as e:
            print(f"Zero-shot detection error: {e}")
            return []

    def _detect_custom(self, image: Image.Image, filter_queries: list, conf_thresh: float, iou_thresh: float):
        """Detection using custom trained weights."""
        try:
            results = self.custom_model.predict(image, conf=conf_thresh, iou=iou_thresh, imgsz=640, verbose=False)
            detections = []
            if results and len(results) > 0:
                res = results[0]
                filter_set = set(q.strip().lower() for q in filter_queries if q.strip())
                for box_obj in res.boxes:
                    cls_id = int(box_obj.cls[0])
                    conf = float(box_obj.conf[0])
                    coords = box_obj.xyxy[0].cpu().numpy().tolist()
                    cls_name = res.names[cls_id]

                    if filter_set and cls_name.lower() not in filter_set:
                        if not any(f in cls_name.lower() or cls_name.lower() in f for f in filter_set):
                            continue

                    detections.append({
                        "label": cls_name,
                        "label_en": cls_name,
                        "box": [round(c) for c in coords],
                        "score": round(conf, 3),
                        "color": CLASS_COLORS[abs(hash(cls_name)) % len(CLASS_COLORS)],
                        "source": "custom_trained"
                    })
            return detections
        except Exception as e:
            print(f"Custom detection error: {e}")
            return []


def calculate_iou(boxA, boxB):
    """Computes Intersection over Union between two [x1, y1, x2, y2] boxes."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    denom = float(boxAArea + boxBArea - interArea)
    return interArea / denom if denom > 0 else 0


detector = HighAccuracyZeroShotDetector()
