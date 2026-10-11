# -*- coding: utf-8 -*-
import urllib.request
import json

def test_api(sample_key, prompt, conf=0.25):
    url = "http://127.0.0.1:5000/api/detect"
    payload = {
        "sample_key": sample_key,
        "prompt": prompt,
        "conf_thresh": conf,
        "model_mode": "zero_shot"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"\nAPI Result for sample '{sample_key}' with prompt '{prompt}':")
        print(f"Status: {res.get('status')}, Found: {len(res.get('detections', []))} objects, Time: {res.get('time_ms')}ms")
        for d in res.get('detections', []):
            print(f"  -> {d['label']} ({d['label_en']}): {d['score']*100:.1f}% | Box: {d['box']}")

test_api("avengers", "ธอร์, แบล็ควิโดว์, กัปตันอเมริกา, ไอรอนแมน", 0.25)
test_api("batman", "แบทแมน", 0.25)
test_api("superman", "ซูเปอร์แมน", 0.25)
test_api("dc", "ซูเปอร์แมน, แบทแมน, วันเดอร์วูแมน", 0.25)
