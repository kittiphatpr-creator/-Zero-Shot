from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
img = Image.open('static/samples/anime_cats.jpg')
w, h = img.size
print(f"Image dimensions: {w}x{h}")

terms = ["cat", "kitten", "feline", "white cat", "sitting cat", "cartoon cat", "anime cat", "cat from behind", "cat back"]
model.set_classes(terms)

res = model.predict(img, conf=0.01, imgsz=960, verbose=False)[0]
print(f"Total raw boxes found with conf >= 0.01: {len(res.boxes)}")
for b in res.boxes:
    cls_id = int(b.cls[0])
    raw_c = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    print(f"  {name:20s} | conf: {raw_c:.4f} | box: {box}")
