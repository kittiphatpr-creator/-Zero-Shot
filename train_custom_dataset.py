"""
Auto-Labeling and Fine-Tuning Pipeline for YOLO-World / YOLOv8
Allows training custom AI models for any domain (Food, Industry, Retail, Vehicles, Fashion, etc.)
"""

import os
import sys
import shutil
import argparse
import threading
from pathlib import Path
from PIL import Image

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Global training status for web API monitoring
TRAINING_STATE = {
    "status": "idle",       # idle | labeling | training | finished | error
    "progress": 0,          # 0 - 100
    "current_step": "",
    "logs": [],
    "error_message": "",
    "best_weights": ""
}

def log_event(message: str):
    print(message)
    TRAINING_STATE["logs"].append(message)
    # Keep last 50 lines
    if len(TRAINING_STATE["logs"]) > 50:
        TRAINING_STATE["logs"] = TRAINING_STATE["logs"][-50:]

def setup_dataset_structure(dataset_dir="custom_training_data"):
    """Sets up standard YOLO dataset directory hierarchy."""
    for split in ["train", "val"]:
        os.makedirs(f"{dataset_dir}/images/{split}", exist_ok=True)
        os.makedirs(f"{dataset_dir}/labels/{split}", exist_ok=True)
    log_event(f"📁 Dataset directory structure initialized at '{dataset_dir}/'")

def auto_label_images(source_dir, dataset_dir, class_names, conf_thresh=0.12):
    """
    Uses Zero-Shot Open-Vocabulary AI to automatically pseudo-label raw images.
    Saves bounding boxes in standard YOLO format: <class_id> <x_center> <y_center> <width> <height>
    """
    from ultralytics import YOLO
    from thai_knowledge_base import analyze_and_expand_thai_query

    log_event("=" * 60)
    log_event("🚀 [Step 1/3] Auto-Labeling Raw Images using Zero-Shot AI...")
    log_event("=" * 60)

    model = YOLO("yolov8s-worldv2.pt")
    
    # Expand classes
    class_map = {} # english candidate -> class_id
    expanded_classes = []
    for cid, cname in enumerate(class_names):
        candidates = analyze_and_expand_thai_query(cname)
        for cand in candidates:
            cand_l = cand.lower().strip()
            if cand_l not in expanded_classes:
                expanded_classes.append(cand_l)
            class_map[cand_l] = cid

    model.set_classes(expanded_classes)

    source_path = Path(source_dir)
    image_files = list(source_path.glob("*.jpg")) + list(source_path.glob("*.png")) + list(source_path.glob("*.jpeg"))
    log_event(f"Found {len(image_files)} image(s) to auto-annotate.")

    if not image_files:
        log_event(f"⚠️ No images found in {source_dir}. Please place .jpg/.png images in {source_dir}.")
        return 0

    labeled_count = 0
    total_imgs = len(image_files)

    for idx, img_p in enumerate(image_files):
        split = "val" if idx % 5 == 0 else "train"
        target_img = f"{dataset_dir}/images/{split}/{img_p.name}"
        target_txt = f"{dataset_dir}/labels/{split}/{img_p.stem}.txt"

        # Copy image
        shutil.copy(img_p, target_img)

        # Predict with high-resolution 800px
        results = model.predict(str(img_p), conf=conf_thresh, imgsz=800, verbose=False)
        lines = []

        if results and len(results) > 0:
            res = results[0]
            w, h = res.orig_shape[1], res.orig_shape[0]

            for box in res.boxes:
                cls_name = res.names[int(box.cls[0])].lower()
                target_cid = class_map.get(cls_name, 0)
                xywh = box.xywh[0].cpu().numpy()
                xc = xywh[0] / w
                yc = xywh[1] / h
                bw = xywh[2] / w
                bh = xywh[3] / h
                lines.append(f"{target_cid} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}")

        with open(target_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        labeled_count += 1
        pct = int(10 + (idx + 1) / total_imgs * 30)
        TRAINING_STATE["progress"] = pct
        log_event(f"  [{idx+1}/{total_imgs}] Auto-annotated {img_p.name} ({len(lines)} objects) -> {split}")

    return labeled_count

def generate_yaml(dataset_dir, class_names):
    """Generates dataset.yaml for Ultralytics YOLO training."""
    abs_dir = os.path.abspath(dataset_dir).replace("\\", "/")
    names_dict = {i: name for i, name in enumerate(class_names)}

    yaml_content = f"""# Ultralytics Custom Dataset Configuration
path: {abs_dir}
train: images/train
val: images/val

names:
"""
    for i, name in names_dict.items():
        yaml_content += f"  {i}: {name}\n"

    yaml_path = f"{dataset_dir}/dataset.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    log_event(f"📄 [Step 2/3] Created dataset configuration at: {yaml_path}")
    return yaml_path

def start_training(yaml_path, epochs=5, imgsz=320, base_model="yolov8n.pt"):
    """Launches model fine-tuning with PyTorch."""
    from ultralytics import YOLO
    import torch

    device = "0" if torch.cuda.is_available() else "cpu"
    log_event("=" * 60)
    log_event(f"🔥 [Step 3/3] Starting AI Model Training...")
    log_event(f"⚙️ Hardware: {'GPU (CUDA)' if device == '0' else 'CPU'}")
    log_event(f"📊 Epochs: {epochs} | Image Resolution: {imgsz}x{imgsz} | Base: {base_model}")
    log_event("=" * 60)

    model = YOLO(base_model)
    results = model.train(
        data=yaml_path,
        epochs=epochs,
        imgsz=imgsz,
        batch=2 if device == "cpu" else 8,
        device=device,
        workers=0,
        verbose=False
    )

    best_path = os.path.join(results.save_dir, "weights", "best.pt")
    log_event("=" * 60)
    log_event("✅ Training Complete!")
    log_event(f"🏆 Best model weights saved at: {best_path}")
    log_event("=" * 60)
    return best_path


def run_full_pipeline_thread(source_dir, class_names, epochs=3):
    """Runs the complete auto-labeling and training pipeline in a background thread."""
    global TRAINING_STATE
    try:
        TRAINING_STATE["status"] = "labeling"
        TRAINING_STATE["progress"] = 5
        TRAINING_STATE["current_step"] = "กำลังสร้างโครงสร้างชุดข้อมูลและตีกรอบรูปภาพอัตโนมัติ..."
        TRAINING_STATE["logs"] = []

        dataset_dir = "custom_training_data"
        setup_dataset_structure(dataset_dir)

        count = auto_label_images(source_dir, dataset_dir, class_names)
        if count == 0:
            TRAINING_STATE["status"] = "error"
            TRAINING_STATE["error_message"] = "ไม่พบไฟล์รูปภาพในโฟลเดอร์"
            return

        TRAINING_STATE["progress"] = 45
        TRAINING_STATE["current_step"] = "กำลังสร้างไฟล์ dataset.yaml..."
        yaml_file = generate_yaml(dataset_dir, class_names)

        TRAINING_STATE["status"] = "training"
        TRAINING_STATE["progress"] = 50
        TRAINING_STATE["current_step"] = f"กำลัง Fine-Tuning โมเดล PyTorch ({epochs} Epochs)..."

        best_weights = start_training(yaml_file, epochs=epochs, imgsz=320)
        TRAINING_STATE["progress"] = 100
        TRAINING_STATE["status"] = "finished"
        TRAINING_STATE["current_step"] = "การเทรนเสร็จสมบูรณ์ พร้อมใช้งานแล้ว!"
        TRAINING_STATE["best_weights"] = best_weights

        # Notify detector to reload
        from detector import detector
        detector.reload_custom_model()

    except Exception as e:
        TRAINING_STATE["status"] = "error"
        TRAINING_STATE["error_message"] = str(e)
        log_event(f"❌ Error during training: {e}")


def launch_training_job(source_dir="static/samples", classes_list=None, epochs=3):
    """Starts training thread if not already running."""
    if classes_list is None:
        classes_list = ["ไข่ดาว", "ข้าว", "แล็ปท็อป", "สุนัข", "คน", "รถยนต์"]
    if TRAINING_STATE["status"] in ["labeling", "training"]:
        return False, "Training is already in progress."

    t = threading.Thread(target=run_full_pipeline_thread, args=(source_dir, classes_list, epochs), daemon=True)
    t.start()
    return True, "Training started successfully."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-Label & Train Custom AI Model")
    parser.add_argument("--images", default="static/samples", help="Directory containing raw images to train on")
    parser.add_argument("--classes", default="ไข่ดาว, ข้าว, แล็ปท็อป, สุนัข, คน, รถยนต์", help="Comma-separated class names")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    args = parser.parse_args()

    classes = [c.strip() for c in args.classes.split(",") if c.strip()]
    dataset_dir = "custom_training_data"

    setup_dataset_structure(dataset_dir)
    auto_label_images(args.images, dataset_dir, classes)
    yaml_file = generate_yaml(dataset_dir, classes)
    
    print("\nStarting model training...")
    start_training(yaml_file, epochs=args.epochs)
