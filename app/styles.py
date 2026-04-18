# styles.py — AgroScan AI Custom Styling Module
# ==============================================
# Contains all custom CSS styling for the AgroScan application
# Uses centralized config for colors and fonts

import streamlit as st
from config import AppColors, AppFonts

# Build CSS from config
CSS_CONTENT = f"""

/* ============================================
   FORCE DARK MODE - PREVENT BROWSER OVERRIDE
   ============================================ */
:root {{
    color-scheme: dark !important;
    forced-color-adjust: none !important;
    background-color: {AppColors.BG_ROOT} !important;
}}

html, body, .stApp, [data-testid="stAppViewContainer"] {{
    background-color: {AppColors.BG_ROOT} !important;
    color-scheme: dark !important;
}}

/* Force all text to remain visible */
.ag-title, .ag-subtitle, .ag-label, .ag-disease, .ag-insight, .ag-remedy {{
    color-scheme: dark !important;
}}

/* ============================================
   COLOR VARIABLES
   ============================================ */
:root {{
    --lime: {AppColors.LIME};
    --teal: {AppColors.TEAL};
    --warn: {AppColors.WARN};
    --danger: {AppColors.DANGER};
    --ok: {AppColors.OK};
    --bg-root: {AppColors.BG_ROOT};
    --border: {AppColors.BORDER};
    --border-hi: {AppColors.BORDER_HI};
    --mid: {AppColors.MID};
    --dim: {AppColors.DIM};
    --white: {AppColors.WHITE};
    --fD: '{AppFonts.PRIMARY}', monospace;
    --fB: '{AppFonts.SECONDARY}', sans-serif;
    --fM: '{AppFonts.MONO}', monospace;
}}

/* ============================================
   TEXT READABILITY ENHANCEMENTS
   ============================================ */
body, .stMarkdown, p, div {{
    font-size: 1rem !important;
    line-height: 1.6 !important;
    letter-spacing: 0.3px !important;
}}

.ag-disease, .ag-disease-ok {{
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    text-shadow: 0 0 12px rgba(164,240,0,0.4) !important;
}}

.ag-insight {{
    font-size: 0.95rem !important;
    line-height: 1.8 !important;
    color: #d8ece4 !important;
    font-weight: 400 !important;
}}

.ag-remedy {{
    font-size: 0.95rem !important;
    line-height: 1.8 !important;
    color: #d8ece4 !important;
    background: rgba(46,242,226,0.06) !important;
}}

.ag-label {{
    font-size: 0.7rem !important;
    letter-spacing: 5px !important;
    font-weight: 600 !important;
}}

.ag-card-hdr {{
    font-size: 0.65rem !important;
    letter-spacing: 4px !important;
    font-weight: 600 !important;
    color: {AppColors.LIME} !important;
}}

.ag-conf-pct {{
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
}}

.ag-plant {{
    font-size: 0.8rem !important;
    letter-spacing: 3px !important;
    font-weight: 500 !important;
    color: #7ec8e0 !important;
}}

.ag-empty {{
    font-size: 0.9rem !important;
    font-style: normal !important;
    color: #7a9a8a !important;
}}

.ag-badge {{
    font-size: 0.65rem !important;
    letter-spacing: 2.5px !important;
    font-weight: 600 !important;
}}

/* Text shadows for better visibility */
.ag-disease {{
    text-shadow: 0 0 15px rgba(164,240,0,0.5),
                 0 0 5px rgba(164,240,0,0.3) !important;
    font-weight: 800 !important;
}}

.ag-disease-ok {{
    text-shadow: 0 0 15px rgba(94,250,94,0.5) !important;
}}

.ag-insight {{
    text-shadow: 0 1px 2px rgba(0,0,0,0.5) !important;
}}

.ag-conf-pct {{
    text-shadow: 0 0 8px rgba(164,240,0,0.3) !important;
    font-weight: 800 !important;
}}

/* ============================================
   GLOBAL RESET & LAYOUT
   ============================================ */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html, body {{
    margin: 0 !important;
    padding: 0 !important;
    height: 100% !important;
}}

.stApp {{
    margin-top: -44px !important;
    padding-top: 0 !important;
}}

[data-testid="stAppViewContainer"] {{
    margin-top: -44px !important;
    padding-top: 44px !important;
    min-height: 100vh !important;
}}

[data-testid="stAppViewContainer"] > section {{
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
}}

[data-testid="stMainBlockContainer"], 
[data-testid="block-container"],
.block-container {{
    padding: 0 !important;
    margin: 0 !important;
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
}}

/* ============================================
   HIDE STREAMLIT UI ELEMENTS
   ============================================ */
[data-testid="stHeader"], [data-testid="stToolbar"], 
[data-testid="stDecoration"], [data-testid="stStatusWidget"], footer {{
    display: none !important;
}}

/* ============================================
   COLUMN LAYOUT STYLES
   ============================================ */
[data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 5px !important;
    align-items: stretch !important;
    flex: 1 !important;
    min-height: 0 !important;
}}

[data-testid="column"] {{
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;
    min-width: 0 !important;
    min-height: 0 !important;
}}

/* Left column styling */
[data-testid="column"]:first-child {{
    flex: 0 0 calc(42% - 2px) !important;
    max-width: calc(42% - 2px) !important;
    background: rgba(10, 24, 32, 0.65) !important;
    backdrop-filter: blur(12px) !important;
    border-right: none !important;
    border-radius: 0 8px 8px 0 !important;
}}

/* Right column styling */
[data-testid="column"]:last-child {{
    flex: 0 0 calc(58% - 2px) !important;
    max-width: calc(58% - 2px) !important;
    background: rgba(8, 15, 23, 0.55) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 8px 0 0 8px !important;
}}

/* Column content containers */
[data-testid="column"] [data-testid="stVerticalBlock"] {{
    flex: 1 !important;
    padding: 24px 20px !important;
    min-height: 0 !important;
    overflow-y: visible !important;
}}

/* Left column content spacing */
[data-testid="column"]:first-child [data-testid="stVerticalBlock"] {{
    gap: 16px !important;
}}

/* Right column content spacing */
[data-testid="column"]:last-child [data-testid="stVerticalBlock"] {{
    gap: 8px !important;
    padding: 24px 20px 24px 20px !important;
    min-height: 0 !important;
    overflow-y: visible !important;
}}

/* ============================================
   HEADER STYLES
   ============================================ */
.ag-header {{
    position: relative;
    z-index: 10;
    background: linear-gradient(135deg, rgba(10,24,32,0.97) 0%, rgba(6,35,28,0.95) 55%, rgba(4,20,20,0.97) 100%);
    border-bottom: 1px solid var(--border-hi);
    padding: 24px 40px 18px;
    text-align: center;
    margin-top: 0 !important;
    flex-shrink: 0;
}}

.ag-header::after {{
    content: '';
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(90deg, transparent, rgba(164,240,0,0.06), transparent);
    will-change: transform;  
    transform: translateZ(0);
}}

.ag-logo-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
}}

.ag-logo-leaf {{
    font-size: 2.3rem;
    filter: drop-shadow(0 0 10px rgba(164,240,0,0.7));
    animation: leaf-pulse 2s ease-in-out infinite;
}}

@keyframes leaf-pulse {{
    0%, 100% {{ filter: drop-shadow(0 0 10px rgba(164,240,0,0.7)); }}
    50% {{ filter: drop-shadow(0 0 22px rgba(164,240,0,1.0)); }}
}}

.ag-title {{
    font-family: var(--fD) !important;
    font-size: 2.3rem !important;
    font-weight: 700 !important;
    color: var(--lime) !important;
    letter-spacing: 3px !important;
    text-shadow: 0 0 26px rgba(164,240,0,0.5) !important;
}}

.ag-subtitle {{
    font-family: var(--fM) !important;
    font-size: 0.66rem !important;
    letter-spacing: 5px !important;
    color: var(--teal) !important;
    text-transform: uppercase !important;
    margin-top: 7px !important;
}}

/* Section label with dot indicator */
.ag-label {{
    font-family: var(--fM);
    color: var(--lime);
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
    position: relative;
}}

.ag-label::before {{
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    border: 1.5px solid var(--lime);
    border-radius: 50%;
    box-shadow: 0 0 6px var(--lime);
}}

/* ============================================
   FILE UPLOADER STYLES
   ============================================ */
[data-testid="stFileUploader"] > label {{
    display: none !important;
}}

[data-testid="stFileUploader"] section {{
    border: 1.5px dashed rgba(164,240,0,0.4) !important;
    border-radius: 14px !important;
    background: rgba(164,240,0,0.12) !important;
    backdrop-filter: blur(4px);
    padding: 28px 16px !important;
    transition: all 0.3s ease !important;
}}

[data-testid="stFileUploader"] section:hover {{
    border-color: var(--lime) !important;
    background: rgba(164,240,0,0.2) !important;
}}

[data-testid="stFileUploaderDropzoneInstructions"] > div > span {{
    font-family: var(--fB) !important;
    font-size: 0.95rem !important;
    color: var(--white) !important;
    font-weight: 600 !important;
}}

[data-testid="stFileUploaderDropzoneInstructions"] > div > small {{
    font-family: var(--fM) !important;
    font-size: 0.64rem !important;
    color: var(--mid) !important;
}}

[data-testid="stFileUploader"] button {{
    background: rgba(164,240,0,0.15) !important;
    border: 1px solid rgba(164,240,0,0.5) !important;
    color: var(--lime) !important;
    font-family: var(--fB) !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 6px 18px !important;
}}

/* ============================================
   IMAGE PREVIEW STYLES
   ============================================ */
.ag-img-frame {{
    border: 1px solid var(--border-hi);
    border-radius: 14px;
    overflow: hidden;
    background: rgba(0,0,0,0.5);
    position: relative;
    margin-bottom: 16px;
}}

.ag-img-frame img {{
    width: 100%;
    max-height: 300px;
    object-fit: contain;
}}

.ag-img-badge {{
    position: absolute;
    top: 9px;
    left: 9px;
    background: rgba(6,13,16,0.82);
    border: 1px solid var(--border-hi);
    border-radius: 5px;
    padding: 3px 10px;
    font-family: var(--fM);
    font-size: 0.57rem;
    color: var(--teal);
}}

.ag-file-meta {{
    display: flex;
    justify-content: space-between;
    padding: 6px 12px;
    background: rgba(0,0,0,0.45);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-top: 8px;
}}

.ag-file-name {{
    font-family: var(--fM);
    font-size: 0.68rem;
    color: var(--lime);
}}

.ag-file-size {{
    font-family: var(--fM);
    font-size: 0.62rem;
    color: var(--mid);
}}

/* ============================================
   BUTTON STYLES
   ============================================ */
.stButton > button {{
    width: 100% !important;
    background: linear-gradient(135deg, #173d20 0%, #0c2714 100%) !important;
    border: 1.5px solid var(--lime) !important;
    color: var(--lime) !important;
    font-family: var(--fD) !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 14px 20px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin-top: 16px !important;
}}

.stButton > button:hover:not(:disabled) {{
    background: linear-gradient(135deg, #1f5a2c 0%, #133420 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 0 34px rgba(164,240,0,0.34) !important;
}}

/* ============================================
   CARD STYLES
   ============================================ */
.ag-card {{
    background: rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(4px);
    border-bottom: 1px solid rgba(164, 240, 0, 0.1);
    border-radius: 12px;
    margin-bottom: 12px;
    padding: 18px 4px 18px 18px;
    position: relative;
    transition: all 0.3s ease;
}}

.ag-card:hover {{
    background: rgba(0, 0, 0, 0.35);
    border-bottom-color: rgba(164, 240, 0, 0.3);
}}

/* Left accent line for cards */
.ag-card::before {{
    content: '';
    position: absolute;
    left: 0;
    top: 16px;
    bottom: 16px;
    width: 3px;
    border-radius: 2px;
    background: var(--card-accent, var(--lime));
    box-shadow: 0 0 8px var(--card-accent, var(--lime));
}}

.ag-card-hdr {{
    font-family: var(--fM);
    font-size: 0.59rem;
    letter-spacing: 3px;
    color: var(--mid);
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}}

.ag-icon {{
    font-size: 0.95rem;
}}

/* Empty state text */
.ag-empty {{
    font-family: var(--fB);
    font-size: 0.80rem;
    color: var(--dim);
    font-style: italic;
}}

/* Disease name styles */
.ag-disease {{
    font-family: var(--fD);
    font-size: 1.28rem;
    font-weight: 700;
    color: var(--lime);
    text-shadow: 0 0 14px rgba(164,240,0,0.35);
    margin-bottom: 4px;
}}

.ag-disease-ok {{
    font-family: var(--fD);
    font-size: 1.28rem;
    font-weight: 700;
    color: var(--ok);
    text-shadow: 0 0 14px rgba(94,250,94,0.4);
    margin-bottom: 4px;
}}

.ag-plant {{
    font-family: var(--fM);
    font-size: 0.66rem;
    letter-spacing: 2px;
    color: var(--teal);
    margin-bottom: 8px;
}}

/* Severity badge styles */
.ag-badge {{
    display: inline-block;
    padding: 2px 12px;
    border-radius: 20px;
    font-family: var(--fM);
    font-size: 0.57rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    border: 1px solid;
}}

.b-none {{ color: var(--ok); border-color: var(--ok); background: rgba(94,250,94,0.08); }}
.b-low {{ color: var(--lime); border-color: var(--lime); background: rgba(164,240,0,0.08); }}
.b-medium {{ color: var(--warn); border-color: var(--warn); background: rgba(255,179,71,0.08); }}
.b-high {{ color: var(--danger); border-color: var(--danger); background: rgba(255,92,106,0.08); }}

/* Confidence score styles */
.ag-conf-row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 8px;
}}

.ag-conf-lbl {{
    font-family: var(--fB);
    font-size: 0.80rem;
    color: var(--mid);
}}

.ag-conf-pct {{
    font-family: var(--fD);
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--lime);
}}

/* Progress bar styles */
.ag-bar-track {{
    height: 7px;
    background: rgba(20, 48, 63, 0.5);
    border-radius: 99px;
    overflow: hidden;
}}

.ag-bar-fill {{
    height: 100%;
    border-radius: 99px;
}}

/* Insight and remedy text */
.ag-insight, .ag-remedy {{
    font-family: var(--fB);
    font-size: 0.83rem;
    color: rgba(232,244,240,0.72);
    line-height: 1.7;
}}

.ag-remedy {{
    padding: 10px 14px;
    background: rgba(46,242,226,0.04);
    border: 1px solid rgba(46,242,226,0.12);
    border-radius: 8px;
}}

/* ============================================
   FOOTER STYLES
   ============================================ */
.ag-footer {{
    background: rgba(10, 24, 32, 0.95);
    backdrop-filter: blur(8px);
    border-top: 1px solid var(--border);
    padding: 12px 40px;
    text-align: center;
    font-family: var(--fM);
    font-size: 0.57rem;
    color: var(--dim);
    position: relative;
    z-index: 100;
    margin-top: 20px;
    margin-bottom: 0;
    width: 100%;
    box-sizing: border-box;
}}

.ag-footer .hl {{ color: var(--teal); }}

/* ============================================
   SCROLLBAR STYLES
   ============================================ */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: var(--bg-root); }}
::-webkit-scrollbar-thumb {{ background: var(--border-hi); border-radius: 99px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--lime); }}

/* ============================================
   UTILITY CLASSES
   ============================================ */
html, body, .stApp {{
    background-color: {AppColors.BG_ROOT} !important;
    margin: 0 !important;
    padding: 0 !important;
}}

body::after, .stApp::after {{
    display: none !important;
    content: none !important;
}}

.block-container {{
    padding-bottom: 0 !important;
    margin-bottom: 0 !important;
}}

.stVerticalBlock {{
    gap: 0 !important;
}}

.ag-footer {{
    margin-bottom: 0 !important;
    margin-top: 20px !important;
    position: relative;
    bottom: 0;
    left: 0;
    right: 0;
}}

.main > div {{
    padding-bottom: 0 !important;
}}

[data-testid="stAppViewContainer"] {{
    padding-bottom: 0 !important;
}}

body {{
    background-color: {AppColors.BG_ROOT} !important;
    min-height: 100vh;
}}

.stApp {{
    background-color: {AppColors.BG_ROOT} !important;
    min-height: 100vh;
}}

/* ============================================
   WEATHER WIDGET SPECIFIC STYLES
   ============================================ */
div[data-testid="stTextInput"] input {{
    width: 100px !important;
    min-width: 80px !important;
    padding: 5px 8px !important;
    font-size: 0.8rem !important;
}}

div[data-testid="stButton"] button {{
    padding: 10px 8px !important;
    min-width: 50px !important;
    margin-top: -20px !important;
}}

/* ============================================
   UTILITY SPACING CLASSES
   ============================================ */
.ag-spacer-xs {{ height: 5px; }}
.ag-spacer-sm {{ height: 15px; }}
.ag-spacer-md {{ height: 25px; }}
.ag-spacer-lg {{ height: 40px; }}
.ag-spacer-xl {{ height: 60px; }}

/* ============================================
   WEATHER WIDGET COLORS (from config)
   ============================================ */
.ag-temp-high {{ color: {AppColors.TEMP_HIGH}; }}
.ag-temp-low {{ color: {AppColors.TEMP_LOW}; }}
.ag-temp-ideal {{ color: {AppColors.TEMP_IDEAL}; }}
.ag-humidity-high {{ color: {AppColors.HUMIDITY_HIGH}; }}
.ag-humidity-low {{ color: {AppColors.HUMIDITY_LOW}; }}
.ag-humidity-ideal {{ color: {AppColors.HUMIDITY_IDEAL}; }}

/* ============================================
   TEXT COLORS
   ============================================ */
.ag-text-lime {{ color: {AppColors.LIME}; }}
.ag-text-teal {{ color: {AppColors.TEAL}; }}
.ag-text-white {{ color: {AppColors.WHITE}; }}
.ag-text-mid {{ color: {AppColors.MID}; }}
.ag-text-dim {{ color: {AppColors.DIM}; }}

/* ============================================
   HEADER STYLES FOR WEATHER WIDGET
   ============================================ */
.ag-weather-header {{
    color: #7ec8e0;
    font-size: 0.85rem;
    letter-spacing: 1px;
}}
"""


def inject_styles():
    """Inject all custom styles into the Streamlit app"""
    font_link = f'<link href="{AppFonts.URL}" rel="stylesheet">'
    style_tag = f"<style>{CSS_CONTENT}</style>"
    st.markdown(font_link, unsafe_allow_html=True)
    st.markdown(style_tag, unsafe_allow_html=True)


def bar_gradient(pct: int) -> str:
    """
    Return gradient color based on confidence percentage
    Uses centralized color configuration
    """
    from config import AppColors
    
    if pct >= 80:
        return f"linear-gradient(90deg,{AppColors.PROGRESS_HIGH[0]},{AppColors.PROGRESS_HIGH[1]})"
    if pct >= 55:
        return f"linear-gradient(90deg,{AppColors.PROGRESS_MEDIUM[0]},{AppColors.PROGRESS_MEDIUM[1]})"
    return f"linear-gradient(90deg,{AppColors.PROGRESS_LOW[0]},{AppColors.PROGRESS_LOW[1]})"


def badge_cls(severity: str) -> str:
    """Return CSS class for severity badge"""
    return {
        "none": "b-none",
        "low": "b-low",
        "medium": "b-medium",
        "high": "b-high",
    }.get(severity, "b-low")


def card_accent(severity: str, healthy: bool) -> str:
    """Return accent color based on disease severity"""
    from config import AppColors
    
    if healthy:
        return AppColors.CARD_ACCENT_HEALTHY
    return {
        "low": AppColors.CARD_ACCENT_LOW,
        "medium": AppColors.CARD_ACCENT_MEDIUM,
        "high": AppColors.CARD_ACCENT_HIGH,
    }.get(severity, AppColors.CARD_ACCENT_LOW)