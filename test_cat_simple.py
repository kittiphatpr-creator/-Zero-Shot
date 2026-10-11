from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
img = Image.open('static/samples/cats_reconstructed.jpg')
model.set_classes(["cat"])
res = model.predict(img, conf=0.001, imgsz=960, verbose=True)[0]
print("Boxes with conf >= 0.001:", len(res.boxes))
for b in res.boxes:
    print(b.conf.item(), b.xyxy.tolist())
