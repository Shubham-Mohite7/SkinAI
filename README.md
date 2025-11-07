# SkinAI – AI-Powered Skin & Acne Analyzer  
**Live Demo**: [https://acnemodel.streamlit.app](https://acnemodel.streamlit.app)   

---

## Overview  
**SkinAI** is a **real-time facial skin analysis tool** that detects:  
- **Acne (pimples, blackheads, whiteheads)**  
- **Skin tone & undertone**  
- **Likely ancestral origin (continent genes)**  
- **Skin type (Oily / Dry / Combo)**  
- **Smoothness score (0–100)**  

It uses **computer vision + color science** to give **instant dermatology-level insights** from a selfie.

---

## Features  

| Feature | Description |
|-------|-----------|
| **Face Detection** | Auto-detects face using OpenCV Haar Cascade |
| **Acne Detection** | Finds red, white, blackheads with **numbered red circles** |
| **Location Mapping** | Labels acne as: Forehead, Left/Right Cheek, Chin, Jaw |
| **Skin Tone Analysis** | Classifies: Very Fair → Deep Brown |
| **Undertone** | Warm (Golden) vs Cool (Pink) |
| **Genetic Origin (Approx)** | Europe, Mediterranean, South Asia, Africa, East Asia |
| **Skin Type** | Oily / Combination / Dry based on brightness variance |
| **Smoothness Score** | Texture analysis (0–100) |
| **Zoomable Acne Crops** | Click each pimple to see close-up |
| **Web App (Streamlit)** | Upload selfie → Instant report |

---

## Tech Stack  

| Layer | Technology | Version / Notes |
|------|-----------|----------------|
| **Frontend / UI** | [Streamlit](https://streamlit.io) | `1.30+` – Interactive web app |
| **Backend / Logic** | Python | `3.11` |
| **Computer Vision** | [OpenCV](https://opencv.org) | `opencv-python-headless` (cloud-safe) |
| **Image Processing** | NumPy, PIL (Pillow) | Core array & image handling |
| **Color Analysis** | HSV & Lab color spaces | For tone, acne, texture |
| **Face Detection** | Haar Cascade (`haarcascade_frontalface_default.xml`) | Auto-downloaded |
| **Deployment** | [Streamlit Community Cloud](https://streamlit.io/cloud) | Free, auto-deploy from GitHub |
| **Version Control** | Git + GitHub | `git` |
| **Package Management** | `requirements.txt` | Cloud dependency install |
| **Local Dev** | Conda (Miniconda) | `skinai` environment |

---

## Project Structure  

```
SkinAI/
│
├── app.py                  # Main Streamlit app (all logic)
├── requirements.txt        # Cloud dependencies
├── haarcascade_frontalface_default.xml  # Auto-downloaded
├── README.md               # This file
└── .git/                   # Git repo
```

---

## How It Works (Technical Flow)

1. **Upload Selfie** → PIL → NumPy array → OpenCV (BGR)
2. **Face Detection** → Haar Cascade → Crop face ROI
3. **Skin Mask** → HSV range → Remove eyes/lips (anti-mask)
4. **Acne Detection**:
   - Red inflamed: High saturation + value
   - Dark scars: Low value
   - Shape filter: Circularity > 0.5
5. **Color Analysis** → Mean HSV in skin mask
6. **Texture** → Variance in grayscale → Smoothness score
7. **Output** → Streamlit UI with images, metrics, zoomable crops

---

## Local Setup (Mac / Linux / Windows)

```bash
# 1. Clone repo
git clone https://github.com/yourusername/SkinAI.git
cd SkinAI

# 2. Create conda env
conda create -n skinai python=3.11 -y
conda activate skinai

# 3. Install deps
pip install -r requirements.txt

# 4. Run locally
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) → Upload selfie → See results!

---

## Deploy to Streamlit Cloud (Free)

1. Push to GitHub  
2. Go to [share.streamlit.io](https://share.streamlit.io)  
3. New App → Link your repo → `app.py` → Deploy!  
4. Done in 60 seconds!

---

## Screenshots  

| Screenshot | Description |
|----------|-----------|
| ![Main UI](https://via.placeholder.com/600x400?text=SkinAI+Main+Screen) | Upload + Face + Acne Circles |
| ![Report](https://via.placeholder.com/600x300?text=Skin+Report) | Color, Genes, Type, Smoothness |


---

## Limitations & Future Ideas  

| Current Limit | Future Upgrade |
|--------------|----------------|
| Lighting-sensitive | Add auto-light correction |
| Single face only | Multi-face support |
| No age/gender | Add CNN models (MediaPipe) |
| No history | Add user login + save reports |
| No PDF export | Add "Download Report" button |

---

## Author  

**Shubham**  
- GitHub: 

> "Turning selfies into skin science — one pimple at a time."

---

## Star This Project!  
If you like it, give it a **star** on GitHub!  
Help others find this AI dermatology tool.

---

**SkinAI — Because your skin deserves AI.**
