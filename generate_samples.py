import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("static/samples", exist_ok=True)

def create_street_scene():
    img = Image.new("RGB", (800, 600), color=(140, 180, 210))
    draw = ImageDraw.Draw(img)
    # Sky and ground
    draw.rectangle([(0, 380), (800, 600)], fill=(75, 80, 85))  # Asphalt street
    draw.rectangle([(0, 340), (800, 380)], fill=(170, 175, 175)) # Sidewalk
    # Buildings in background
    draw.rectangle([(40, 120), (220, 340)], fill=(120, 110, 130))
    draw.rectangle([(250, 80), (450, 340)], fill=(100, 130, 150))
    draw.rectangle([(480, 150), (750, 340)], fill=(140, 130, 110))
    
    # Building windows
    for bx in [60, 100, 140, 180]:
        for by in range(140, 320, 40):
            draw.rectangle([(bx, by), (bx+25, by+25)], fill=(240, 240, 200))
    for bx in [270, 330, 390]:
        for by in range(100, 320, 45):
            draw.rectangle([(bx, by), (bx+35, by+30)], fill=(220, 235, 245))

    # Car in background
    draw.rectangle([(550, 350), (760, 430)], fill=(40, 80, 160)) # Blue car
    draw.rectangle([(580, 310), (720, 350)], fill=(40, 80, 160))
    draw.rectangle([(590, 315), (640, 345)], fill=(190, 220, 240)) # window
    draw.rectangle([(650, 315), (710, 345)], fill=(190, 220, 240))
    draw.ellipse([(580, 410), (620, 450)], fill=(20, 20, 20))    # wheel
    draw.ellipse([(690, 410), (730, 450)], fill=(20, 20, 20))    # wheel

    # Person wearing RED shirt (Center stage)
    # Head
    draw.ellipse([(280, 210), (320, 250)], fill=(235, 195, 165))
    # Hair
    draw.chord([(280, 210), (320, 240)], 180, 360, fill=(45, 30, 20))
    # Red Shirt (Torso)
    draw.rectangle([(270, 250), (330, 370)], fill=(220, 35, 45))
    # Text on shirt
    draw.line([(270, 250), (330, 250)], fill=(180, 20, 30), width=3)
    # Pants (Blue jeans)
    draw.rectangle([(275, 370), (300, 490)], fill=(40, 60, 110))
    draw.rectangle([(302, 370), (325, 490)], fill=(40, 60, 110))
    # Shoes
    draw.rectangle([(270, 490), (300, 505)], fill=(25, 25, 25))
    draw.rectangle([(302, 490), (332, 505)], fill=(25, 25, 25))
    # Left arm holding umbrella
    draw.line([(270, 260), (240, 310)], fill=(220, 35, 45), width=12)
    # Umbrella shaft
    draw.line([(240, 170), (240, 360)], fill=(60, 60, 60), width=4)
    # Umbrella Canopy (Yellow umbrella)
    draw.pieslice([(150, 120), (330, 240)], 180, 360, fill=(245, 190, 30))
    # Backpack straps / backpack
    draw.rectangle([(325, 260), (345, 330)], fill=(50, 50, 50)) # backpack

    # Road markings
    for x in range(50, 800, 120):
        draw.rectangle([(x, 480), (x+60, 490)], fill=(250, 250, 250))

    img.save("static/samples/street_person.jpg", quality=95)
    print("Created static/samples/street_person.jpg")

def create_workspace_scene():
    img = Image.new("RGB", (800, 600), color=(235, 230, 220))
    draw = ImageDraw.Draw(img)
    # Wooden Table
    draw.rectangle([(50, 150), (750, 580)], fill=(180, 130, 90))
    draw.rectangle([(50, 540), (750, 580)], fill=(140, 100, 65))
    
    # Laptop
    draw.rectangle([(230, 210), (530, 410)], fill=(195, 200, 205)) # Laptop base
    draw.rectangle([(260, 225), (500, 350)], fill=(30, 35, 45))     # Screen
    draw.rectangle([(270, 235), (490, 340)], fill=(60, 120, 200))    # Wallpaper
    draw.rectangle([(290, 365), (470, 400)], fill=(150, 155, 160))   # Keyboard
    draw.rectangle([(360, 402), (400, 408)], fill=(130, 135, 140))   # Trackpad

    # Coffee Mug (Right side)
    draw.ellipse([(600, 280), (670, 350)], fill=(240, 70, 60))
    draw.ellipse([(610, 290), (660, 340)], fill=(75, 45, 30)) # Dark coffee
    draw.arc([(660, 295), (690, 335)], -90, 90, fill=(240, 70, 60), width=6) # Handle

    # Smartphone (Left side)
    draw.rectangle([(110, 300), (190, 440)], fill=(30, 30, 35))
    draw.rectangle([(115, 310), (185, 430)], fill=(100, 170, 240)) # Screen display

    # Notebook & Pen
    draw.rectangle([(140, 180), (220, 270)], fill=(245, 245, 230))
    for y in range(195, 265, 12):
        draw.line([(150, y), (210, y)], fill=(180, 180, 190), width=1)
    draw.line([(222, 190), (228, 260)], fill=(20, 20, 180), width=4) # Pen

    img.save("static/samples/workspace.jpg", quality=95)
    print("Created static/samples/workspace.jpg")

def create_dog_scene():
    img = Image.new("RGB", (800, 600), color=(150, 205, 245))
    draw = ImageDraw.Draw(img)
    # Sunny lawn
    draw.ellipse([(-100, 300), (900, 750)], fill=(110, 185, 80))
    # Sun
    draw.ellipse([(660, 40), (740, 120)], fill=(255, 225, 70))

    # Brown Dog sitting on lawn
    # Body
    draw.ellipse([(330, 310), (470, 450)], fill=(160, 95, 45))
    # Head
    draw.ellipse([(290, 240), (380, 330)], fill=(175, 105, 50))
    # Snout
    draw.ellipse([(270, 280), (320, 330)], fill=(205, 145, 95))
    draw.ellipse([(270, 285), (285, 298)], fill=(30, 20, 15)) # Nose
    # Eye
    draw.ellipse([(320, 265), (332, 277)], fill=(20, 15, 10))
    # Floppy Ear
    draw.ellipse([(350, 250), (385, 320)], fill=(120, 65, 25))
    # Legs
    draw.rectangle([(330, 420), (360, 480)], fill=(160, 95, 45))
    draw.rectangle([(380, 420), (410, 480)], fill=(160, 95, 45))
    draw.ellipse([(325, 470), (365, 490)], fill=(175, 105, 50))
    draw.ellipse([(375, 470), (415, 490)], fill=(175, 105, 50))
    # Tail
    draw.arc([(450, 340), (510, 400)], -100, 20, fill=(160, 95, 45), width=14)

    # Red Ball
    draw.ellipse([(200, 440), (250, 490)], fill=(230, 40, 40))
    draw.arc([(205, 445), (245, 485)], 45, 180, fill=(255, 200, 200), width=3)

    img.save("static/samples/dog_park.jpg", quality=95)
    print("Created static/samples/dog_park.jpg")

if __name__ == "__main__":
    create_street_scene()
    create_workspace_scene()
    create_dog_scene()
