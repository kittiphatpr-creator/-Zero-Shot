# -*- coding: utf-8 -*-
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
im_dc = Image.open('static/samples/dc_heroes.jpg')

bat_candidates = [
    "man with pointed ears cowl and cape",
    "man in dark knight suit",
    "man in grey suit with bat logo",
    "batman in grey suit and black cape",
    "man wearing bat costume",
    "batman costume",
    "man in black cape and cowl",
    "superhero with black cape",
    "batman"
]

model.set_classes(bat_candidates)
res = model.predict(im_dc, conf=0.02, imgsz=960, verbose=False)[0]
print("Batman in group photo:")
for b in res.boxes:
    cls_id = int(b.cls[0])
    conf = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    if 550 <= box[0] <= 620 or 550 <= box[2] <= 720:
        print(f"  FOUND BATMAN: {name:35s} | conf: {conf:.4f} | box: {box}")
    else:
        print(f"  Other:        {name:35s} | conf: {conf:.4f} | box: {box}")
