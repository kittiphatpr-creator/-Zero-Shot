# -*- coding: utf-8 -*-
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")

def test_image(path, classes):
    print("=" * 60)
    print("Testing:", path)
    im = Image.open(path)
    model.set_classes(classes)
    res = model.predict(im, conf=0.03, imgsz=960, verbose=False)[0]
    for b in res.boxes:
        cls_id = int(b.cls[0])
        conf = float(b.conf[0])
        name = res.names[cls_id]
        box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
        print(f"  {name:25s} | conf: {conf:.4f} | box: {box}")

test_image('static/samples/batman_dc.jpg', [
    "batman", "man in bat costume", "bat cowl", "man in armor", "man in black suit", "dark knight"
])

test_image('static/samples/superman_dc.jpg', [
    "superman", "man with red cape and s crest", "man with red cape", "man in blue suit", "superhero"
])

test_image('static/samples/dc_heroes.jpg', [
    "batman", "superman", "wonder woman", "martian manhunter", "blue beetle",
    "man in bat costume", "man with red cape and s crest", "woman with tiara",
    "superhero", "man in blue suit", "green man"
])
