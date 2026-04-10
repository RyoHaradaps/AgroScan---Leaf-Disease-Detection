# app.py — AgroScan AI Main Application (Refactored with template.py)
# ======================================
# Main Streamlit application for leaf disease detection.
# Handles UI layout, image upload, analysis processing, and result display.
# ======================================

import streamlit as st
from PIL import Image
import time
import base64
from io import BytesIO
from predict import predict_image
from remedies import get_remedy
from ai_advisor import get_ai_advice

# Import custom styling functions and helpers
from styles import inject_styles
from template import (
    AppConfig, ResultProcessor, UIComponents, 
    MessageTemplates, Validators, SeverityCalculator
)

# ==============================================
# PAGE CONFIGURATION
# ==============================================
st.set_page_config(
    page_title=AppConfig.name,
    page_icon=AppConfig.icon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================
# FORCE PERMANENT DARK MODE - ULTRA STRONG VERSION
# ==============================================
st.markdown("""
<head>
    <meta name="color-scheme" content="dark">
    <meta name="supported-color-schemes" content="dark">
    <meta name="darkreader-lock" content="yes">
    <meta name="theme-color" content="#060d10">
</head>
<style>
    /* ULTRA AGGRESSIVE DARK MODE FORCE */
    :root, html, body, .stApp, [data-testid="stAppViewContainer"] {
        color-scheme: dark !important;
        forced-color-adjust: none !important;
        background-color: #060d10 !important;
        background: #060d10 !important;
    }
    
    /* Force ALL elements to stay dark */
    *, *::before, *::after {
        color-scheme: dark !important;
        forced-color-adjust: none !important;
        -webkit-forced-color-adjust: none !important;
    }
    
    /* Prevent any light mode injection */
    @media (prefers-color-scheme: light) {
        :root, html, body {
            color-scheme: dark !important;
            background-color: #060d10 !important;
        }
    }
</style>
<script>
    // Force dark mode via JavaScript (most reliable)
    document.documentElement.style.colorScheme = 'dark';
    document.documentElement.style.backgroundColor = '#060d10';
    document.body.style.backgroundColor = '#060d10';
    
    // Monitor for any changes and reapply
    const observer = new MutationObserver(function() {
        document.documentElement.style.colorScheme = 'dark';
        document.documentElement.style.backgroundColor = '#060d10';
        document.body.style.backgroundColor = '#060d10';
    });
    observer.observe(document.body, { attributes: true, childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# ==============================================
# STYLE INJECTION
# ==============================================
inject_styles()

# ==============================================
# SESSION STATE INITIALIZATION
# ==============================================
if "result" not in st.session_state:
    st.session_state.result = None

# ==============================================
# HEADER SECTION
# ==============================================
st.markdown(f"""
<div class="ag-header">
    <div class="ag-logo-row">
        <span class="ag-logo-leaf">{AppConfig.icon}</span>
        <span class="ag-title">{AppConfig.name}</span>
    </div>
    <div class="ag-subtitle">{AppConfig.tagline}</div>
</div>
""", unsafe_allow_html=True)

# ==============================================
# TWO-COLUMN LAYOUT
# ==============================================
col_left, col_right = st.columns(
    [AppConfig.left_col_ratio, AppConfig.right_col_ratio], 
    gap="small"
)

# ==============================================
# LEFT COLUMN - IMAGE UPLOAD SECTION
# ==============================================
with col_left:
    st.markdown('<div class="ag-label">Image Analysis</div>', unsafe_allow_html=True)
    
    uploaded = st.file_uploader(
        "Upload",
        type=AppConfig.allowed_formats,
        label_visibility="collapsed"
    )
    
    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        
        uploaded.seek(0)
        size_kb = len(uploaded.read()) / 1024
        size_str = f"{round(size_kb, 1)} KB" if size_kb < 1024 else f"{round(size_kb / 1024, 2)} MB"
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        
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
    
    run = st.button("⬡ Run Analysis", disabled=(uploaded is None), use_container_width=True)

    if run and uploaded:
        st.session_state.result = None

        with st.spinner("Running model inference..."):
            time.sleep(1.5)

            # Real model prediction
            disease, confidence = predict_image(img)
            
            # Get remedy and AI advice
            remedy = get_remedy(disease)
            ai_advice = get_ai_advice(disease, confidence)

            # Process using template (centralized logic)
            st.session_state.result = ResultProcessor.process_prediction(
                disease, confidence, remedy, ai_advice
            )

# ==============================================
# RIGHT COLUMN - RESULTS DISPLAY
# ==============================================
with col_right:
    res = st.session_state.result
    
    if res:
        # Card 1: Detected Disease
        UIComponents.render_disease_card(
            disease=res["disease"],
            plant=res["plant"],
            severity=res["severity"],
            is_healthy=res["healthy"],
            accent_color=res["accent_color"]
        )
        
        # Card 2: Confidence Score
        UIComponents.render_confidence_card(
            confidence=res["confidence"],
            accent_color=res["accent_color"]
        )
        
        # Card 3: System Insight
        UIComponents.render_insight_card(
            insight=res["insight"],
            accent_color=res["accent_color"]
        )
        
        # Card 4: Suggested Solution
        UIComponents.render_solution_card(remedy=res["remedy"])
        
        # Card 5: AI Advisory
        UIComponents.render_ai_card(ai_advice=res["ai_advice"])
    
    else:
        # Empty state for all 5 cards
        empty_msgs = MessageTemplates.get_empty_state_messages()
        titles = MessageTemplates.get_card_titles()
        
        UIComponents.render_empty_card(
            titles["disease"], "🔬", empty_msgs["disease"]
        )
        UIComponents.render_empty_card(
            titles["confidence"], "📊", empty_msgs["confidence"]
        )
        UIComponents.render_empty_card(
            titles["insight"], "🧬", empty_msgs["insight"]
        )
        UIComponents.render_empty_card(
            titles["solution"], "🌱", empty_msgs["solution"]
        )
        # Note: Empty state for AI Advisory (Card 5)
        UIComponents.render_empty_card(
            titles["ai_advisor"], "🤖", "AI advice will appear here..."
        )

# ==============================================
# FOOTER
# ==============================================
st.markdown(f"""
<div class="ag-footer">
    {AppConfig.name} {AppConfig.version} • Powered by <span class="hl">PyTorch</span> • Advanced Computer Vision
</div>
""", unsafe_allow_html=True)