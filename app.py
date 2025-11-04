# ACNE LOCATION MASTER + FULL SKIN REPORT
import cv2
import numpy as np
import streamlit as st
from PIL import Image
import os

# Download face detector
cascade_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
cascade_path = "haarcascade_frontalface_default.xml"
if not os.path.exists(cascade_path):
    st.warning("Downloading face detector... (one-time)")
    import urllib.request
    urllib.request.urlretrieve(cascade_url, cascade_path)

st.title("Acne Location Master + Full Skin Report")
st.write("Upload selfie → **NUMBERED RED CIRCLES + CLICK TO ZOOM!**")

photo = st.file_uploader("Choose selfie", type=["jpg", "png"])

if photo:
    image = Image.open(photo)
    st.image(image, caption="Your Photo", width=300)
    
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # FACE DETECTION
    face_cascade = cv2.CascadeClassifier(cascade_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(150, 150))
    
    if len(faces) == 0:
        st.error("No face found! Use clear front-facing selfie.")
    else:
        x, y, w, h = max(faces, key=lambda r: r[2]*r[3])
        face = img[y:y+h, x:x+w]
        hsv = cv2.cvtColor(face, cv2.COLOR_BGR2HSV)
        
        # SKIN MASK
        skin_mask = cv2.inRange(hsv, (0, 20, 70), (20, 255, 255))
        eyes_lips = cv2.inRange(hsv, (0, 0, 0), (180, 255, 30)) + cv2.inRange(hsv, (0, 100, 100), (15, 255, 255))
        skin_mask = cv2.bitwise_and(skin_mask, skin_mask, mask=~eyes_lips)
        
        # ACNE DETECTION
        acne_red = cv2.inRange(hsv, (0, 70, 100), (10, 255, 255))
        acne_dark = cv2.inRange(hsv, (0, 0, 0), (180, 100, 100))
        acne_mask = cv2.bitwise_and(acne_red + acne_dark, acne_red + acne_dark, mask=skin_mask)
        kernel = np.ones((5,5), np.uint8)
        acne_mask = cv2.morphologyEx(acne_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # REAL PIMPLES
        contours, _ = cv2.findContours(acne_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        pimples = []
        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            if 200 < area < 3000:
                perimeter = cv2.arcLength(c, True)
                circularity = 4*np.pi*area/(perimeter**2) if perimeter > 0 else 0
                if circularity > 0.5:
                    (cx, cy), r = cv2.minEnclosingCircle(c)
                    pimples.append({
                        'id': i+1,
                        'center': (int(cx)+x, int(cy)+y),
                        'radius': int(r),
                        'area': int(area),
                        'location': '',
                        'crop': None
                    })
        
        # LOCATION NAMES
        face_center_y = y + h // 2
        face_center_x = x + w // 2
        for p in pimples:
            px, py = p['center']
            # Divide face into zones
            if py < y + h*0.35: 
                zone = "Forehead"
            elif py < y + h*0.6:
                if px < face_center_x: zone = "Left Cheek"
                else: zone = "Right Cheek"
            elif py < y + h*0.8:
                if px < face_center_x: zone = "Left Jaw"
                else: zone = "Right Jaw"
            else:
                zone = "Chin"
            p['location'] = zone
            
            # Crop close-up
            crop_size = p['radius'] * 4
            x1 = max(0, px - crop_size)
            y1 = max(0, py - crop_size)
            x2 = min(img.shape[1], px + crop_size)
            y2 = min(img.shape[0], py + crop_size)
            p['crop'] = img[y1:y2, x1:x2]
        
        # DRAW
        result = img.copy()
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 4)
        for p in pimples:
            cv2.circle(result, p['center'], p['radius'] + 10, (0, 0, 255), 5)
            cv2.putText(result, str(p['id']), (p['center'][0]-15, p['center'][1]+10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
        
        # DISPLAY
        st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), 
                 caption="NUMBERED ACNE (Click below to zoom)", width=500)
        
        if pimples:
            st.markdown("### Acne Locations (Click to Zoom)")
            cols = st.columns(3)
            for i, p in enumerate(pimples):
                with cols[i % 3]:
                    st.write(f"**Pimple #{p['id']}**")
                    st.write(f"**Location:** {p['location']}")
                    st.image(cv2.cvtColor(p['crop'], cv2.COLOR_BGR2RGB), width=150)
        else:
            st.success("**CLEAR SKIN! No acne found.**")
        
        # FULL SKIN REPORT
        st.markdown("---")
        st.subheader("Full Skin Report")
        mean_hsv = cv2.mean(hsv, mask=skin_mask)[:3]
        h_val, s, v = mean_hsv
        
        color_type = ["Very Fair", "Fair", "Medium", "Olive/Tan", "Brown", "Deep Brown"][int(v//40)]
        undertone = "Warm (Golden)" if h_val < 15 else "Cool (Pink)"
        genes = "Northern Europe" if v > 200 else "Mediterranean" if v > 160 else "South Asia/Latin" if v > 120 else "Africa/Caribbean" if v > 80 else "East Asia"
        skin_type = "Oily" if np.var(hsv[:,:,2][skin_mask>0]) > 800 else "Combination" if np.var(hsv[:,:,2][skin_mask>0]) > 400 else "Dry/Normal"
        smoothness = max(0, min(100, 100 - np.var(cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)[skin_mask>0]) / 150))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Color Type", color_type)
            st.metric("Undertone", undertone)
        with col2:
            st.metric("Likely Genes", genes)
            st.metric("Skin Type", skin_type)
        with col3:
            st.metric("Smoothness", f"{smoothness:.0f}/100")
            st.metric("Acne Count", len(pimples))