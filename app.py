import os
import sys
import io
import time
import base64

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from detector import detector, parse_user_queries
from train_custom_dataset import TRAINING_STATE, launch_training_job

app = Flask(__name__, static_folder="static")

# Preload models on startup so first detection is fast
try:
    detector.load_models()
except Exception as e:
    print(f"Deferred load: {e}")

SAMPLE_MAP = {
    "food": "static/samples/thai_food.jpg",
    "salmon": "static/samples/salmon_dish.jpg",
    "spongebob": "static/samples/spongebob.jpg",
    "avengers": "static/samples/avengers.jpg",
    "cartoon": "static/samples/cartoon_stack.jpg",
    "batman": "static/samples/batman_dc.jpg",
    "superman": "static/samples/superman_dc.jpg",
    "dc": "static/samples/dc_heroes.jpg",
    "street": "static/samples/street_person.jpg",
    "fashion": "static/samples/fashion.jpg",
    "workspace": "static/samples/workspace.jpg",
    "dog": "static/samples/dog_park.jpg",
    "cat": "static/samples/cat_pet.jpg",
    "traffic": "static/samples/traffic.jpg"
}

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.route("/api/status", methods=["GET"])
def get_status():
    import torch
    return jsonify({
        "status": "online",
        "cuda_available": torch.cuda.is_available(),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "zero_shot_loaded": detector.is_loaded,
        "custom_model_loaded": detector.custom_model is not None,
        "has_custom_weights": os.path.exists("runs/detect/train/weights/best.pt")
    })

@app.route("/api/models", methods=["GET"])
def get_models():
    has_custom = os.path.exists("runs/detect/train/weights/best.pt")
    return jsonify({
        "models": [
            {
                "id": "zero_shot",
                "name": "⚡ Zero-Shot YOLO-World v2 (Open-Vocabulary)",
                "description": "ค้นหาวัตถุใหม่ได้ทุกชนิดในโลกตามคำสั่ง ไม่ต้องเทรนล่วงหน้า",
                "active": True
            },
            {
                "id": "custom",
                "name": "🏆 Custom Trained Model (Fine-Tuned)",
                "description": "โมเดลที่ผ่านการเทรนเฉพาะทาง แม่นยำเป็นพิเศษสำหรับชุดข้อมูล",
                "available": has_custom,
                "weights": "runs/detect/train/weights/best.pt" if has_custom else None
            }
        ]
    })

@app.route("/api/detect", methods=["POST"])
def detect_objects():
    data = request.get_json() or {}
    image_src = data.get("image_src", "")
    prompt = data.get("prompt", "person, car, dog")
    conf_thresh = float(data.get("conf_thresh", 0.25))
    sample_key = data.get("sample_key", "food")
    model_mode = data.get("model_mode", "zero_shot")

    # Smart parse prompt (handles commas, spaces between Thai words, conjunctions)
    queries = parse_user_queries(prompt)

    t0 = time.time()
    image = None

    try:
        # 1. Custom uploaded image (base64)
        if image_src.startswith("data:image"):
            header, encoded = image_src.split(",", 1)
            img_bytes = base64.b64decode(encoded)
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        # 2. Sample preset by key
        elif sample_key in SAMPLE_MAP and os.path.exists(SAMPLE_MAP[sample_key]):
            image = Image.open(SAMPLE_MAP[sample_key]).convert("RGB")
        # 3. Static path
        elif image_src.startswith("/static/"):
            local_path = image_src.lstrip("/")
            if os.path.exists(local_path):
                image = Image.open(local_path).convert("RGB")
    except Exception as e:
        print(f"Error reading image: {e}")

    # Fallback sample image if not loaded
    if image is None:
        sample_path = SAMPLE_MAP.get(sample_key, "static/samples/thai_food.jpg")
        if os.path.exists(sample_path):
            image = Image.open(sample_path).convert("RGB")
        else:
            image = Image.new("RGB", (800, 600), color=(120, 120, 120))

    detections = detector.detect(image, queries, conf_thresh=conf_thresh, model_mode=model_mode)
    latency_ms = round((time.time() - t0) * 1000)

    return jsonify({
        "status": "success",
        "detections": detections,
        "latency_ms": latency_ms,
        "count": len(detections),
        "queries_searched": queries,
        "model_used": model_mode
    })

@app.route("/api/train/start", methods=["POST"])
def start_train():
    data = request.get_json() or {}
    source_dir = data.get("source_dir", "static/samples")
    classes_str = data.get("classes", "ไข่ดาว, ข้าว, แล็ปท็อป, สุนัข, คน, รถยนต์")
    epochs = int(data.get("epochs", 3))

    classes_list = [c.strip() for c in classes_str.split(",") if c.strip()]
    success, msg = launch_training_job(source_dir, classes_list, epochs)
    return jsonify({"success": success, "message": msg})

@app.route("/api/train/status", methods=["GET"])
def get_train_status():
    return jsonify(TRAINING_STATE)

def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    local_ip = get_local_ip()
    print(f"\n=======================================================")
    print(f"🚀 High-Accuracy Zero-Shot & Training Studio Running 24/7!")
    print(f"👉 Local Access:   http://localhost:{port}")
    print(f"👉 Network/Mobile: http://{local_ip}:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
