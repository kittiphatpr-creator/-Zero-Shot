# -*- coding: utf-8 -*-
from PIL import Image

img = Image.open('static/samples/avengers.jpg')
w, h = img.size
print(f"Image dimensions: {w}x{h}")

# In avengers.jpg:
# Tony Stark (Iron man) is at the top left/center:
# x: ~220 to ~530, y: ~60 to ~370. Let's check!
# Thor is top right: x: ~320 to ~560, y: ~160 to ~430.
# Captain America is center foreground: x: ~140 to ~530, y: ~380 to ~830.
# Black Widow is middle left: x: ~60 to ~270, y: ~340 to ~600.
# Hawkeye is bottom left: x: ~20 to ~270, y: ~580 to ~800.
# Thanos is top far left: x: ~0 to ~160, y: ~80 to ~380.
# Captain Marvel is middle right: x: ~380 to ~570, y: ~320 to ~600.
# Shield is bottom right: x: ~440 to ~576, y: ~540 to ~760.
