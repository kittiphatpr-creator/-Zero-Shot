from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
crop = Image.open('static/samples/cat5_crop.jpg')
# Resize to a reasonable size for YOLO (e.g. 320x320)
crop_resized = crop.resize((320, 320), Image.Resampling.LANCZOS)

candidates = [
    "cat",
    "white cat",
    "sitting cat",
    "cat from behind",
    "cat back",
    "white feline",
    "small cat",
    "feline",
    "kitten",
    "animal"
]

model.set_classes(candidates)
res = model.predict(crop_resized, conf=0.005, verbose=False)[0]
print(f"Boxes found on Cat 5 crop: {len(res.boxes)}")
for b in res.boxes:
    cls_id = int(b.cls[0])
    raw_c = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    print(f"  {name:20s} | conf: {raw_c:.4f} | box: {box}")
