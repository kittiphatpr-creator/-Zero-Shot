# -*- coding: utf-8 -*-
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from PIL import Image
from detector import detector

if not detector.is_loaded:
    detector.load_models()

def test_terms(img_path, term_list):
    print("=" * 60)
    print("Testing:", img_path)
    img = Image.open(img_path)
    print("Image size:", img.size)
    detector.yolo_world.set_classes(term_list)
    res = detector.yolo_world.predict(img, conf=0.02, imgsz=960, verbose=False)[0]
    print(f"Boxes found ({len(res.boxes)}):")
    for b in res.boxes[:20]:
        cls_id = int(b.cls[0])
        raw_c = float(b.conf[0])
        name = res.names[cls_id]
        box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
        print(f"  {name:30s} conf={raw_c:.4f} box={box}")

# Test batman_dc.jpg
test_terms('static/samples/batman_dc.jpg', [
    "batman", "bat cowl", "man in bat costume", "masked man", "black mask", "pointed ears mask", 
    "dark knight", "man in armor", "superhero with cape", "joker", "clown", "green hair"
])

# Test superman_dc.jpg
test_terms('static/samples/superman_dc.jpg', [
    "superman", "man in blue suit with red cape", "man with red cape", "flying superhero", 
    "man with s on chest", "clark kent", "superhero"
])

# Test dc_heroes.jpg
test_terms('static/samples/dc_heroes.jpg', [
    "superman", "batman", "wonder woman", "the flash", "aquaman", "cyborg",
    "man with red cape", "man with trident", "woman with sword", "man in red suit",
    "superhero", "person", "man", "woman"
])

# Test avengers.jpg for Tony Stark / Iron Man and others
test_terms('static/samples/avengers.jpg', [
    "man looking sideways", "man with goatee", "tony stark", "robert downey jr", "iron man",
    "man profile", "man looking up", "thor", "blonde man with beard", "chris hemsworth",
    "woman with red hair", "black widow", "scarlett johansson", "man with star on chest", "captain america"
])
