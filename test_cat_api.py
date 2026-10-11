import urllib.request, json
req = urllib.request.Request('http://127.0.0.1:5000/api/detect', 
    data=json.dumps({'sample_key': 'cat', 'prompt': 'แมว', 'conf_thresh': 0.25}).encode('utf-8'),
    headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as r:
    res = json.loads(r.read().decode('utf-8'))
    print('API Cat Test:', len(res['detections']), 'found.')
    for d in res['detections']:
        print(f"  -> {d['label']}: {d['score']*100:.1f}%")
