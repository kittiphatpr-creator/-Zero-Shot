# -*- coding: utf-8 -*-
from PIL import Image
from detector import detector, parse_user_queries

img = Image.open('static/samples/cat_pet.jpg')
queries = parse_user_queries('แมว')
dets = detector.detect(img, queries, conf_thresh=0.25)
print('Detections on cat_pet.jpg:')
for d in dets:
    print(f"  {d['label']} ({d['label_en']}) - Score: {d['score']*100:.1f}% - Box: {d['box']}")
