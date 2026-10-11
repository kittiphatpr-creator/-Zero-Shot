from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8s-worldv2.pt")
im = Image.open("static/samples/thai_food.jpg")
model.set_classes(["fried egg", "rice", "plate"])

try:
    res = model.predict(im, conf=0.05, augment=True, verbose=False)[0]
    print("augment=True SUCCESS, boxes found:", len(res.boxes))
except Exception as e:
    print("augment=True error:", e)
