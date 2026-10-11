# -*- coding: utf-8 -*-
import urllib.request
import os
from PIL import Image

headers = {'User-Agent': 'AntigravityHeroDownloader/1.0 (educational student bot; contact@antigravity.ai)'}

urls = {
    'batman': 'https://upload.wikimedia.org/wikipedia/commons/3/30/Batman_Cosplay_-_Dragon_Con_2012.jpg',
    'superman': 'https://upload.wikimedia.org/wikipedia/commons/1/15/Superman_cosplay_by_Greg_Carlson.jpg',
    'dc': 'https://upload.wikimedia.org/wikipedia/commons/8/8c/Dragon_Con_2013_-_Justice_League_(9664854502).jpg'
}

dest_map = {
    'batman': 'static/samples/batman_dc.jpg',
    'superman': 'static/samples/superman_dc.jpg',
    'dc': 'static/samples/dc_heroes.jpg'
}

for k, url in urls.items():
    dest = dest_map[k]
    print(f"Downloading {k} from {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(dest, 'wb') as out_f:
            out_f.write(resp.read())
        im = Image.open(dest)
        # Resize if huge
        if max(im.size) > 1200:
            ratio = 1200 / max(im.size)
            new_size = (int(im.size[0] * ratio), int(im.size[1] * ratio))
            im = im.resize(new_size, Image.Resampling.LANCZOS)
            im.save(dest, quality=92)
        print(f"  Success: {dest} ({im.size})")
    except Exception as e:
        print(f"  Error downloading {k}: {e}")
