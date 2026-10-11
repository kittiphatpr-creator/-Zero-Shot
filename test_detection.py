# -*- coding: utf-8 -*-
import sys
import io

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from PIL import Image
from detector import detector, parse_user_queries
import json

img = Image.open('static/samples/avengers.jpg')
queries = parse_user_queries('ธอร์, แบล็ควิโดว์, กัปตันอเมริกา, ไอรอนแมน')
print('Queries:', queries)
dets = detector.detect(img, queries, conf_thresh=0.20)
print('Detections on Avengers:')
for d in dets:
    print(f"  {d['label']} ({d['label_en']}) - Score: {d['score']*100:.1f}% (raw: {d['raw_score']}) - Box: {d['box']}")

# Test DC queries on batman_dc.jpg
print('\nTesting DC on batman_dc.jpg:')
img_bm = Image.open('static/samples/batman_dc.jpg')
queries_dc = parse_user_queries('แบทแมน, โจ๊กเกอร์')
dets_dc = detector.detect(img_bm, queries_dc, conf_thresh=0.20)
for d in dets_dc:
    print(f"  {d['label']} ({d['label_en']}) - Score: {d['score']*100:.1f}% (raw: {d['raw_score']}) - Box: {d['box']}")

# Test DC on dc_heroes.jpg
print('\nTesting DC on dc_heroes.jpg:')
img_dc = Image.open('static/samples/dc_heroes.jpg')
queries_dc_all = parse_user_queries('ซูเปอร์แมน, แบทแมน, วันเดอร์วูแมน, เดอะแฟลช, อะควาแมน, ไซบอร์ก')
dets_dc_all = detector.detect(img_dc, queries_dc_all, conf_thresh=0.20)
for d in dets_dc_all:
    print(f"  {d['label']} ({d['label_en']}) - Score: {d['score']*100:.1f}% (raw: {d['raw_score']}) - Box: {d['box']}")
