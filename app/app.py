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
import os
from weather_service import WeatherService

# Import custom styling functions and helpers
from styles import inject_styles
from template import (
    AppConfig, ResultProcessor, StylingConfig, UIComponents, 
    MessageTemplates, Validators, SeverityCalculator, 
    CropWeatherRequirements, WeatherComparison
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
# SESSION STATE INITIALIZATION
# ==============================================
if "result" not in st.session_state:
    st.session_state.result = None
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None
if "selected_location" not in st.session_state:
    st.session_state.selected_location = "auto"
    
# ==============================================
# HIDE STREAMLIT UI ELEMENTS
# ==============================================
hide_streamlit_style = """
    <style>
    footer {visibility: hidden;}
    footer:after {content: ''; visibility: hidden;}
    .stApp > footer {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==============================================
# FORCE PERMANENT DARK MODE
# ==============================================
st.markdown("""
<head>
    <meta name="color-scheme" content="dark">
    <meta name="supported-color-schemes" content="dark">
    <meta name="darkreader-lock" content="yes">
    <meta name="theme-color" content="#060d10">
</head>
<style>
    :root, html, body, .stApp, [data-testid="stAppViewContainer"] {
        color-scheme: dark !important;
        forced-color-adjust: none !important;
        background-color: #060d10 !important;
        background: #060d10 !important;
    }
    
    *, *::before, *::after {
        color-scheme: dark !important;
        forced-color-adjust: none !important;
        -webkit-forced-color-adjust: none !important;
    }
    
    @media (prefers-color-scheme: light) {
        :root, html, body {
            color-scheme: dark !important;
            background-color: #060d10 !important;
        }
    }
</style>
<script>
    document.documentElement.style.colorScheme = 'dark';
    document.documentElement.style.backgroundColor = '#060d10';
    document.body.style.backgroundColor = '#060d10';
    
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

# Force remove Streamlit footer
st.markdown("""
<script>
    setTimeout(function() {
        var footers = document.querySelectorAll('footer');
        footers.forEach(function(footer) {
            footer.style.display = 'none';
            footer.style.visibility = 'hidden';
            footer.style.height = '0';
        });
    }, 100);
</script>
""", unsafe_allow_html=True)

# ==============================================
# DEBUG: DISCOVER MODEL CLASSES (Optional - can remove later)
# ==============================================
def discover_model_classes():
    """Discover what crops/diseases your model can detect"""
    try:
        import predict
        if hasattr(predict, 'model'):
            if hasattr(predict.model, 'class_to_idx'):
                classes = list(predict.model.class_to_idx.keys())
                return classes
                
        if os.path.exists('classes.txt'):
            with open('classes.txt', 'r') as f:
                classes = [line.strip() for line in f.readlines()]
            return classes
    except Exception as e:
        print(f"Could not discover classes: {e}")
    return None

# Optional debug info in sidebar
with st.sidebar:
    st.write("### Debug Info")
    model_classes = discover_model_classes()
    if model_classes:
        st.write(f"Model detects {len(model_classes)} classes")
        with st.expander("View all classes"):
            st.write(model_classes)
        
        unique_crops = set()
        for cls in model_classes:
            if '_' in cls:
                crop = cls.split('_')[0]
            elif ' ' in cls:
                crop = cls.split(' ')[0]
            else:
                crop = cls
            unique_crops.add(crop)
        
        st.write(f"### Unique Crops: {len(unique_crops)}")
        st.write(sorted(list(unique_crops)))

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

st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

# ==============================================
# TWO-COLUMN LAYOUT
# ==============================================
col_left, col_right = st.columns(
    [AppConfig.left_col_ratio, AppConfig.right_col_ratio], 
    gap="small"
)

# ==============================================
# LEFT COLUMN - IMAGE UPLOAD & WEATHER SECTION
# ==============================================
with col_left:
    # Image Analysis Section
    st.markdown(f'''
    <div class="ag-label" style="
        font-size: {StylingConfig.section_label_font_size};
        letter-spacing: {StylingConfig.section_label_letter_spacing};
        margin-bottom: {StylingConfig.section_label_margin_bottom};
        margin-top: {StylingConfig.section_label_margin_top};
        text-align: {StylingConfig.section_label_alignment};
        justify-content: {StylingConfig.section_label_alignment};
    ">Image Analysis</div>
    ''', unsafe_allow_html=True)
    
    uploaded = st.file_uploader(
        "Upload",
        type=AppConfig.allowed_formats,
        label_visibility="collapsed",
        key="image_uploader"
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
        </div>
        """, unsafe_allow_html=True)
    
    # Weather Location Section
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ag-label" style="font-size: 0.7rem;">Location for Weather</div>', unsafe_allow_html=True)
    
    col_loc1, col_loc2 = st.columns([3, 1])
    with col_loc1:
        location_input = st.text_input(
            "City or Pincode", 
            placeholder="e.g., Mumbai, 400001", 
            label_visibility="collapsed", 
            key="location_input"
        )
    with col_loc2:
        get_weather_btn = st.button("🌤️ Get Weather", key="get_weather_btn", use_container_width=True)
    
    # Fetch weather when requested
    if get_weather_btn and location_input:
        with st.spinner("Fetching weather data..."):
            if location_input.isdigit():
                weather = WeatherService.get_weather_by_pincode(location_input)
            else:
                weather = WeatherService.get_weather_by_city(location_input)
            st.session_state.weather_data = weather
            st.rerun()
    
    # Show weather status
    if st.session_state.weather_data:
        location_name = st.session_state.weather_data.get('location', 'Location')
        if location_name == "Unknown (using demo data)":
            location_name = location_input if location_input else "Demo Location"
        st.success(f"📍 {location_name} | {st.session_state.weather_data['temp']}°C, {st.session_state.weather_data['humidity']}% humidity")
    
    # Run Analysis Button
    run_analysis = st.button(
        "⬡ Run Analysis", 
        disabled=(uploaded is None), 
        use_container_width=True,
        key="run_analysis_btn"
    )

    if run_analysis and uploaded:
        st.session_state.result = None

        with st.spinner("Running model inference..."):
            time.sleep(0.5)

            # Real model prediction
            disease, confidence = predict_image(img)
            
            # Get remedy and AI advice
            remedy = get_remedy(disease)
            ai_advice = get_ai_advice(disease, confidence)

            # Process using template
            st.session_state.result = ResultProcessor.process_prediction(
                disease, confidence, remedy, ai_advice
            )
            st.rerun()
    
    # ==============================================
    # WEATHER CARD - Display after Run Analysis button
    # ==============================================
    # Add spacing
    st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True)
    
    # Display weather comparison card if conditions are met
    if st.session_state.weather_data and st.session_state.result:
        comparison = WeatherComparison.compare(
            actual_temp=st.session_state.weather_data['temp'],
            actual_humidity=st.session_state.weather_data['humidity'],
            crop_name=st.session_state.result["plant"]
        )
        UIComponents.render_weather_comparison_card(comparison)
    elif st.session_state.weather_data and not st.session_state.result:
        st.info("🌱 Upload an image and click 'Run Analysis' to see crop-specific weather advice")
    elif not st.session_state.weather_data:
        st.info("📍 Enter a location above and click 'Get Weather' to see crop suitability analysis")

# ==============================================
# RIGHT COLUMN - RESULTS DISPLAY
# ==============================================
with col_right:
    res = st.session_state.result
    
    if res:
        
        # Create two sub-columns for side-by-side layout
        col_disease, col_analysis = st.columns([0.5, 0.5], gap="small")
        
        # Card 1: Detected Disease (Left sub-column)
        with col_disease:
            UIComponents.render_disease_card(
                disease=res["disease"],
                plant=res["plant"],
                severity=res["severity"],
                is_healthy=res["healthy"],
                accent_color=res["accent_color"]
            )
        
        # Card 2: Combined Confidence + Insight Card (Right sub-column)
        with col_analysis:
            UIComponents.render_confidence_insight_card(
                confidence=res["confidence"],
                insight=res["insight"],
                accent_color=res["accent_color"]
            )
        
        # Card 3: Suggested Solution (Full width)
        UIComponents.render_solution_card(remedy=res["remedy"])
        
        # Card 4: AI Advisory (Full width)
        UIComponents.render_ai_card(ai_advice=res["ai_advice"])
    
    else:
        # Empty state for 4 cards
        empty_msgs = MessageTemplates.get_empty_state_messages()
        titles = MessageTemplates.get_card_titles()
        
        # Create two sub-columns for empty state
        col_disease, col_analysis = st.columns([0.5, 0.5], gap="small")
        
        with col_disease:
            UIComponents.render_empty_card(
                titles["disease"], "🔬", empty_msgs["disease"]
            )
        
        with col_analysis:
            UIComponents.render_empty_card(
                "Analysis Details", "📊", "Confidence score and insights will appear here..."
            )
        
        # Full width cards
        UIComponents.render_empty_card(
            titles["solution"], "🌱", empty_msgs["solution"]
        )
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