from PIL import Image
from ultralytics import YOLO

# Crop the full canvas area from screenshot
screenshot = Image.open('C:/Users/acer/.gemini/antigravity/brain/d4fe97d1-7625-4652-a0b4-7d889f02b2c2/.user_uploaded/media_1791736647249.png').convert('RGB')
# Clean bounds of canvas image: x=581..820, y=51..473
clean_crop = screenshot.crop((581, 51, 820, 473))
# Resize to original 576 x 1024
orig = clean_crop.resize((576, 1024), Image.Resampling.LANCZOS)
orig.save('static/samples/cats_reconstructed.jpg')
print("Reconstructed image saved, size:", orig.size)

model = YOLO("yolov8s-worldv2.pt")

cat_prompts = [
    "cat",
    "white cat",
    "grey cat",
    "black cat",
    "striped cat",
    "cat sitting on wall",
    "cat from back",
    "cat back",
    "sitting cat",
    "kitten",
    "feline",
    "small animal",
    "pet",
    "cat tail"
]

model.set_classes(cat_prompts)
res = model.predict(orig, conf=0.01, imgsz=960, verbose=False)[0]

print(f"\nTotal detections with conf >= 0.01: {len(res.boxes)}")
for b in res.boxes:
    cls_id = int(b.cls[0])
    raw_c = float(b.conf[0])
    name = res.names[cls_id]
    box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
    print(f"  {name:25s} | conf: {raw_c:.4f} | box: {box}")
