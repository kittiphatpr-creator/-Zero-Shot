# -*- coding: utf-8 -*-
from PIL import Image
from detector import detector, parse_user_queries

im_sm = Image.open('static/samples/superman_dc.jpg')
queries_sm = parse_user_queries('ซูเปอร์แมน')
dets_sm = detector.detect(im_sm, queries_sm, conf_thresh=0.25)
print("Superman on superman_dc.jpg:")
for d in dets_sm:
    print(f"  {d['label']} ({d['label_en']}) - Score: {d['score']*100:.1f}% - Box: {d['box']}")

im_dc = Image.open('static/samples/dc_heroes.jpg')
queries_dc = parse_user_queries('ซูเปอร์แมน, แบทแมน, วันเดอร์วูแมน')
dets_dc = detector.detect(im_dc, queries_dc, conf_thresh=0.25)
print("\nDC Group on dc_heroes.jpg:")
for d in dets_dc:
    print(f"  {d['label']} ({d['label_en']}) - Score: {d['score']*100:.1f}% - Box: {d['box']}")
