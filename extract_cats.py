from PIL import Image

screenshot = Image.open('C:/Users/acer/.gemini/antigravity/brain/d4fe97d1-7625-4652-a0b4-7d889f02b2c2/.user_uploaded/media_1791736647249.png').convert('RGB')
# In screenshot (1024 x 675):
# Left edge of image is around x=580, right edge is around x=820
# Top is around y=50, bottom is around y=475
crop = screenshot.crop((580, 50, 820, 475))
crop.save('static/samples/anime_cats.jpg')
print("Saved crop:", crop.size)
