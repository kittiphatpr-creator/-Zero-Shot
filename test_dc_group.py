# -*- coding: utf-8 -*-
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
im_dc = Image.open('static/samples/dc_heroes.jpg')

dc_terms = [
    # Batman
    "man in dark knight suit", "man in black armor with cape", "batman",
    # Superman
    "man with red cape and s crest", "superman",
    # Wonder Woman
    "woman in wonder woman costume", "woman with tiara and armor", "wonder woman", "woman with tiara",
    # Flash
    "man in red speedster suit", "the flash",
    # Martian Manhunter
    "martian manhunter", "green skinned superhero",
    # Blue Beetle
    "blue beetle", "man in blue superhero suit",
    # Joker
    "joker", "clown with green hair"
]

model.set_classes(dc_terms)
res = model.predict(im_dc, conf=0.03, imgsz=960, verbose=False)[0]
print("DC Heroes in group photo:")
for b in res.boxes:
    cls_id = int(b.cls[0])
    conf = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    print(f"  {name:30s} | conf: {conf:.4f} | box: {box}")
