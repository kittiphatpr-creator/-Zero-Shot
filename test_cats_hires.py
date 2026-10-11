from PIL import Image
from ultralytics import YOLO

# Upscale anime_cats to match original resolution (where Cat 4 width was 84px)
im = Image.open('static/samples/anime_cats.jpg')
orig_w = int(im.size[0] * 3.5)
orig_h = int(im.size[1] * 3.5)
im_hi = im.resize((orig_w, orig_h), Image.Resampling.LANCZOS)
im_hi.save('static/samples/anime_cats_hi.jpg')
print(f"Resized image: {orig_w}x{orig_h}")

model = YOLO("yolov8s-worldv2.pt")

prompts = [
    "cat",
    "white cat",
    "cat sitting",
    "sitting cat",
    "cat back",
    "cartoon cat",
    "cat from behind",
    "feline",
    "small cat",
    "pet cat"
]

model.set_classes(prompts)
res = model.predict(im_hi, conf=0.01, imgsz=960, verbose=False)[0]
print(f"Boxes found: {len(res.boxes)}")
for b in res.boxes:
    cls_id = int(b.cls[0])
    raw_c = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    print(f"  {name:20s} | conf: {raw_c:.4f} | box: {box}")
