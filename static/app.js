// Application State
let currentImage = new Image();
let currentDetections = [];
let highlightedIndex = -1;
let currentSampleKey = "food";
let currentModelMode = "zero_shot"; // 'zero_shot' | 'custom'
let trainPollInterval = null;

// Presets configuration
const presets = {
  avengers: {
    src: "/static/samples/avengers.jpg",
    prompt: "กัปตันอเมริกา, ไอรอนแมน, ธอร์, แบล็ควิโดว์",
    domain: "popculture"
  },
  batman: {
    src: "/static/samples/batman_dc.jpg",
    prompt: "แบทแมน",
    domain: "popculture"
  },
  superman: {
    src: "/static/samples/superman_dc.jpg",
    prompt: "ซูเปอร์แมน",
    domain: "popculture"
  },
  dc: {
    src: "/static/samples/dc_heroes.jpg",
    prompt: "ซูเปอร์แมน, แบทแมน, วันเดอร์วูแมน",
    domain: "popculture"
  },
  salmon: {
    src: "/static/samples/salmon_dish.jpg",
    prompt: "ปลา, ข้าวโพด, จาน",
    domain: "food"
  },
  food: {
    src: "/static/samples/thai_food.jpg",
    prompt: "ไข่ดาว, ข้าว, จาน",
    domain: "food"
  },
  fashion: {
    src: "/static/samples/fashion.jpg",
    prompt: "คน, เสื้อ, กางเกง, รองเท้า",
    domain: "fashion"
  },
  traffic: {
    src: "/static/samples/traffic.jpg",
    prompt: "รถยนต์, คน",
    domain: "traffic"
  },
  street: {
    src: "/static/samples/street_person.jpg",
    prompt: "คน, ผู้หญิง, ใบหน้า, รองเท้า",
    domain: "fashion"
  },
  workspace: {
    src: "/static/samples/workspace.jpg",
    prompt: "แล็ปท็อป, แก้วกาแฟ, เก้าอี้",
    domain: "workspace"
  },
  dog: {
    src: "/static/samples/dog_park.jpg",
    prompt: "สุนัข, หญ้า",
    domain: "animals"
  },
  cat: {
    src: "/static/samples/cat_pet.jpg",
    prompt: "แมว",
    domain: "animals"
  }
};

// Domain Quick Tags
const domainTags = {
  food: ["ปลา", "แซลมอน", "ข้าวโพด", "ไข่ดาว", "ข้าว", "กะเพรา", "หมูกรอบ", "พริก", "จาน", "ช้อน", "แก้วน้ำ"],
  fashion: ["คน", "เสื้อ", "เสื้อสีแดง", "กางเกง", "รองเท้า", "หมวก", "แว่นตา", "กระเป๋า"],
  traffic: ["รถยนต์", "รถเก๋ง", "มอเตอร์ไซค์", "จักรยาน", "คน", "ไฟจราจร", "ป้ายจราจร"],
  workspace: ["แล็ปท็อป", "แก้วกาแฟ", "จอ", "เมาส์", "คีย์บอร์ด", "เก้าอี้", "โต๊ะ", "สมุด"],
  animals: ["สุนัข", "แมว", "นก", "หญ้า", "สนามหญ้า", "ต้นไม้", "ลูกบอล"],
  popculture: ["กัปตันอเมริกา", "ไอรอนแมน", "ธอร์", "แบล็ควิโดว์", "แบทแมน", "ซูเปอร์แมน", "วันเดอร์วูแมน", "เดอะแฟลช", "อะควาแมน", "โจ๊กเกอร์", "ฮาร์ลีย์ ควินน์", "สพันจ์บ็อบ", "แพทริก", "โล่", "ธนู", "การ์ตูน", "คน"]
};

document.addEventListener("DOMContentLoaded", () => {
  setupUpload();
  setupSlider();
  setupPaste();
  selectDomain("food");
  checkModelStatus();
});

// Setup File Upload & Drag-and-Drop
function setupUpload() {
  const fileInput = document.getElementById("fileInput");
  const dropZone = document.getElementById("dropZone");

  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) handleImageFile(file);
  });

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageFile(e.dataTransfer.files[0]);
    }
  });
}

// Setup Paste (Ctrl+V) from clipboard
function setupPaste() {
  window.addEventListener("paste", (e) => {
    const items = (e.clipboardData || e.originalEvent.clipboardData).items;
    for (const item of items) {
      if (item.type.indexOf("image") === 0) {
        const file = item.getAsFile();
        handleImageFile(file);
        break;
      }
    }
  });
}

function handleImageFile(file) {
  const reader = new FileReader();
  reader.onload = (event) => {
    currentSampleKey = "custom";
    document.querySelectorAll(".sample-thumb").forEach(t => t.classList.remove("active"));
    
    currentImage.onload = () => {
      currentDetections = [];
      drawCanvas();
      updateStatus("รูปภาพพร้อมแล้ว", "var(--success)");
    };
    currentImage.src = event.target.result;
  };
  reader.readAsDataURL(file);
}

// Setup Confidence Slider
function setupSlider() {
  const slider = document.getElementById("confSlider");
  const display = document.getElementById("confDisplay");

  slider.addEventListener("input", (e) => {
    const val = parseFloat(e.target.value);
    display.textContent = `${Math.round(val * 100)}%`;
    drawCanvas();
  });
}

// Domain Selection
function selectDomain(domainKey) {
  // Update Tab Styling
  const tabs = document.querySelectorAll(".domain-tab");
  tabs.forEach(t => t.classList.remove("active"));
  const clickedTab = Array.from(tabs).find(t => t.getAttribute("onclick")?.includes(domainKey));
  if (clickedTab) clickedTab.classList.add("active");

  // Render Domain Quick Tags
  const tagsContainer = document.getElementById("quickTags");
  const tags = domainTags[domainKey] || domainTags.food;
  tagsContainer.innerHTML = tags.map(tag => `
    <span class="quick-tag" onclick="appendTag('${tag}')">+ ${tag}</span>
  `).join("");

  // Only load preset sample image if user hasn't uploaded their own custom image
  if (currentSampleKey !== "custom") {
    const domainToSample = {
      popculture: "avengers",
      food: "salmon",
      fashion: "fashion",
      traffic: "traffic",
      workspace: "workspace",
      animals: "dog"
    };

    const sampleKey = domainToSample[domainKey] || "avengers";
    loadSamplePreset(sampleKey, false);
  }
}

// Load Preset Sample
function loadSamplePreset(key, switchDomainTab = true) {
  currentSampleKey = key;
  const p = presets[key];
  if (!p) return;

  document.querySelectorAll(".sample-thumb").forEach(t => t.classList.remove("active"));
  const activeThumb = document.getElementById(`thumb-${key}`);
  if (activeThumb) activeThumb.classList.add("active");

  if (switchDomainTab && p.domain) {
    const tabs = document.querySelectorAll(".domain-tab");
    tabs.forEach(t => t.classList.remove("active"));
    const tab = Array.from(tabs).find(t => t.getAttribute("onclick")?.includes(p.domain));
    if (tab) tab.classList.add("active");

    const tagsContainer = document.getElementById("quickTags");
    const tags = domainTags[p.domain] || domainTags.food;
    tagsContainer.innerHTML = tags.map(tag => `
      <span class="quick-tag" onclick="appendTag('${tag}')">+ ${tag}</span>
    `).join("");
  }

  const promptInput = document.getElementById("promptInput");
  if (promptInput) promptInput.value = p.prompt;

  currentImage.onload = () => {
    currentDetections = [];
    drawCanvas();
    updateStatus("รูปภาพพร้อมแล้ว", "var(--success)");
  };
  currentImage.src = p.src;
}

// Quick Tag click helper
function appendTag(tagText) {
  const input = document.getElementById("promptInput");
  if (!input) return;
  const current = input.value.trim();
  if (!current) {
    input.value = tagText;
  } else {
    // Avoid duplicate
    const items = current.split(",").map(i => i.trim());
    if (!items.includes(tagText)) {
      input.value = `${current}, ${tagText}`;
    }
  }
}

// Switch Model Mode
function switchModelMode(mode) {
  currentModelMode = mode;
  const zeroBtn = document.getElementById("modeZeroShotBtn");
  const customBtn = document.getElementById("modeCustomBtn");
  const modelBadge = document.getElementById("activeModelBadge");

  if (mode === "zero_shot") {
    zeroBtn.classList.add("active");
    customBtn.classList.remove("active");
    modelBadge.textContent = "⚡ Zero-Shot YOLO-World";
    modelBadge.style.color = "var(--success)";
    modelBadge.style.borderColor = "var(--success)";
  } else {
    zeroBtn.classList.remove("active");
    customBtn.classList.add("active");
    modelBadge.textContent = "🏆 Fine-Tuned Model (best.pt)";
    modelBadge.style.color = "#a855f7";
    modelBadge.style.borderColor = "#a855f7";
  }
}

// Check Backend Model Status
async function checkModelStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    if (data.has_custom_weights) {
      document.getElementById("modeCustomBtn").title = "โมเดลที่ผ่านการเทรนพร้อมใช้งาน";
    }
  } catch (e) {
    console.error("Status check error:", e);
  }
}

// Start Object Detection
async function startDetection() {
  const promptInput = document.getElementById("promptInput");
  const detectBtn = document.getElementById("detectBtn");
  const confSlider = document.getElementById("confSlider");
  const promptText = promptInput.value.trim();

  if (!promptText && currentModelMode === "zero_shot") {
    alert("กรุณาพิมพ์สิ่งของที่ต้องการค้นหาก่อนครับ เช่น ไข่ดาว, ข้าว หรือ คน, รถยนต์");
    promptInput.focus();
    return;
  }

  if (!currentImage.src) {
    alert("กรุณาเลือกหรืออัปโหลดรูปภาพก่อนครับ");
    return;
  }

  // Set Loading UI
  detectBtn.disabled = true;
  detectBtn.innerHTML = `<span class="spinner"></span> กำลังวิเคราะห์และตีกรอบวัตถุ...`;
  updateStatus("AI กำลังประมวลผล...", "#60a5fa");

  const startTime = performance.now();
  const confThresh = parseFloat(confSlider.value);

  try {
    const res = await fetch("/api/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        image_src: currentImage.src,
        prompt: promptText,
        conf_thresh: confThresh,
        sample_key: currentSampleKey,
        model_mode: currentModelMode
      })
    });

    const data = await res.json();
    currentDetections = data.detections || [];
    const duration = Math.round(performance.now() - startTime);

    document.getElementById("latencyDisplay").textContent = `~${data.latency_ms || duration} ms`;
    updateStatus("ตรวจจับสำเร็จ", "var(--success)");
  } catch (err) {
    console.error("Detection error:", err);
    updateStatus("เกิดข้อผิดพลาดในการเชื่อมต่อ", "#ef4444");
  } finally {
    detectBtn.disabled = false;
    detectBtn.innerHTML = `<i class="fa-solid fa-bolt"></i> ค้นหาและตีกรอบวัตถุ (Detect Objects)`;
    drawCanvas();
  }
}

function setConfidence(val) {
  const slider = document.getElementById("confSlider");
  const display = document.getElementById("confDisplay");
  if (slider) slider.value = val;
  if (display) display.textContent = `${Math.round(val * 100)}%`;

  document.querySelectorAll(".quick-conf-btn").forEach(b => b.classList.remove("active"));
  if (val <= 0.18) document.getElementById("btnConf15")?.classList.add("active");
  else if (val <= 0.35) document.getElementById("btnConf25")?.classList.add("active");
  else document.getElementById("btnConf50")?.classList.add("active");

  drawCanvas();
}

// Draw Canvas with Ultra-Clear, High-Contrast Viewfinder Styling
function drawCanvas() {
  const canvas = document.getElementById("resultCanvas");
  if (!canvas || !currentImage.complete || currentImage.naturalWidth === 0) return;

  const ctx = canvas.getContext("2d");
  canvas.width = currentImage.naturalWidth;
  canvas.height = currentImage.naturalHeight;

  // 1. Draw base image
  ctx.drawImage(currentImage, 0, 0, canvas.width, canvas.height);

  const confThresh = parseFloat(document.getElementById("confSlider").value);
  const activeBoxes = currentDetections.filter(d => d.score >= confThresh);

  // Update Count
  document.getElementById("foundCount").textContent = `${activeBoxes.length} รายการ`;

  // Scale factor based on resolution so line is never too thin on large images
  const scale = Math.max(1, Math.min(canvas.width, canvas.height) / 520);
  const baseStroke = (scale * 3.8);

  // 2. Draw Ultra-Clear Bounding Boxes
  activeBoxes.forEach((item, idx) => {
    const [x1, y1, x2, y2] = item.box;
    const w = x2 - x1;
    const h = y2 - y1;
    const isHighlighted = (idx === highlightedIndex);
    const color = item.color || "#2563eb";
    const strokeW = isHighlighted ? (baseStroke * 1.5) : baseStroke;

    // A. Semi-transparent highlight fill
    ctx.fillStyle = hexToRgba(color, isHighlighted ? 0.38 : 0.16);
    ctx.fillRect(x1, y1, w, h);

    // B. Outer Dark Shadow Contour (prevents blending into bright backgrounds)
    ctx.shadowBlur = 0;
    ctx.lineWidth = strokeW + (2.5 * scale);
    ctx.strokeStyle = "rgba(0, 0, 0, 0.95)";
    ctx.strokeRect(x1, y1, w, h);

    // C. Main Vibrant Neon Stroke with Glow
    ctx.shadowColor = color;
    ctx.shadowBlur = (isHighlighted ? 18 : 10) * scale;
    ctx.lineWidth = strokeW;
    ctx.strokeStyle = color;
    ctx.strokeRect(x1, y1, w, h);
    ctx.shadowBlur = 0; // reset

    // D. Viewfinder Corner Bracket Accents (Ultra-sharp corners)
    const cornerLen = Math.min(w * 0.22, h * 0.22, 26 * scale);
    const cornerW = strokeW + (1.8 * scale);
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = cornerW;
    ctx.lineCap = "round";

    // Top-Left corner
    ctx.beginPath();
    ctx.moveTo(x1, y1 + cornerLen);
    ctx.lineTo(x1, y1);
    ctx.lineTo(x1 + cornerLen, y1);
    ctx.stroke();

    // Top-Right corner
    ctx.beginPath();
    ctx.moveTo(x2 - cornerLen, y1);
    ctx.lineTo(x2, y1);
    ctx.lineTo(x2, y1 + cornerLen);
    ctx.stroke();

    // Bottom-Left corner
    ctx.beginPath();
    ctx.moveTo(x1, y2 - cornerLen);
    ctx.lineTo(x1, y2);
    ctx.lineTo(x1 + cornerLen, y2);
    ctx.stroke();

    // Bottom-Right corner
    ctx.beginPath();
    ctx.moveTo(x2 - cornerLen, y2);
    ctx.lineTo(x2, y2);
    ctx.lineTo(x2, y2 - cornerLen);
    ctx.stroke();

    // E. High-Contrast Pill Badge
    const labelText = `${item.label} ${Math.round(item.score * 100)}%`;
    const fontSize = Math.round(15 * Math.max(1, scale * 0.88));
    ctx.font = `bold ${fontSize}px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`;
    const textMetrics = ctx.measureText(labelText);
    const textWidth = textMetrics.width;
    const badgeW = textWidth + (18 * scale);
    const badgeH = Math.round(26 * scale);
    const badgeY = Math.max(2, y1 - badgeH - (4 * scale));

    // Badge Dark Drop Shadow
    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
    ctx.beginPath();
    ctx.roundRect(x1 + 1, badgeY + 2, badgeW, badgeH, 6 * scale);
    ctx.fill();

    // Solid Badge Background
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x1, badgeY, badgeW, badgeH, 6 * scale);
    ctx.fill();

    // Badge White Border for separation
    ctx.lineWidth = Math.max(1, 1.4 * scale);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.9)";
    ctx.stroke();

    // Badge Text with dark text shadow
    ctx.fillStyle = "#ffffff";
    ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
    ctx.shadowBlur = 4;
    ctx.shadowOffsetX = 1;
    ctx.shadowOffsetY = 1;
    ctx.fillText(labelText, x1 + (9 * scale), badgeY + (fontSize * 1.15));
    ctx.shadowBlur = 0; // reset
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;
  });

  // Render bottom list
  renderDetectionsList(activeBoxes);
}

// Render Results Table
function renderDetectionsList(boxes) {
  const container = document.getElementById("detectionsList");
  if (!container) return;

  if (boxes.length === 0) {
    container.innerHTML = `
      <div style="color:var(--text-dim); font-size:0.85rem; padding:1rem; text-align:center;">
        ไม่พบวัตถุที่ตรงกับคำสั่ง หรือลองปรับลดแถบ "ระดับความมั่นใจ (Confidence)" ด้านซ้าย
      </div>
    `;
    return;
  }

  container.innerHTML = boxes.map((item, idx) => {
    const [x1, y1, x2, y2] = item.box;
    const w = x2 - x1;
    const h = y2 - y1;

    return `
      <div class="detection-pill" onmouseenter="highlightBox(${idx})" onmouseleave="unhighlightBox()">
        <div class="pill-info">
          <div class="pill-color-dot" style="background-color:${item.color};"></div>
          <div>
            <strong style="color:#fff;">${item.label}</strong>
            <span style="color:#60a5fa; font-weight:700; margin-left:0.35rem;">${Math.round(item.score * 100)}%</span>
          </div>
        </div>
        <div class="pill-coords">
          [x: ${x1}, y: ${y1}, w: ${w}, h: ${h}]
        </div>
      </div>
    `;
  }).join("");
}

function highlightBox(index) {
  highlightedIndex = index;
  drawCanvas();
}

function unhighlightBox() {
  highlightedIndex = -1;
  drawCanvas();
}

function updateStatus(text, color) {
  const badge = document.getElementById("activeModelBadge");
  if (!badge) return;
  // Keep model label unless error
  if (color === "#ef4444") {
    badge.textContent = text;
    badge.style.color = color;
  }
}

// Download Annotated Canvas
function downloadImage() {
  const canvas = document.getElementById("resultCanvas");
  if (!canvas) return;

  const link = document.createElement("a");
  link.download = "zero_shot_detected_result.jpg";
  link.href = canvas.toDataURL("image/jpeg", 0.95);
  link.click();
}

// ==========================================================
// Training Studio Modal Controls
// ==========================================================
function openTrainingModal() {
  const modal = document.getElementById("trainingModal");
  if (modal) modal.classList.add("active");
  fetchTrainingStatus();
}

function closeTrainingModal() {
  const modal = document.getElementById("trainingModal");
  if (modal) modal.classList.remove("active");
}

async function triggerTraining() {
  const sourceDir = document.getElementById("trainSourceDir").value.trim();
  const classesStr = document.getElementById("trainClasses").value.trim();
  const epochs = parseInt(document.getElementById("trainEpochs").value) || 3;
  const startBtn = document.getElementById("startTrainBtn");

  startBtn.disabled = true;
  startBtn.innerHTML = `<span class="spinner"></span> กำลังรันกระบวนการ...`;

  try {
    const res = await fetch("/api/train/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source_dir: sourceDir,
        classes: classesStr,
        epochs: epochs
      })
    });
    const data = await res.json();
    if (data.success) {
      if (trainPollInterval) clearInterval(trainPollInterval);
      trainPollInterval = setInterval(fetchTrainingStatus, 1500);
    } else {
      alert(data.message || "ไม่สามารถเริ่มการเทรนได้");
      startBtn.disabled = false;
      startBtn.innerHTML = `<i class="fa-solid fa-rocket"></i> เริ่มสร้างชุดข้อมูลและเทรนโมเดล`;
    }
  } catch (e) {
    console.error("Training trigger error:", e);
    startBtn.disabled = false;
    startBtn.innerHTML = `<i class="fa-solid fa-rocket"></i> เริ่มสร้างชุดข้อมูลและเทรนโมเดล`;
  }
}

async function fetchTrainingStatus() {
  try {
    const res = await fetch("/api/train/status");
    const data = await res.json();

    const statusLabel = document.getElementById("trainStatusLabel");
    const progressLabel = document.getElementById("trainProgressLabel");
    const progressFill = document.getElementById("trainProgressFill");
    const logTerminal = document.getElementById("trainLogTerminal");
    const startBtn = document.getElementById("startTrainBtn");

    if (data.status === "labeling") {
      statusLabel.textContent = `สถานะ: กำลัง Auto-Labeling ด้วย Zero-Shot...`;
      statusLabel.style.color = "#f59e0b";
      startBtn.disabled = true;
    } else if (data.status === "training") {
      statusLabel.textContent = `สถานะ: กำลัง Fine-Tuning โครงข่ายประสาทเทียม...`;
      statusLabel.style.color = "#a855f7";
      startBtn.disabled = true;
    } else if (data.status === "finished") {
      statusLabel.textContent = `สถานะ: ✅ การเทรนเสร็จสมบูรณ์! บันทึกโมเดลแล้ว`;
      statusLabel.style.color = "var(--success)";
      startBtn.disabled = false;
      startBtn.innerHTML = `<i class="fa-solid fa-check"></i> เทรนเรียบร้อยแล้ว (เทรนใหม่อีกครั้ง)`;
      if (trainPollInterval) clearInterval(trainPollInterval);
      // Auto switch to custom model
      switchModelMode("custom");
    } else if (data.status === "error") {
      statusLabel.textContent = `สถานะ: ❌ เกิดข้อผิดพลาด (${data.error_message})`;
      statusLabel.style.color = "#ef4444";
      startBtn.disabled = false;
      startBtn.innerHTML = `<i class="fa-solid fa-rocket"></i> ลองใหม่อีกครั้ง`;
      if (trainPollInterval) clearInterval(trainPollInterval);
    }

    progressLabel.textContent = `${data.progress || 0}%`;
    progressFill.style.width = `${data.progress || 0}%`;

    if (data.logs && data.logs.length > 0) {
      logTerminal.textContent = data.logs.join("\n");
      logTerminal.scrollTop = logTerminal.scrollHeight;
    }
  } catch (e) {
    console.error("Fetch training status error:", e);
  }
}

function copyCliCommand() {
  const text = document.getElementById("cliSnippet").textContent;
  navigator.clipboard.writeText(text).then(() => {
    alert("คัดลอกคำสั่ง Terminal สำเร็จแล้ว!");
  });
}

// Helper: Hex to RGBA
function hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16) || 37;
  const g = parseInt(hex.slice(3, 5), 16) || 99;
  const b = parseInt(hex.slice(5, 7), 16) || 235;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}
