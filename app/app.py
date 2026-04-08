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
    MessageTemplates, Validators
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
        disease_content = UIComponents.render_disease_card(
            res["disease"], res["plant"], 
            res["severity"], res["healthy"]
        )
        UIComponents.render_result_card(
            title=MessageTemplates.get_card_titles()["disease"],
            icon="🔬",
            content_html=disease_content,
            accent_color=res["accent_color"]
        )
        
        # Card 2: Confidence Score
        conf_content = UIComponents.render_confidence_card(res["confidence"])
        UIComponents.render_result_card(
            title=MessageTemplates.get_card_titles()["confidence"],
            icon="📊",
            content_html=conf_content,
            accent_color=res["accent_color"]
        )
        
        # Card 3: System Insight
        UIComponents.render_result_card(
            title=MessageTemplates.get_card_titles()["insight"],
            icon="🧬",
            content_html=f'<p class="ag-insight">{res["insight"]}</p>',
            accent_color=res["accent_color"]
        )
        
        # Card 4: Suggested Solution
        UIComponents.render_result_card(
            title=MessageTemplates.get_card_titles()["solution"],
            icon="🌱",
            content_html=f'<p class="ag-remedy">{res["remedy"]}</p>',
            accent_color="#2ef2e2"
        )
        
        # Card 5: AI Advisory
        UIComponents.render_result_card(
            title=MessageTemplates.get_card_titles()["ai_advisor"],
            icon="🤖",
            content_html=f'<p class="ag-remedy">{res["ai_advice"]}</p>',
            accent_color="#A4F000"
        )
    
    else:
        # Empty state
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

# ==============================================
# FOOTER
# ==============================================
st.markdown(f"""
<div class="ag-footer">
    {AppConfig.name} {AppConfig.version} • Powered by <span class="hl">PyTorch</span> • Advanced Computer Vision
</div>
""", unsafe_allow_html=True)