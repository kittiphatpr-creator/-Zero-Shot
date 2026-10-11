from PIL import Image

screenshot = Image.open('C:/Users/acer/.gemini/antigravity/brain/d4fe97d1-7625-4652-a0b4-7d889f02b2c2/.user_uploaded/media_1791736647249.png').convert('RGB')
# In screenshot, the image displayed in canvas:
# Width is from ~580 to ~820
# Cat 4 box was [x: 385, y: 944, w: 84, h: 152] in orig image
# In the screenshot, Cat 5 is to the right of Cat 4.
# Let's crop x: 720..810, y: 350..470 in screenshot!
cat5_crop = screenshot.crop((730, 350, 790, 460))
cat5_crop.save('static/samples/cat5_crop.jpg')
print("Saved cat5_crop.jpg:", cat5_crop.size)
