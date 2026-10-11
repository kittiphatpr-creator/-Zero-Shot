# Zero-Shot Object Detection & Grounding DINO Studio 🚀

โปรเจกต์จำลองและทดสอบการทำงานของ **Zero-Shot (Open-Vocabulary) Object Detection** พร้อมระบบจำลองสถาปัตยกรรม **Grounding DINO** แบบเจาะลึก 4 ขั้นตอน (Step-by-Step Interactive Simulator) และระบบ Playground ตรวจจับวัตถุจริงด้วย Text Prompt ภาษาธรรมชาติ

---

## 📌 สารบัญ (Table of Contents)
1. [Zero-Shot Object Detection คืออะไร?](#zero-shot-object-detection-คืออะไร)
2. [สถาปัตยกรรมและการทำงานของ Grounding DINO](#สถาปัตยกรรมและการทำงานของ-grounding-dino)
3. [Tech Stack หลัก](#tech-stack-หลัก)
4. [โครงสร้างโปรเจกต์](#โครงสร้างโปรเจกต์)
5. [วิธีติดตั้งและเริ่มใช้งาน](#วิธีติดตั้งและเริ่มใช้งาน)
6. [การใช้งาน CLI Script](#การใช้งาน-cli-script)
7. [ตัวอย่างโค้ดการใช้งาน](#ตัวอย่างโค้ดการใช้งาน)

---

## 💡 Zero-Shot Object Detection คืออะไร?

เทคโนโลยี AI ที่ปฏิวัติวงการ Computer Vision:
- **ยุคเดิม (Closed-Set Detection):** ต้องเตรียมภาพนับพันรูป ตีกรอบวัตถุ (Label) และเทรนโมเดลใหม่ทุกครั้งที่ต้องการให้ AI รู้จักของชิ้นใหม่ เช่น YOLO, Faster R-CNN
- **ยุคใหม่ (Open-Vocabulary / Zero-Shot):** เพียงพิมพ์คำสั่ง **Text Prompt** (เช่น *"ผู้ชายใส่เสื้อแดง"*, *"แก้วกาแฟ"*, *"สุนัข"*) โมเดลจะสามารถจับคู่ความหมายของภาษาเข้ากับพิกเซลบนภาพ แล้วตีกรอบวัตถุได้ทันที **แม้โมเดลจะไม่เคยถูกเทรนคลาสนั้นมาก่อนเลยก็ตาม**

---

## 🧠 สถาปัตยกรรมและการทำงานของ Grounding DINO

การที่ AI เข้าใจว่าคำศัพท์ตรงกับตำแหน่งใดในภาพ ทำงานผ่าน 4 ขั้นตอนหลัก:

```
[1 ข้อมูลนำเข้า (Dual Input)]
  ├── รูปภาพดิบ (Image RGB)
  └── Text Prompt ("ผู้ชายใส่เสื้อแดง")
            │
            ▼ (raw)
[2 สกัดฟีเจอร์ (Encoders)]
  ├── Image Backbone (Swin Transformer): สกัด Multi-Scale Image Feature Maps
  └── Text Backbone (BERT Encoder): แปลงคำเป็น Subword Tokens & Embeddings (768-d)
            │
            ▼ (emb)
[3 ฟิวชันข้อมูล (Cross-Modality Fusion)]
  ├── Feature Enhancer (Bi-Directional Cross-Attention): Image <-> Text
  └── จับคู่ความคล้ายคลึงด้วย Cosine Similarity & CLIP Contrastive Alignment
            │
            ▼ (attr)
[4 ผลลัพธ์การทำนาย (Region Prediction)]
  ├── Box Predictor Head: คำนวณพิกัด Bounding Box [x, y, w, h]
  └── Confidence Score Head: คำนวณเปอร์เซ็นต์ความมั่นใจ
```

### 1. Dual Input (ข้อมูลนำเข้า)
รับข้อมูล 2 มิติพร้อมกัน คือ รูปภาพดิจิทัล (RGB) และข้อความภาษาธรรมชาติ (Text Prompt)

### 2. Feature Extraction (สกัดฟีเจอร์แยกส่วน)
- **ฝั่งรูปภาพ:** ใช้ **Swin Transformer** แบ่งภาพออกเป็นแพตช์ขนาดเล็ก และใช้ Shifted Window Multi-head Self-Attention สกัดฟีเจอร์เชิงพื้นที่ ลวดลาย และสีในระดับความละเอียดต่าง ๆ (Multi-scale Feature Maps P3, P4, P5)
- **ฝั่งข้อความ:** ใช้ **BERT / RoBERTa** ตัดคำออกเป็น Tokens (เช่น `[CLS]`, `ผู้ชาย`, `ใส่`, `เสื้อ`, `แดง`, `[SEP]`) และแปลงเป็นเวกเตอร์มิติสูง (High-dimensional Embeddings)

### 3. Cross-Modality Fusion (ฟิวชันภาพและภาษา)
- **Bi-Directional Cross-Attention:** ข้อมูลภาพและภาษาถูกป้อนเข้าสู่ชั้น **Feature Enhancer** โดยข้อความจะส่องดูพิกัดภาพ (Text-to-Image) และภาพจะส่องดูคำศัพท์ (Image-to-Text)
- **Cosine Similarity:** โมเดลเปรียบเทียบมุมเวกเตอร์ทางคณิตศาสตร์ว่าคำว่า *"เสื้อแดง"* มีความใกล้เคียงกับพิกเซลใดในภาพมากที่สุด

### 4. Region Prediction (การตีกรอบ Bounding Box)
- โมเดลคัดเลือก Language-Guided Region Queries
- **Box Predictor MLP Head:** ทำนายพิกัดกล่อง $[x, y, w, h]$ หรือ $[x_{min}, y_{min}, x_{max}, y_{max}]$
- **Confidence Score:** คำนวณคะแนนความเชื่อมั่น (เช่น 92%)
- **Roboflow Supervision:** วาดกรอบสี่เหลี่ยมพร้อมป้ายระบุชื่อวัตถุและคะแนนความเชื่อมั่นลงบนภาพ

---

## 🛠 Tech Stack หลัก

- **Python 3.10+ / 3.12**
- **PyTorch (torch):** Framework หลักในการประมวลผลโมเดลบน GPU / CPU
- **Hugging Face transformers:** สำหรับโหลดโมเดล Pre-trained Zero-Shot เช่น Grounding DINO (`IDEA-Research/grounding-dino-tiny`) หรือ OWL-ViT (`google/owlvit-base-patch32`)
- **supervision (โดย Roboflow):** ไลบรารีสำหรับจัดการและวาด Bounding Box (`sv.BoxAnnotator`, `sv.LabelAnnotator`) สไตล์โมเดิร์น
- **Flask:** สำหรับรัน Web Studio Server
- **Pillow & NumPy:** สำหรับจัดการไฟล์รูปภาพและการคำนวณทางคณิตศาสตร์

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```
propb/
├── app.py                  # Flask Web Server และ API Endpoints (/api/detect)
├── detector.py             # เอนจินตรวจจับ Zero-Shot รองรับ Transformers + Fallback Matcher
├── cli_demo.py             # สคริปต์รันตรวจจับวัตถุผ่าน Command Line แบบ Standalone
├── generate_samples.py     # สคริปต์สร้างรูปภาพตัวอย่างสำหรับทดสอบ
├── requirements.txt        # รายการแพ็กเกจที่จำเป็น
├── run.bat                 # สคริปต์คลิกเดียวรันโปรเจกต์บน Windows
├── static/
│   ├── index.html          # หน้าเว็บ Interactive Studio (Simulator, Playground, Code, Theory)
│   ├── style.css           # ธีมมืด (Dark UI) ตามสไตล์ในรูปภาพ
│   ├── app.js              # ลอจิกการทำงานของ Stepper, Heatmap และ Supervision Canvas
│   └── samples/            # รูปภาพตัวอย่าง (คนใส่เสื้อแดง, โต๊ะทำงาน, สุนัข)
└── README.md               # เอกสารคู่มือฉบับสมบูรณ์
```

---

## 🚀 วิธีติดตั้งและเริ่มใช้งาน

### 1. ติดตั้ง Dependencies
เปิด PowerShell หรือ Command Prompt ในโฟลเดอร์โปรเจกต์:
```powershell
pip install -r requirements.txt
```

### 2. รัน Web Studio
ดับเบิลคลิกไฟล์ `run.bat` หรือพิมพ์คำสั่ง:
```powershell
python app.py
```

เปิดเบราว์เซอร์ไปที่:
👉 **`http://127.0.0.1:5000`**

### ฟีเจอร์ใน Web Studio:
1. **🧩 จำลองสถาปัตยกรรม (Grounding DINO Simulator):** คลิกเลื่อนดู 4 สเต็ป (Input -> Extraction -> Fusion -> Output) พร้อมระบบ Interactive Cross-Attention Heatmap
2. **🎯 Zero-Shot Playground:** ทดสอบใส่ Text Prompt อิสระ, ปรับ Confidence Threshold และ NMS Slider, ดูพิกัด Bounding Box
3. **💻 โค้ดตัวอย่าง:** รวมโค้ด Python พร้อมใช้งาน กดคัดลอกได้ทันที
4. **📚 สรุปหลักการทำงาน:** ทฤษฎีเปรียบเทียบสถาปัตยกรรมแบบละเอียด

---

## 💻 การใช้งาน CLI Script

สามารถรันการตรวจจับผ่าน Terminal ได้ทันที:

```powershell
# รันกับรูปตัวอย่างมาตรฐาน
python cli_demo.py

# หรือระบุรูปภาพที่คุณต้องการ
python cli_demo.py path/to/your_image.jpg
```
ผลลัพธ์จะบันทึกเป็นรูปภาพที่มี Bounding Box ที่ `demo_output.jpg`

---

## 📝 ตัวอย่างโค้ดสั้น (Python)

```python
import torch
from PIL import Image
from transformers import OwlViTProcessor, OwlViTForObjectDetection
import supervision as sv

# 1. โหลดโมเดล
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "google/owlvit-base-patch32"
processor = OwlViTProcessor.from_pretrained(model_id)
model = OwlViTForObjectDetection.from_pretrained(model_id).to(device)

# 2. ป้อนรูปภาพและคำสั่ง Text Prompt
image = Image.open("static/samples/street_person.jpg")
queries = [["person wearing red shirt", "umbrella", "car"]]

# 3. รันโมเดล
inputs = processor(text=queries, images=image, return_tensors="pt").to(device)
with torch.no_grad():
    outputs = model(**inputs)

# 4. แปลงผลลัพธ์
target_sizes = torch.tensor([image.size[::-1]]).to(device)
results = processor.post_process_object_detection(
    outputs=outputs, target_sizes=target_sizes, threshold=0.25
)[0]

# 5. วาดด้วย Roboflow Supervision
detections = sv.Detections(
    xyxy=results["boxes"].cpu().numpy(),
    confidence=results["scores"].cpu().numpy(),
    class_id=results["labels"].cpu().numpy()
)

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

annotated_image = box_annotator.annotate(scene=image.copy(), detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image,
    detections=detections,
    labels=[queries[0][i] for i in results["labels"].cpu().numpy()]
)

annotated_image.save("result.jpg")
```
