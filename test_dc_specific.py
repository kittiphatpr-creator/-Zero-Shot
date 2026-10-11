# -*- coding: utf-8 -*-
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
im_dc = Image.open('static/samples/dc_heroes.jpg')

terms = [
    "man with s logo on chest", "man with red s crest", "superman",
    "woman with tiara", "wonder woman", "diana prince",
    "man in dark knight suit", "man with pointed ears cowl and cape", "batman",
    "blue beetle", "martian manhunter"
]

model.set_classes(terms)
res = model.predict(im_dc, conf=0.03, imgsz=960, verbose=False)[0]
print("DC Group with specific terms:")
for b in res.boxes:
    cls_id = int(b.cls[0])
    conf = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    print(f"  {name:30s} | conf: {conf:.4f} | box: {box}")
