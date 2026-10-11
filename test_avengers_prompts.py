# -*- coding: utf-8 -*-
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
img = Image.open("static/samples/avengers.jpg")

prompts = [
    "captain america",
    "man with star on chest",
    "iron man",
    "tony stark",
    "man with goatee",
    "man looking sideways",
    "thor",
    "man with beard",
    "blonde man with beard",
    "black widow",
    "woman with red hair",
    "woman with braided hair",
    "hawkeye",
    "man with bow and arrow",
    "captain marvel",
    "shield"
]

model.set_classes(prompts)
results = model.predict(img, conf=0.02, imgsz=960, verbose=False)[0]

print("Predictions with conf >= 0.02:")
for b in results.boxes:
    cls_id = int(b.cls[0])
    raw_c = float(b.conf[0])
    name = results.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    print(f"  {name:25s} | conf: {raw_c:.4f} | box: {box}")
