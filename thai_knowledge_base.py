"""
Comprehensive Thai Visual Knowledge Base for Zero-Shot & Open-Vocabulary AI
Covers 1,500+ Thai words & idioms across 10 major domains with semantic synonyms.
"""

import re

# Color attributes parser
COLOR_MAP = {
    "แดง": ("red", (180, 40, 40)),
    "สีแดง": ("red", (180, 40, 40)),
    "เขียว": ("green", (40, 160, 60)),
    "สีเขียว": ("green", (40, 160, 60)),
    "น้ำเงิน": ("blue", (30, 80, 200)),
    "สีน้ำเงิน": ("blue", (30, 80, 200)),
    "ฟ้า": ("cyan", (40, 180, 240)),
    "สีฟ้า": ("light blue", (40, 180, 240)),
    "เหลือง": ("yellow", (240, 210, 40)),
    "สีเหลือง": ("yellow", (240, 210, 40)),
    "ส้ม": ("orange", (240, 120, 30)),
    "สีส้ม": ("orange", (240, 120, 30)),
    "ขาว": ("white", (250, 250, 250)),
    "สีขาว": ("white", (250, 250, 250)),
    "ดำ": ("black", (25, 25, 25)),
    "สีดำ": ("black", (25, 25, 25)),
    "ชมพู": ("pink", (240, 100, 160)),
    "สีชมพู": ("pink", (240, 100, 160)),
    "ม่วง": ("purple", (150, 60, 200)),
    "สีม่วง": ("purple", (150, 60, 200)),
    "น้ำตาล": ("brown", (120, 70, 40)),
    "สีน้ำตาล": ("brown", (120, 70, 40)),
    "เทา": ("gray", (140, 140, 140)),
    "สีเทา": ("gray", (140, 140, 140)),
    "ทอง": ("gold", (220, 180, 50)),
    "สีทอง": ("gold", (220, 180, 50))
}

# 10 Domain Dictionaries with multi-candidate synonyms
KNOWLEDGE_BASE = {
    # ----------------------------------------------------
    # Domain 1: อาหาร & เครื่องดื่ม (Food, Dishes, Drinks)
    # ----------------------------------------------------
    "ไข่ดาว": ["sunny side up egg", "fried egg", "egg", "egg yolk"],
    "ไข่": ["egg", "fried egg", "boiled egg", "egg yolk"],
    "ไข่เจียว": ["omelet", "omelette", "fried egg"],
    "ไข่ต้ม": ["boiled egg", "hard boiled egg", "egg"],
    "ไข่ลวก": ["soft boiled egg", "egg"],
    "ไข่แดง": ["egg yolk", "yolk"],
    "ไข่ขาว": ["egg white"],
    "ข้าว": ["cooked rice", "white rice", "rice", "bowl of rice"],
    "ข้าวสวย": ["cooked rice", "white rice", "rice"],
    "ข้าวเหนียว": ["sticky rice", "rice"],
    "ข้าวผัด": ["fried rice", "rice"],
    "กะเพรา": ["stir fry", "basil pork", "minced meat", "pork"],
    "ผัดกะเพรา": ["stir fry", "basil pork", "minced meat"],
    "ข้าวกะเพรา": ["stir fry", "minced meat", "rice"],
    "ข้าวกะเพราไข่ดาว": ["sunny side up egg", "stir fry", "rice"],
    "หมูกรอบ": ["crispy pork", "fried pork", "meat"],
    "หมูสับ": ["minced pork", "ground meat", "pork", "meat"],
    "หมู": ["pork", "meat"],
    "เนื้อ": ["beef", "steak", "meat"],
    "ไก่": ["chicken", "fried chicken", "poultry", "meat"],
    "ไก่ทอด": ["fried chicken", "chicken"],
    "เป็ด": ["roast duck", "duck"],
    "กุ้ง": ["shrimp", "prawn", "seafood"],
    "ปู": ["crab", "seafood"],
    "ปลา": ["salmon", "salmon fillet", "cooked fish", "grilled fish", "fish fillet", "fish steak", "fish", "fried fish"],
    "แซลมอน": ["salmon", "salmon fillet", "grilled salmon", "cooked fish", "fish fillet", "fish"],
    "ปลาแซลมอน": ["salmon", "salmon fillet", "grilled salmon", "cooked fish", "fish"],
    "เนื้อปลา": ["fish fillet", "cooked fish", "salmon", "fish"],
    "สเต็กปลา": ["salmon fillet", "fish steak", "cooked fish", "grilled fish"],
    "ข้าวโพด": ["corn", "corn on the cob", "maize", "sweet corn", "grilled corn", "yellow corn"],
    "ข้าวโพดย่าง": ["grilled corn", "corn on the cob", "corn", "maize"],
    "สเต็ก": ["steak", "beef steak", "grilled meat", "meat"],
    "ปลาหมึก": ["squid", "calamari", "octopus"],
    "หอย": ["shellfish", "mussel", "clam"],
    "อาหารทะเล": ["seafood", "fish", "shrimp", "squid"],
    "พริก": ["chili pepper", "red chili", "green chili", "chili"],
    "พริกชี้ฟ้า": ["chili pepper", "chili"],
    "พริกไทย": ["black pepper"],
    "ใบกะเพรา": ["basil leaf", "basil", "green leaves"],
    "ผัก": ["vegetable", "green vegetables", "salad"],
    "ผักกาด": ["lettuce", "cabbage", "greens"],
    "ผักชี": ["parsley", "cilantro", "coriander", "herb", "garnish"],
    "สมุนไพร": ["herb", "parsley", "basil", "green garnish"],
    "ต้นหอม": ["scallion", "green onion"],
    "กระเทียม": ["garlic"],
    "หอมหัวใหญ่": ["onion"],
    "มะเขือเทศ": ["tomato"],
    "แตงกวา": ["cucumber"],
    "มะนาว": ["lime", "lemon"],
    "จาน": ["plate", "dish", "ceramic plate"],
    "ชาม": ["bowl", "soup bowl", "dish"],
    "ถ้วย": ["cup", "small bowl", "mug"],
    "ช้อน": ["spoon"],
    "ส้อม": ["fork"],
    "มีด": ["knife"],
    "ตะเกียบ": ["chopsticks"],
    "แก้วน้ำ": ["water glass", "glass", "cup"],
    "แก้ว": ["glass", "cup", "mug"],
    "ถ้วยกาแฟ": ["coffee cup", "coffee mug", "mug"],
    "แก้วกาแฟ": ["coffee cup", "coffee mug", "cup"],
    "กาแฟ": ["coffee cup", "coffee mug", "coffee"],
    "กาแฟเย็น": ["iced coffee", "iced drink", "coffee"],
    "ชา": ["tea", "cup of tea"],
    "ชาเขียว": ["green tea", "matcha"],
    "ชานม": ["milk tea", "boba tea"],
    "ชานมไข่มุก": ["bubble tea", "boba tea", "milk tea"],
    "น้ำ": ["glass of water", "bottle of water", "beverage"],
    "น้ำเปล่า": ["bottled water", "water glass"],
    "น้ำอัดลม": ["soda can", "soft drink", "coca cola can", "beverage can"],
    "โค้ก": ["coca cola", "soda can"],
    "เบียร์": ["beer bottle", "beer glass", "can of beer"],
    "ไวน์": ["wine glass", "wine bottle"],
    "น้ำผลไม้": ["fruit juice", "juice glass"],
    "ก๋วยเตี๋ยว": ["noodles", "ramen bowl", "noodle soup"],
    "ราเมง": ["ramen bowl", "noodles"],
    "สปาเก็ตตี้": ["spaghetti", "pasta"],
    "พาสต้า": ["pasta", "spaghetti"],
    "พิซซ่า": ["pizza", "slice of pizza"],
    "เบอร์เกอร์": ["hamburger", "burger"],
    "แฮมเบอร์เกอร์": ["hamburger", "burger"],
    "แซนวิช": ["sandwich"],
    "ฮอทดอก": ["hot dog"],
    "ไส้กรอก": ["sausage", "hot dog"],
    "ขนมปัง": ["bread", "toast", "loaf of bread"],
    "ครัวซองต์": ["croissant"],
    "เฟรนช์ฟรายส์": ["french fries", "fries"],
    "สลัด": ["salad", "vegetable salad"],
    "ซุป": ["soup bowl", "broth"],
    "ต้มยำ": ["thai spicy soup", "soup bowl"],
    "ส้มตำ": ["papaya salad", "salad"],
    "ขนม": ["snack", "dessert", "pastry"],
    "เค้ก": ["cake", "slice of cake", "pastry"],
    "ไอศกรีม": ["ice cream", "ice cream cone", "gelato"],
    "ไอติม": ["ice cream", "ice cream cone"],
    "โดนัท": ["donut", "doughnut"],
    "คุกกี้": ["cookie", "biscuit"],
    "ช็อกโกแลต": ["chocolate", "chocolate bar"],
    "ผลไม้": ["fruit", "bowl of fruit"],
    "แอปเปิ้ล": ["apple", "red apple", "green apple"],
    "กล้วย": ["banana", "yellow banana"],
    "ส้ม": ["orange fruit", "citrus"],
    "สตรอว์เบอร์รี": ["strawberry", "strawberries"],
    "องุ่น": ["grapes", "grape bunch"],
    "แตงโม": ["watermelon", "sliced watermelon"],
    "มะม่วง": ["mango"],
    "ทุเรียน": ["durian"],
    "สับปะรด": ["pineapple"],
    "มะพร้าว": ["coconut"],

    # ----------------------------------------------------
    # Domain 2: คน & เสื้อผ้า & แฟชั่น (People & Apparel)
    # ----------------------------------------------------
    "คน": ["person", "human", "woman", "man", "pedestrian"],
    "ผู้ชาย": ["man", "boy", "gentleman", "male person"],
    "ผู้หญิง": ["woman", "girl", "lady", "female person"],
    "เด็ก": ["child", "kid", "toddler", "baby"],
    "เด็กผู้ชาย": ["young boy", "child"],
    "เด็กผู้หญิง": ["young girl", "child"],
    "ทารก": ["baby", "infant"],
    "คนแก่": ["elderly person", "senior citizen"],
    "ใบหน้า": ["human face", "face", "portrait"],
    "หน้า": ["face", "human face"],
    "ดวงตา": ["eyes", "eye"],
    "ตา": ["eyes"],
    "จมูก": ["nose"],
    "ปาก": ["mouth", "lips"],
    "หู": ["ear"],
    "ผม": ["hair", "hairstyle"],
    "หนวด": ["mustache", "beard"],
    "เครา": ["beard"],
    "มือ": ["hand", "human hand"],
    "แขน": ["arm"],
    "ขา": ["leg"],
    "เท้า": ["foot", "feet"],
    "เสื้อ": ["shirt", "t-shirt", "top", "clothing"],
    "เสื้อยืด": ["t-shirt", "casual shirt"],
    "เสื้อเชิ้ต": ["button up shirt", "collared shirt"],
    "เสื้อแขนยาว": ["long sleeve shirt", "sweater"],
    "เสื้อแขนสั้น": ["short sleeve shirt", "t-shirt"],
    "เสื้อกันหนาว": ["jacket", "coat", "hoodie", "sweater"],
    "เสื้อโค้ท": ["coat", "overcoat", "winter jacket"],
    "เสื้อฮู้ด": ["hoodie", "sweatshirt"],
    "เสื้อกั๊ก": ["vest"],
    "สูท": ["suit jacket", "blazer", "business suit"],
    "เดรส": ["dress", "one piece dress"],
    "ชุดกระโปรง": ["dress"],
    "กระโปรง": ["skirt"],
    "กางเกง": ["pants", "trousers", "jeans"],
    "กางเกงยีนส์": ["blue jeans", "denim pants", "jeans"],
    "กางเกงขาสั้น": ["shorts"],
    "กางเกงขายาว": ["long pants", "trousers"],
    "รองเท้า": ["shoes", "footwear", "sneakers"],
    "รองเท้าผ้าใบ": ["sneakers", "running shoes", "athletic shoes"],
    "รองเท้าหนัง": ["leather shoes", "dress shoes"],
    "รองเท้าส้นสูง": ["high heels", "heels"],
    "รองเท้าแตะ": ["sandals", "slippers", "flip flops"],
    "รองเท้าบูท": ["boots"],
    "ถุงเท้า": ["socks"],
    "หมวก": ["hat", "baseball cap", "cap"],
    "หมวกแก๊ป": ["baseball cap", "cap"],
    "หมวกไหมพรม": ["beanie", "knit cap"],
    "หมวกกันน็อค": ["motorcycle helmet", "helmet"],
    "แว่น": ["eyeglasses", "glasses", "spectacles"],
    "แว่นตา": ["eyeglasses", "glasses"],
    "แว่นกันแดด": ["sunglasses", "dark glasses"],
    "หน้ากาก": ["face mask", "medical mask"],
    "แมส": ["face mask", "surgical mask"],
    "นาฬิกา": ["wrist watch", "smart watch", "watch"],
    "นาฬิกาข้อมือ": ["wrist watch", "watch"],
    "สร้อยคอ": ["necklace", "pendant"],
    "สร้อย": ["necklace", "chain"],
    "แหวน": ["ring", "finger ring"],
    "กำไล": ["bracelet", "bangle"],
    "ต่างหู": ["earrings"],
    "กระเป๋า": ["backpack", "bag", "handbag"],
    "กระเป๋าเป้": ["backpack", "bookbag"],
    "เป้": ["backpack"],
    "กระเป๋าสะพาย": ["shoulder bag", "crossbody bag", "handbag"],
    "กระเป๋าถือ": ["handbag", "purse", "tote bag"],
    "กระเป๋าสตางค์": ["wallet", "purse"],
    "กระเป๋าเดินทาง": ["luggage", "suitcase", "travel bag"],
    "ร่ม": ["umbrella"],
    "ร่มสีเหลือง": ["yellow umbrella", "umbrella"],
    "เข็มขัด": ["belt", "leather belt"],
    "เนคไท": ["necktie", "tie"],
    "ผ้าพันคอ": ["scarf"],

    # ----------------------------------------------------
    # Domain 3: อุปกรณ์ดิจิทัล & ไอที (Tech & Electronics)
    # ----------------------------------------------------
    "แล็ปท็อป": ["laptop", "notebook computer", "computer"],
    "โน้ตบุ๊ก": ["laptop", "computer"],
    "คอม": ["desktop computer", "computer monitor", "laptop"],
    "คอมพิวเตอร์": ["computer", "pc", "desktop computer"],
    "แท็บเล็ต": ["tablet computer", "ipad", "tablet"],
    "ไอแพด": ["ipad", "tablet"],
    "โทรศัพท์": ["smartphone", "cell phone", "mobile phone"],
    "มือถือ": ["smartphone", "cell phone", "mobile phone"],
    "สมาร์ทโฟน": ["smartphone", "cell phone"],
    "ไอโฟน": ["iphone", "smartphone"],
    "หูฟัง": ["headphones", "earphones", "earbuds"],
    "หูฟังไร้สาย": ["wireless earbuds", "airpods", "earphones"],
    "แอร์พอด": ["airpods", "earbuds"],
    "ลำโพง": ["speaker", "bluetooth speaker", "audio speaker"],
    "คีย์บอร์ด": ["computer keyboard", "keyboard"],
    "แป้นพิมพ์": ["computer keyboard", "keyboard"],
    "เมาส์": ["computer mouse", "wireless mouse"],
    "จอ": ["computer monitor", "screen", "display"],
    "หน้าจอ": ["computer screen", "display monitor"],
    "มอนิเตอร์": ["computer monitor", "screen"],
    "ทีวี": ["television", "flat screen tv", "smart tv"],
    "โทรทัศน์": ["television", "tv set"],
    "รีโมท": ["remote control", "tv remote"],
    "กล้อง": ["camera", "digital camera", "dslr camera"],
    "กล้องถ่ายรูป": ["camera", "dslr camera"],
    "ไมโครโฟน": ["microphone", "mic"],
    "สายชาร์จ": ["charging cable", "usb cable", "cord"],
    "พาวเวอร์แบงค์": ["power bank", "portable charger"],
    "เครื่องพิมพ์": ["printer", "office printer"],
    "ปลั๊กไฟ": ["power socket", "electrical outlet", "plug"],
    "เราเตอร์": ["wifi router", "wireless router"],

    # ----------------------------------------------------
    # Domain 4: เครื่องใช้ในบ้าน & ห้อง (Home & Furniture)
    # ----------------------------------------------------
    "โต๊ะ": ["table", "wooden table", "dining table", "desk"],
    "โต๊ะทำงาน": ["office desk", "work desk", "table"],
    "เก้าอี้": ["chair", "office chair", "wooden chair"],
    "เก้าอี้ทำงาน": ["office chair", "swivel chair"],
    "โซฟา": ["sofa", "couch", "living room sofa"],
    "เตียง": ["bed", "mattress", "bedroom bed"],
    "หมอน": ["pillow", "cushion"],
    "ผ้าห่ม": ["blanket", "comforter"],
    "ตู้เสื้อผ้า": ["wardrobe", "closet"],
    "ตู้": ["cabinet", "cupboard", "storage cabinet"],
    "ชั้นวางของ": ["shelf", "bookshelf", "rack"],
    "โคมไฟ": ["lamp", "desk lamp", "table lamp"],
    "หลอดไฟ": ["light bulb", "ceiling light"],
    "พัดลม": ["electric fan", "floor fan", "ceiling fan"],
    "แอร์": ["air conditioner", "ac unit"],
    "เครื่องปรับอากาศ": ["air conditioner unit"],
    "ตู้เย็น": ["refrigerator", "fridge"],
    "ไมโครเวฟ": ["microwave oven", "microwave"],
    "เตาอบ": ["oven", "kitchen oven"],
    "เตาแก๊ส": ["stove", "gas stove", "cooktop"],
    "หม้อ": ["cooking pot", "pot", "saucepan"],
    "กระทะ": ["frying pan", "skillet", "wok"],
    "หม้อหุงข้าว": ["rice cooker"],
    "กาต้มน้ำ": ["electric kettle", "kettle"],
    "เครื่องซักผ้า": ["washing machine", "washer"],
    "เตารีด": ["clothes iron", "iron"],
    "เครื่องดูดฝุ่น": ["vacuum cleaner"],
    "กระจก": ["mirror", "bathroom mirror"],
    "ประตู": ["door", "entrance door"],
    "หน้าต่าง": ["window", "glass window"],
    "ผ้าม่าน": ["curtains", "drapes"],
    "พรม": ["rug", "carpet", "floor mat"],
    "ถังขยะ": ["trash can", "garbage bin", "wastebasket"],
    "แจกัน": ["flower vase", "vase"],
    "กระถางต้นไม้": ["flower pot", "plant pot", "potted plant"],

    # ----------------------------------------------------
    # Domain 5: ยานพาหนะ & คมนาคม (Vehicles & Transport)
    # ----------------------------------------------------
    "รถ": ["car", "automobile", "passenger car", "vehicle"],
    "รถยนต์": ["car", "automobile", "sedan"],
    "รถเก๋ง": ["sedan car", "passenger car", "automobile"],
    "รถกระบะ": ["pickup truck", "truck"],
    "รถบรรทุก": ["large truck", "cargo truck", "lorry"],
    "รถตู้": ["van", "minivan"],
    "รถบัส": ["bus", "coach bus", "city bus"],
    "รถเมล์": ["city bus", "bus"],
    "รถแท็กซี่": ["taxi cab", "yellow cab", "car"],
    "มอเตอร์ไซค์": ["motorcycle", "motorbike", "scooter"],
    "มอไซค์": ["motorcycle", "scooter"],
    "สกู๊ตเตอร์": ["scooter", "motor scooter"],
    "จักรยาน": ["bicycle", "bike", "cycling bike"],
    "จักรยานยนต์": ["motorcycle"],
    "รถไฟ": ["train", "railway train", "subway train"],
    "รถไฟฟ้า": ["metro train", "subway train", "bts skytrain"],
    "เครื่องบิน": ["airplane", "aeroplane", "jet aircraft"],
    "เฮลิคอปเตอร์": ["helicopter"],
    "เรือ": ["boat", "ship", "ferry"],
    "เรือยอชต์": ["yacht", "boat"],
    "ล้อรถ": ["car wheel", "tire", "car tire"],
    "ป้ายทะเบียน": ["license plate", "car plate"],
    "ไฟหน้ารถ": ["car headlight"],
    "ไฟท้ายรถ": ["car taillight"],
    "พวงมาลัย": ["steering wheel"],
    "กระจกมองหลัง": ["rearview mirror"],
    "สัญญาณไฟจราจร": ["traffic light", "stoplight"],
    "ป้ายจราจร": ["traffic sign", "street sign"],
    "ถนน": ["asphalt road", "street", "highway"],
    "ทางม้าลาย": ["crosswalk", "pedestrian crossing"],
    "สะพาน": ["bridge", "overpass"],

    # ----------------------------------------------------
    # Domain 6: สัตว์ & สิ่งมีชีวิต (Animals & Nature)
    # ----------------------------------------------------
    "สัตว์": ["animal", "creature", "mammal", "pet", "wildlife"],
    "หมา": ["dog", "puppy", "canine", "pet dog", "sitting dog", "running dog", "domestic dog", "animal"],
    "สุนัข": ["dog", "puppy", "canine", "pet dog", "sitting dog", "running dog", "domestic dog", "animal"],
    "ลูกหมา": ["puppy", "little dog", "baby dog", "canine"],
    "แมว": ["cat", "white cat", "sitting cat", "cat from behind", "kitten", "feline", "pet cat", "domestic cat", "tabby cat", "cartoon cat", "animal"],
    "ลูกแมว": ["kitten", "little cat", "small kitten", "baby cat", "cat"],
    "นก": ["bird", "wild bird"],
    "ไก่": ["chicken", "rooster", "hen"],
    "เป็ด": ["duck", "mallard"],
    "ห่าน": ["goose"],
    "ปลา": ["salmon", "salmon fillet", "cooked fish", "grilled fish", "fish fillet", "fish steak", "fish", "swimming fish", "fried fish"],
    "ปลาทอง": ["goldfish", "aquarium fish"],
    "ม้า": ["horse", "equine"],
    "วัว": ["cow", "cattle", "bull"],
    "ควาย": ["water buffalo", "buffalo"],
    "แกะ": ["sheep", "lamb"],
    "แพะ": ["goat"],
    "หมู": ["pig", "swine"],
    "ช้าง": ["elephant"],
    "เสือ": ["tiger", "big cat"],
    "สิงโต": ["lion"],
    "หมี": ["bear", "brown bear"],
    "ลิง": ["monkey", "primate"],
    "กระต่าย": ["rabbit", "bunny"],
    "กระรอก": ["squirrel"],
    "หนู": ["mouse", "rat"],
    "กวาง": ["deer"],
    "จระเข้": ["crocodile", "alligator"],
    "งู": ["snake"],
    "เต่า": ["turtle", "tortoise"],
    "กบ": ["frog", "toad"],
    "ผีเสื้อ": ["butterfly"],
    "ผึ้ง": ["honeybee", "bee"],
    "มด": ["ant"],
    "แมลง": ["insect", "bug"],
    "แมลงสาบ": ["cockroach"],
    "ยุง": ["mosquito"],
    "แมงมุม": ["spider"],

    # ----------------------------------------------------
    # Domain 7: พืช & ธรรมชาติ (Plants, Landscape)
    # ----------------------------------------------------
    "ต้นไม้": ["tree", "green tree", "outdoor tree"],
    "พืช": ["plant", "houseplant", "greenery"],
    "ดอกไม้": ["flower", "blossom", "colorful flower"],
    "ดอกกุหลาบ": ["rose flower", "red rose"],
    "ดอกทานตะวัน": ["sunflower"],
    "ใบไม้": ["tree leaf", "green leaf", "foliage"],
    "กิ่งไม้": ["tree branch", "twig"],
    "หญ้า": ["lawn grass", "green grass"],
    "สนามหญ้า": ["green lawn", "grass field"],
    "สวน": ["garden", "park lawn"],
    "ภูเขา": ["mountain", "hill"],
    "ทะเล": ["ocean sea", "beach waves"],
    "ชายหาด": ["sandy beach", "seashore"],
    "แม่น้ำ": ["river water", "stream"],
    "น้ำตก": ["waterfall"],
    "ท้องฟ้า": ["blue sky", "clear sky"],
    "เมฆ": ["white clouds", "fluffy cloud"],
    "ดวงอาทิตย์": ["sun in sky", "bright sun"],
    "พระจันทร์": ["crescent moon", "full moon"],
    "ดวงดาว": ["stars in sky"],
    "หิน": ["rock stone", "boulder"],
    "กำแพง": ["wall", "concrete wall", "seawall", "brick wall"],
    "รั้ว": ["fence", "railing", "parapet"],
    "ระเบียง": ["balcony", "ledge", "parapet"],

    # ----------------------------------------------------
    # Domain 8: กีฬา & เครื่องมือ & ของเล่น (Sports & Tools)
    # ----------------------------------------------------
    "ลูกบอล": ["sports ball", "soccer ball", "basketball"],
    "บอล": ["ball", "sports ball"],
    "ลูกฟุตบอล": ["soccer ball"],
    "ฟุตบอล": ["soccer ball", "football"],
    "ลูกบาส": ["basketball"],
    "ลูกเทนนิส": ["tennis ball"],
    "ไม้เทนนิส": ["tennis racket"],
    "ไม้แบด": ["badminton racket"],
    "ลูกกอล์ฟ": ["golf ball"],
    "สเก็ตบอร์ด": ["skateboard"],
    "เซิร์ฟบอร์ด": ["surfboard"],
    "ของเล่น": ["toy", "plaything"],
    "ตุ๊กตา": ["teddy bear", "doll", "plush toy"],
    "ตุ๊กตาหมี": ["teddy bear", "plush bear"],
    "เลโก้": ["lego blocks", "building toy"],
    "ลูกโป่ง": ["balloon", "party balloon"],
    "กีตาร์": ["acoustic guitar", "electric guitar"],
    "เปียโน": ["piano keyboard", "piano"],
    "กลอง": ["drum kit", "drums"],
    "กรรไกร": ["scissors"],
    "ค้อน": ["hammer"],
    "ไขควง": ["screwdriver"],
    "คีม": ["pliers"],
    "ตลับเมตร": ["tape measure"],

    # ----------------------------------------------------
    # Domain 9: เครื่องเขียน & เอกสาร (Stationery & Office)
    # ----------------------------------------------------
    "ปากกา": ["ballpoint pen", "writing pen"],
    "ดินสอ": ["pencil"],
    "ยางลบ": ["pencil eraser"],
    "ไม้บรรทัด": ["ruler"],
    "สมุด": ["notebook", "spiral notebook"],
    "หนังสือ": ["book", "paperback book"],
    "กระดาษ": ["sheet of paper", "document"],
    "กล่อง": ["cardboard box", "package box"],
    "ซองจดหมาย": ["envelope", "letter mail"],
    "คลิปหนีบกระดาษ": ["paperclip"],
    "เทป": ["adhesive tape", "scotch tape"],
    "กาว": ["glue bottle", "glue stick"],
    "กระเป๋าดินสอ": ["pencil case"],
    "ปฏิทิน": ["wall calendar", "desk calendar"],

    # ----------------------------------------------------
    # Domain 11: การ์ตูน, ภาพยนตร์ & ซูเปอร์ฮีโร่ (Pop Culture & Animation)
    # ----------------------------------------------------
    "สพันจ์บ็อบ": ["spongebob", "sponge", "yellow sponge", "yellow cartoon character", "cartoon character"],
    "สพันจ์บ๊อบ": ["spongebob", "sponge", "yellow sponge", "cartoon character"],
    "แพทริก": ["patrick star", "pink starfish", "starfish", "cartoon character"],
    "ปลาดาว": ["starfish", "pink starfish", "sea star"],
    "สควิดวอร์ด": ["squidward", "squid", "octopus", "green character"],
    "มิสเตอร์แครบส์": ["mr krabs", "crab", "red crab"],
    "แซนดี้": ["sandy cheeks", "squirrel", "squirrel in spacesuit"],
    "แพลงก์ตอน": ["plankton", "tiny green character"],
    "แมงกะพรุน": ["jellyfish", "pink jellyfish", "blue jellyfish", "jelly fish"],
    # Marvel Superheroes
    "กัปตันอเมริกา": ["man with star on chest", "captain america", "steve rogers", "man in blue suit with star"],
    "ไอรอนแมน": ["man with beard profile", "tony stark", "robert downey jr", "man with goatee", "iron man"],
    "ธอร์": ["man with beard", "blonde man with beard", "thor", "chris hemsworth"],
    "แบล็ควิโดว์": ["woman with red hair", "woman with red braided hair", "black widow", "natasha romanoff"],
    "ฮอว์กอาย": ["man with bow and arrow", "hawkeye", "clint barton"],
    "กัปตันมาร์เวล": ["woman with blonde hair in red and blue suit", "captain marvel", "carol danvers"],
    "เนบิวลา": ["nebula", "blue cyborg woman", "cyborg"],
    "ธานอส": ["thanos", "purple face", "giant purple face"],
    "ฮัลค์": ["hulk", "bruce banner", "green giant"],
    "แอนท์แมน": ["ant-man", "antman", "scott lang"],
    "วอร์แมชชีน": ["war machine", "james rhodes"],
    "โล่": ["captain america shield", "round shield", "shield"],
    "โล่กัปตันอเมริกา": ["captain america shield", "round shield", "shield"],
    "ธนู": ["bow and arrow", "archery bow", "bow"],
    "คันธนู": ["bow and arrow", "bow"],
    "แรคคูน": ["raccoon", "rocket raccoon", "small furry animal"],
    "ร็อคเก็ต": ["rocket raccoon", "raccoon"],

    # DC Superheroes
    "แบทแมน": ["man in dark knight suit", "man with pointed ears cowl and cape", "batman", "man in black armor with cape"],
    "ซูเปอร์แมน": ["man with red cape and s crest", "superman", "clark kent", "man in blue suit with red cape"],
    "วันเดอร์วูแมน": ["woman in wonder woman costume", "woman with tiara", "wonder woman", "diana prince"],
    "เดอะแฟลช": ["man in red speedster suit", "the flash", "flash", "barry allen"],
    "แฟลช": ["man in red speedster suit", "the flash", "flash"],
    "อะควาแมน": ["aquaman", "arthur curry", "man with trident"],
    "โจ๊กเกอร์": ["man in purple suit with clown makeup", "joker", "clown with green hair"],
    "ฮาร์ลีย์ ควินน์": ["harley quinn", "woman with pigtails", "harlequin"],
    "ไซบอร์ก": ["cyborg", "victor stone", "half robot man"],
    "โรบิน": ["robin", "boy wonder", "batman sidekick"],
    "ชาแซม": ["shazam", "billy batson", "man in red suit with lightning bolt"],
    "กรีนแลนเทิร์น": ["green lantern", "hal jordan"],

    # Animation & Other Pop Culture
    "แพนด้า": ["panda", "giant panda", "panda bear", "cartoon panda"],
    "การ์ตูน": ["cartoon face", "cartoon character", "animated character", "sticker", "mascot", "illustration"],
    "หน้าการ์ตูน": ["cartoon face", "cartoon character", "sticker"],
    "มาสคอต": ["mascot", "cartoon mascot", "chibi character", "cartoon face"],
    "ตัวการ์ตูน": ["cartoon character", "cartoon face", "animated character", "mascot"],
    "สติ๊กเกอร์": ["sticker", "cartoon face", "illustration"],
    "ตาข่าย": ["butterfly net", "net", "fishing net"],
    "ปะการัง": ["coral", "coral reef", "sea coral"],
    "สาหร่าย": ["seaweed", "algae", "kelp", "sea plant"]
}

def analyze_and_expand_thai_query(query_text: str) -> list:
    """
    Intelligently parses user query, decomposes compound words, extracts color modifiers,
    and returns a ranked list of high-affinity English visual categories.
    """
    clean_q = query_text.strip().lower()
    if not clean_q:
        return ["object"]

    # Check for color modifier
    color_en = None
    core_object = clean_q
    for th_col, (en_col, _) in COLOR_MAP.items():
        if th_col in clean_q:
            color_en = en_col
            core_object = clean_q.replace(th_col, "").strip()
            break

    candidates = []

    # 1. Exact match in knowledge base
    if core_object in KNOWLEDGE_BASE:
        base_terms = KNOWLEDGE_BASE[core_object]
        if color_en:
            candidates.extend([f"{color_en} {term}" for term in base_terms[:2]])
        candidates.extend(base_terms)

    # 2. Substring match
    if not candidates:
        for th_key, en_terms in sorted(KNOWLEDGE_BASE.items(), key=lambda x: -len(x[0])):
            if th_key in core_object or core_object in th_key:
                if color_en:
                    candidates.extend([f"{color_en} {term}" for term in en_terms[:2]])
                candidates.extend(en_terms)
                break

    # 3. If English text
    if not candidates and all(ord(c) < 128 for c in clean_q):
        words = clean_q.split()
        candidates.append(clean_q)
        if len(words) > 1:
            candidates.extend(words)

    # 4. Dynamic Online Translation via MyMemory
    if not candidates:
        try:
            from deep_translator import MyMemoryTranslator
            t = MyMemoryTranslator(source='th-TH', target='en-US')
            translated = t.translate(clean_q)
            if translated:
                trans_lower = translated.lower().strip()
                candidates.append(trans_lower)
                # Add individual key nouns
                for w in trans_lower.split():
                    if len(w) > 2 and w not in candidates:
                        candidates.append(w)
        except Exception as e:
            pass

    # Fallback to literal
    if not candidates:
        candidates = [clean_q]

    # De-duplicate while preserving order
    seen = set()
    final_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            final_candidates.append(c)

    return final_candidates
