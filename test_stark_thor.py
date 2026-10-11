# -*- coding: utf-8 -*-
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
im = Image.open('static/samples/avengers.jpg')

stark_terms = [
    "man looking sideways", "man with goatee", "tony stark", "robert downey jr",
    "man looking to the right", "man with beard profile", "iron man", "brunette man"
]

thor_terms = [
    "man with beard", "blonde man with beard", "thor", "man in armor looking forward",
    "chris hemsworth", "man with short beard"
]

print("=== Tony Stark Candidates ===")
model.set_classes(stark_terms)
res = model.predict(im, conf=0.02, imgsz=960, verbose=False)[0]
for b in res.boxes:
    cls_id = int(b.cls[0])
    conf = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    if box[1] < 400 and box[0] < 380: # Stark region
        print(f"  STARK: {name:25s} | conf: {conf:.4f} | box: {box}")

print("\n=== Thor Candidates ===")
model.set_classes(thor_terms)
res = model.predict(im, conf=0.02, imgsz=960, verbose=False)[0]
for b in res.boxes:
    cls_id = int(b.cls[0])
    conf = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    if box[1] < 450 and box[0] >= 280: # Thor region
        print(f"  THOR:  {name:25s} | conf: {conf:.4f} | box: {box}")
