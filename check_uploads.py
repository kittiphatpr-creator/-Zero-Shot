import os
from pathlib import Path
from PIL import Image

upload_dir = Path("C:/Users/acer/.gemini/antigravity/brain/d4fe97d1-7625-4652-a0b4-7d889f02b2c2/.user_uploaded")
for f in upload_dir.glob("*"):
    try:
        im = Image.open(f)
        print(f"{f.name}: {im.size}, format={im.format}")
    except Exception as e:
        print(f"{f.name}: error {e}")
