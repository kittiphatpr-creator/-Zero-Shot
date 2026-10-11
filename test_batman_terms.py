# -*- coding: utf-8 -*-
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
im_bm = Image.open('static/samples/batman_dc.jpg')

bat_terms = [
    "man in bat costume",
    "man in armor",
    "batman costume",
    "batman",
    "man in dark knight suit",
    "man in black armor with cape",
    "masked superhero",
    "man with pointed ears cowl",
    "dark knight",
    "black superhero cape"
]

model.set_classes(bat_terms)
res = model.predict(im_bm, conf=0.03, imgsz=960, verbose=False)[0]
print("Batman candidates:")
for b in res.boxes:
    cls_id = int(b.cls[0])
    conf = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    print(f"  {name:30s} | conf: {conf:.4f} | box: {box}")
