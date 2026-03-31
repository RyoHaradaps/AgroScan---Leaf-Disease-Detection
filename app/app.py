# app.py — AgroScan AI Main Application
# ======================================
# Main Streamlit application for leaf disease detection.
# Handles UI layout, image upload, analysis processing, and result display.
# ======================================

import streamlit as st
from PIL import Image
import random
import time
import base64
from io import BytesIO

# Import custom styling functions and helpers
from styles import inject_styles, bar_gradient, badge_cls, card_accent

# ==============================================
# PAGE CONFIGURATION
# ==============================================
# Must be the first Streamlit command - sets browser tab title, icon, and layout
st.set_page_config(
    page_title="AgroScan AI",           # Browser tab title
    page_icon="🌿",                     # Browser tab icon
    layout="wide",                      # Use full-width layout
    initial_sidebar_state="collapsed",  # Hide sidebar by default
)

# ==============================================
# STYLE INJECTION
# ==============================================
# Apply all custom CSS, fonts, and background animations
inject_styles()

# ==============================================
# DISEASE DATABASE
# ==============================================
# Mock database of diseases with insights and treatment solutions
# In production, this would come from a real database or API
DISEASE_DB = {
    "Apple Scab": {
        "insight": "Apple Scab is a fungal disease caused by Venturia inaequalis. It appears as olive-green to black spots on leaves and fruits.",
        "solution": "Apply fungicides like captan or sulfur. Remove and destroy infected fallen leaves."
    },
    "Late Blight": {
        "insight": "Late blight is caused by Phytophthora infestans. It causes dark, water-soaked lesions on leaves.",
        "solution": "Apply copper-based fungicides preventively. Remove infected plants immediately."
    },
    "Powdery Mildew": {
        "insight": "Powdery mildew appears as white, powdery fungal growth on leaf surfaces.",
        "solution": "Apply sulfur or neem oil-based fungicides. Ensure adequate spacing for air flow."
    },
    "Healthy Leaf": {
        "insight": "Your leaf appears healthy with no visible signs of disease.",
        "solution": "Continue regular monitoring and maintain good agricultural practices."
    }
}

# ==============================================
# SESSION STATE INITIALIZATION
# ==============================================
# Session state persists across reruns, storing analysis results
if "result" not in st.session_state:
    st.session_state.result = None  # Will store detection results when available

# ==============================================
# HEADER SECTION
# ==============================================
# Main title area with logo, title, and subtitle
st.markdown("""
<div class="ag-header">
    <div class="ag-logo-row">
        <span class="ag-logo-leaf">🌿</span>
        <span class="ag-title">AgroScan AI</span>
    </div>
    <div class="ag-subtitle">Smart Leaf Disease Detection System</div>
</div>
""", unsafe_allow_html=True)

# ==============================================
# TWO-COLUMN LAYOUT
# ==============================================
# Left column: Image upload and analysis controls
# Right column: Results display (disease, confidence, insights, solutions)
col_left, col_right = st.columns([0.42, 0.58], gap="small")

# ==============================================
# LEFT COLUMN - IMAGE UPLOAD SECTION
# ==============================================
with col_left:
    # Section label
    st.markdown('<div class="ag-label">Image Analysis</div>', unsafe_allow_html=True)
    
    # File uploader widget - accepts JPG, JPEG, PNG
    uploaded = st.file_uploader(
        "Upload",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    # If an image has been uploaded, display preview and metadata
    if uploaded:
        # Open and convert image to RGB
        img = Image.open(uploaded).convert("RGB")
        
        # Reset file pointer and calculate file size
        uploaded.seek(0)
        size_kb = len(uploaded.read()) / 1024
        size_str = f"{round(size_kb, 1)} KB" if size_kb < 1024 else f"{round(size_kb / 1024, 2)} MB"
        
        # Convert image to base64 for inline HTML display
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Display image preview with badge and metadata
        st.markdown(f"""
        <div class="ag-img-frame">
            <img src="data:image/png;base64,{img_b64}" alt="leaf">
            <div class="ag-img-badge">● LIVE ANALYSIS</div>
        </div>
        <div class="ag-file-meta">
            <span class="ag-file-name">📄 {uploaded.name}</span>
            <span class="ag-file-size">{size_str}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Analyze button - disabled when no image uploaded
    run = st.button("⬡ Run Analysis", disabled=(uploaded is None), use_container_width=True)

# ==============================================
# ANALYSIS PROCESSING
# ==============================================
# Triggered when "Run Analysis" button is clicked and image exists
if run and uploaded:
    # Clear previous results
    st.session_state.result = None
    
    # Show spinner during processing
    with st.spinner("Running model inference..."):
        # Simulate processing delay (replace with actual ML inference)
        time.sleep(1.5)
        
        # Mock prediction - randomly select disease and confidence
        # In production, replace with actual model prediction
        diseases = list(DISEASE_DB.keys())
        disease = random.choice(diseases)
        confidence = random.randint(75, 98)
        healthy = disease == "Healthy Leaf"
        
        # Store results in session state
        st.session_state.result = {
            "disease": disease,                              # Detected disease name
            "confidence": confidence,                        # Confidence percentage
            "healthy": healthy,                              # Boolean for healthy leaf
            "severity": "none" if healthy else "low",        # Severity level
            "plant": "Tomato",                               # Plant type (hardcoded for demo)
            "insight": DISEASE_DB[disease]["insight"],       # Disease insight
            "remedy": DISEASE_DB[disease]["solution"]        # Treatment solution
        }

# ==============================================
# RIGHT COLUMN - RESULTS DISPLAY
# ==============================================
with col_right:
    # Retrieve results from session state
    res = st.session_state.result
    
    # ==========================================
    # CASE 1: Results Available
    # ==========================================
    if res:
        # Get accent color based on severity (for left border)
        ac = card_accent(res["severity"], res["healthy"])
        
        # --- Card 1: Detected Disease ---
        if res["healthy"]:
            # Healthy leaf display
            disease_html = f'<div class="ag-disease-ok">✓ {res["disease"]}</div><div class="ag-plant">{res["plant"]}</div><span class="ag-badge b-none">● No Disease Detected</span>'
        else:
            # Diseased leaf display with severity badge
            disease_html = f'<div class="ag-disease">{res["disease"]}</div><div class="ag-plant">{res["plant"]}</div><span class="ag-badge {badge_cls(res["severity"])}">● Severity: {res["severity"].upper()}</span>'
        
        st.markdown(f'<div class="ag-card" style="--card-accent:{ac};"><div class="ag-card-hdr"><span class="ag-icon">🔬</span>Detected Disease</div>{disease_html}</div>', unsafe_allow_html=True)
        
        # --- Card 2: Confidence Score ---
        # Get gradient color based on confidence percentage
        grad = bar_gradient(res["confidence"])
        conf_html = f'<div class="ag-conf-row"><span class="ag-conf-lbl">Model Certainty</span><span class="ag-conf-pct">{res["confidence"]}%</span></div><div class="ag-bar-track"><div class="ag-bar-fill" style="width:{res["confidence"]}%;background:{grad};"></div></div>'
        st.markdown(f'<div class="ag-card" style="--card-accent:{ac};"><div class="ag-card-hdr"><span class="ag-icon">📊</span>Confidence Score</div>{conf_html}</div>', unsafe_allow_html=True)
        
        # --- Card 3: System Insight ---
        st.markdown(f'<div class="ag-card" style="--card-accent:{ac};"><div class="ag-card-hdr"><span class="ag-icon">🧬</span>System Insight</div><p class="ag-insight">{res["insight"]}</p></div>', unsafe_allow_html=True)
        
        # --- Card 4: Suggested Solution ---
        # Teal accent for solution card
        st.markdown(f'<div class="ag-card" style="--card-accent:#2ef2e2;"><div class="ag-card-hdr"><span class="ag-icon">🌱</span>Suggested Solution</div><p class="ag-remedy">{res["remedy"]}</p></div>', unsafe_allow_html=True)
    
    # ==========================================
    # CASE 2: No Results Yet (Empty State)
    # ==========================================
    else:
        # Display placeholder cards with instructions
        st.markdown('<div class="ag-card"><div class="ag-card-hdr"><span class="ag-icon">🔬</span>Detected Disease</div><p class="ag-empty">Upload an image to begin analysis...</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="ag-card"><div class="ag-card-hdr"><span class="ag-icon">📊</span>Confidence Score</div><p class="ag-empty">Awaiting prediction results...</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="ag-card"><div class="ag-card-hdr"><span class="ag-icon">🧬</span>System Insight</div><p class="ag-empty">AI insights will appear here...</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="ag-card" style="--card-accent:#2ef2e2;"><div class="ag-card-hdr"><span class="ag-icon">🌱</span>Suggested Solution</div><p class="ag-empty">Treatment recommendations will appear here...</p></div>', unsafe_allow_html=True)

# ==============================================
# FOOTER
# ==============================================
# App footer with version info and technology credits
st.markdown("""
<div class="ag-footer">
    AgroScan AI v1.0 • Powered by <span class="hl">PyTorch</span> • Advanced Computer Vision
</div>
""", unsafe_allow_html=True)