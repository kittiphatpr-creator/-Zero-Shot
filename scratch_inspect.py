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
from thai_knowledge_base import analyze_and_expand_thai_query

def inspect_image(img_path, query_list):
    print("=" * 60)
    print("Inspecting:", img_path)
    img = Image.open(img_path)
    all_classes = []
    term_map = {}
    for q in query_list:
        cands = analyze_and_expand_thai_query(q)
        print(f"  Query: '{q}' -> cands: {cands}")
        for c in cands:
            cl = c.lower().strip()
            if cl not in all_classes:
                all_classes.append(cl)
            term_map[cl] = q
    
    detector.yolo_world.set_classes(all_classes)
    res = detector.yolo_world.predict(img, conf=0.03, imgsz=960, max_det=100, verbose=False)[0]
    print(f"Total raw boxes with conf >= 0.03: {len(res.boxes)}")
    for i, b in enumerate(res.boxes[:15]):
        cls_id = int(b.cls[0])
        raw_c = float(b.conf[0])
        name = res.names[cls_id]
        box = [round(x) for x in b.xyxy[0].cpu().numpy().tolist()]
        print(f"  Box {i+1}: {name} (User: {term_map.get(name, name)}) - raw conf: {raw_c:.4f} - box: {box}")

if not detector.is_loaded:
    detector.load_models()

inspect_image('static/samples/avengers.jpg', ['ธอร์', 'แบล็ควิโดว์', 'กัปตันอเมริกา', 'ไอรอนแมน'])
inspect_image('static/samples/batman_dc.jpg', ['แบทแมน', 'โจ๊กเกอร์'])
inspect_image('static/samples/dc_heroes.jpg', ['ซูเปอร์แมน', 'แบทแมน', 'วันเดอร์วูแมน', 'เดอะแฟลช', 'อะควาแมน', 'ไซบอร์ก'])
