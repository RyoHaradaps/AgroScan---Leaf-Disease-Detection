# template.py — Centralized Configuration & Reusable Components
# ==============================================================
# This file contains all configuration, business logic, and UI components
# for the AgroScan AI application. All styling is centrally controlled
# through the StylingConfig class for easy maintenance.

from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import streamlit as st

# ==============================================
# APP CONFIGURATION
# ==============================================

@dataclass(frozen=True)
class AppConfig:
    """Central app configuration - Change app-wide settings here"""
    name: str = "AgroScan AI"
    version: str = "v1.0"
    tagline: str = "Smart Leaf Disease Detection System"
    icon: str = "🌿"
    
    # Layout ratios (left column: image upload, right column: results)
    left_col_ratio: float = 0.42
    right_col_ratio: float = 0.58
    
    # File upload settings
    allowed_formats: Tuple[str, ...] = ("jpg", "jpeg", "png")
    max_file_size_mb: int = 10


@dataclass(frozen=True)
class StylingConfig:
    """Centralized styling configuration - Change all card styles here"""
    
    # ===== SECTION LABEL STYLES (Image Analysis heading) =====
    section_label_font_size: str = "0.7rem"
    section_label_letter_spacing: str = "4px"
    section_label_margin_bottom: str = "20px"
    section_label_margin_top: str = "20px"
    section_label_alignment: str = "left"  # left, center, right
    
    # ===== CARD HEADER STYLES (Controls ALL card titles: Detected Disease, Analysis Details, etc.) =====
    card_header_font_size: str = "1.5rem"      # Card title font size (0.6rem - 1rem)
    card_header_letter_spacing: str = "4px"     # Card title letter spacing
    card_header_font_family: str = "Montserrat"   # Font family for headers
    card_header_font_weight: str = "900"        # Card title boldness (400-900)
    card_header_text_transform: str = "uppercase"  # uppercase/lowercase/capitalize
    card_icon_size: str = "1.1rem"              # Card icon size (🔬, 📊, 🌱, 🤖)
    
    # ===== DISEASE CARD STYLES =====
    disease_font_size: str = "1.6rem"           # Disease name font size
    disease_font_weight: str = "800"            # Disease name boldness
    disease_margin_bottom: str = "14px"         # Space below disease name
    
    plant_font_size: str = "0.85rem"            # Plant name font size
    plant_letter_spacing: str = "2px"           # Plant name letter spacing
    plant_margin_bottom: str = "20px"           # Space below plant name
    plant_color: str = "#7ec8e0"                # Plant name color
    
    badge_font_size: str = "0.7rem"             # Severity badge font size
    badge_padding: str = "4px 14px"             # Badge padding (top/bottom left/right)
    
    # ===== ANALYSIS CARD STYLES =====
    confidence_label_size: str = "0.9rem"       # "Model Certainty" text size
    confidence_label_spacing: str = "2px"       # Label letter spacing
    confidence_percent_size: str = "1.8rem"     # Percentage number size
    confidence_percent_weight: str = "800"      # Percentage boldness
    
    progress_bar_height: str = "8px"            # Height of confidence bar
    progress_bar_margin_bottom: str = "28px"    # Space below progress bar
    
    insight_font_size: str = "0.9rem"           # Insight text size
    insight_line_height: str = "1.7"            # Insight line height (1.5-2.0)
    
    # ===== CARD SPACING =====
    card_content_margin_bottom: str = "20px"    # Bottom margin for card content
    divider_margin_top: str = "8px"             # Space above divider line
    divider_padding_top: str = "18px"           # Space above insight text
    divider_border_width: str = "1px"           # Divider line thickness
    
    # ===== SOLUTION & AI CARDS =====
    remedy_font_size: str = "0.95rem"           # Remedy/AI text size
    remedy_line_height: str = "1.8"             # Remedy/AI line height
    remedy_padding: str = "10px 14px"           # Remedy text padding


@dataclass(frozen=True)
class Thresholds:
    """Confidence and severity thresholds"""
    high_confidence: int = 85      # Above this = low severity
    medium_confidence: int = 60    # 60-85% = medium severity
    low_confidence: int = 0        # Below 60% = high severity
    healthy_keywords: Tuple[str, ...] = ("Healthy", "health", "good condition")


@dataclass(frozen=True)
class UIColors:
    """Centralized color scheme - Change all colors here"""
    lime: str = "#a4f000"          # Primary accent color
    teal: str = "#2ef2e2"          # Secondary accent color
    warn: str = "#ffb347"          # Warning color (medium severity)
    danger: str = "#ff5c6a"        # Danger color (high severity)
    ok: str = "#5efa5e"            # Success color (healthy)
    bg_root: str = "#060d10"       # Background color
    border: str = "#14303f"        # Border color
    border_hi: str = "#1d4a5c"     # Highlight border
    mid: str = "#4a8a7a"           # Mid-tone text
    dim: str = "#1e4a3a"           # Dim text
    white: str = "#e8f4f0"         # White text


# ==============================================
# TEXT FORMATTING UTILITIES
# ==============================================

class TextFormatter:
    """Text formatting utilities for cleaning up model outputs"""
    
    @staticmethod
    def format_disease_name(disease: str) -> str:
        """Convert 'Potato_Late_blight' to 'Potato Late Blight'"""
        formatted = disease.replace("_", " ")
        formatted = " ".join(formatted.split())
        words = formatted.split()
        formatted_words = []
        for word in words:
            if word.isupper():
                formatted_words.append(word)
            else:
                formatted_words.append(word.capitalize())
        return " ".join(formatted_words)
    
    @staticmethod
    def extract_plant_name(disease: str) -> str:
        """Extract plant name from disease string (e.g., 'Potato' from 'Potato_Late_blight')"""
        if "_" in disease:
            plant = disease.split("_")[0]
        else:
            plant = disease.split()[0] if " " in disease else disease
        
        plant = plant.replace("___", " ").replace("__", " ")
        return plant.capitalize()


# ==============================================
# BUSINESS LOGIC
# ==============================================

class SeverityCalculator:
    """Centralized severity calculation logic"""
    
    @staticmethod
    def calculate(confidence: int, is_healthy: bool) -> str:
        """Calculate severity based on confidence and health status"""
        if is_healthy:
            return "none"
        
        if confidence > Thresholds.high_confidence:
            return "low"
        elif confidence > Thresholds.medium_confidence:
            return "medium"
        else:
            return "high"
    
    @staticmethod
    def get_accent_color(severity: str, is_healthy: bool) -> str:
        """Get accent color based on severity level"""
        if is_healthy:
            return UIColors.ok
        
        color_map = {
            "low": UIColors.lime,
            "medium": UIColors.warn,
            "high": UIColors.danger,
        }
        return color_map.get(severity, UIColors.lime)
    
    @staticmethod
    def get_badge_class(severity: str) -> str:
        """Get CSS badge class for severity level"""
        badge_map = {
            "none": "b-none",
            "low": "b-low",
            "medium": "b-medium",
            "high": "b-high",
        }
        return badge_map.get(severity, "b-low")


class MessageTemplates:
    """Centralized message templates for all text content"""
    
    @staticmethod
    def get_insight(disease: str, confidence: int) -> str:
        """Generate system insight message"""
        return f"Model predicts {disease} with {confidence}% confidence."
    
    @staticmethod
    def get_empty_state_messages() -> Dict[str, str]:
        """Empty state placeholder messages"""
        return {
            "disease": "Upload an image to begin analysis...",
            "confidence": "Awaiting prediction results...",
            "insight": "AI insights will appear here...",
            "solution": "Treatment recommendations will appear here...",
        }
    
    @staticmethod
    def get_card_titles() -> Dict[str, str]:
        """Card title templates"""
        return {
            "disease": "Detected Disease",
            "confidence": "Confidence Score",
            "insight": "System Insight",
            "solution": "Suggested Solution",
            "ai_advisor": "AI Advisory",
        }


# ==============================================
# REUSABLE UI COMPONENTS
# ==============================================

class UIComponents:
    """Reusable UI component builder with centralized styling"""
    
    @staticmethod
    def get_header_style() -> str:
        """Generate consistent header style string"""
        return (
            f"font-size: {StylingConfig.card_header_font_size}; "
            f"letter-spacing: {StylingConfig.card_header_letter_spacing}; "
            f"font-family: {StylingConfig.card_header_font_family}; "
            f"font-weight: {StylingConfig.card_header_font_weight}; "
            f"text-transform: {StylingConfig.card_header_text_transform};"
        )
    
    @staticmethod
    def render_result_card(title: str, icon: str, content_html: str, accent_color: str):
        """Render a result card with HTML content (base method)"""
        card_html = f'''
        <div class="ag-card" style="--card-accent:{accent_color};">
            <div class="ag-card-hdr" style="{UIComponents.get_header_style()}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">{icon}</span>
                {title}
            </div>
            {content_html}
        </div>
        '''
        st.markdown(card_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_empty_card(title: str, icon: str, placeholder: str):
        """Render an empty state card"""
        empty_html = f'<p class="ag-empty">{placeholder}</p>'
        UIComponents.render_result_card(
            title=title,
            icon=icon,
            content_html=empty_html,
            accent_color=UIColors.dim,
        )
    
    @staticmethod
    def render_disease_card(disease: str, plant: str, severity: str, is_healthy: bool, accent_color: str):
        """Render disease card with centralized styling from StylingConfig"""
        header_style = UIComponents.get_header_style()
        
        if is_healthy:
            st.markdown(f'''
            <div class="ag-card" style="--card-accent:{accent_color};">
                <div class="ag-card-hdr" style="{header_style}">
                    <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">🔬</span>
                    Detected Disease
                </div>
                <div style="margin-bottom: {StylingConfig.card_content_margin_bottom};">
                    <div class="ag-disease-ok" style="font-size: {StylingConfig.disease_font_size}; font-weight: {StylingConfig.disease_font_weight}; margin-bottom: {StylingConfig.disease_margin_bottom};">✓ {disease}</div>
                    <div class="ag-plant" style="font-size: {StylingConfig.plant_font_size}; letter-spacing: {StylingConfig.plant_letter_spacing}; margin-bottom: {StylingConfig.plant_margin_bottom}; color: {StylingConfig.plant_color};">{plant}</div>
                    <span class="ag-badge {SeverityCalculator.get_badge_class(severity)}" style="font-size: {StylingConfig.badge_font_size}; padding: {StylingConfig.badge_padding}; display: inline-block;">
                        ● No Disease Detected
                    </span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="ag-card" style="--card-accent:{accent_color};">
                <div class="ag-card-hdr" style="{header_style}">
                    <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">🔬</span>
                    Detected Disease
                </div>
                <div style="margin-bottom: {StylingConfig.card_content_margin_bottom};">
                    <div class="ag-disease" style="font-size: {StylingConfig.disease_font_size}; font-weight: {StylingConfig.disease_font_weight}; margin-bottom: {StylingConfig.disease_margin_bottom};">{disease}</div>
                    <div class="ag-plant" style="font-size: {StylingConfig.plant_font_size}; letter-spacing: {StylingConfig.plant_letter_spacing}; margin-bottom: {StylingConfig.plant_margin_bottom}; color: {StylingConfig.plant_color};">{plant}</div>
                    <span class="ag-badge {SeverityCalculator.get_badge_class(severity)}" style="font-size: {StylingConfig.badge_font_size}; padding: {StylingConfig.badge_padding}; display: inline-block;">
                        ● Severity: {severity.upper()}
                    </span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    @staticmethod
    def render_confidence_insight_card(confidence: int, insight: str, accent_color: str):
        """Render combined confidence + insight card with centralized styling"""
        from styles import bar_gradient
        grad = bar_gradient(confidence)
        header_style = UIComponents.get_header_style()
        
        html = f'''
        <div class="ag-card" style="--card-accent:{accent_color};">
            <div class="ag-card-hdr" style="{header_style}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">📊</span>
                Analysis Details
            </div>
            <div class="ag-conf-row" style="margin-bottom: 20px;">
                <span class="ag-conf-lbl" style="font-size: {StylingConfig.confidence_label_size}; letter-spacing: {StylingConfig.confidence_label_spacing};">Model Certainty</span>
                <span class="ag-conf-pct" style="font-size: {StylingConfig.confidence_percent_size}; font-weight: {StylingConfig.confidence_percent_weight};">{confidence}%</span>
            </div>
            <div class="ag-bar-track" style="margin-bottom: {StylingConfig.progress_bar_margin_bottom}; height: {StylingConfig.progress_bar_height};">
                <div class="ag-bar-fill" style="width:{confidence}%;background:{grad};"></div>
            </div>
            <div style="margin-top: {StylingConfig.divider_margin_top}; padding-top: {StylingConfig.divider_padding_top}; border-top: {StylingConfig.divider_border_width} solid rgba(164,240,0,0.2);">
                <p class="ag-insight" style="margin-bottom: 0; font-size: {StylingConfig.insight_font_size}; line-height: {StylingConfig.insight_line_height};">{insight}</p>
            </div>
        </div>
        '''
        
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def render_solution_card(remedy: str):
        """Render solution card with centralized styling"""
        header_style = UIComponents.get_header_style()
        
        st.markdown(f'''
        <div class="ag-card" style="--card-accent:#2ef2e2;">
            <div class="ag-card-hdr" style="{header_style}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">🌱</span>
                Suggested Solution
            </div>
            <p class="ag-remedy" style="font-size: {StylingConfig.remedy_font_size}; line-height: {StylingConfig.remedy_line_height}; padding: {StylingConfig.remedy_padding};">{remedy}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    @staticmethod
    def render_ai_card(ai_advice: str):
        """Render AI advisory card with centralized styling"""
        header_style = UIComponents.get_header_style()
        
        st.markdown(f'''
        <div class="ag-card" style="--card-accent:#A4F000;">
            <div class="ag-card-hdr" style="{header_style}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">🤖</span>
                AI Advisory
            </div>
            <p class="ag-remedy" style="font-size: {StylingConfig.remedy_font_size}; line-height: {StylingConfig.remedy_line_height}; padding: {StylingConfig.remedy_padding};">{ai_advice}</p>
        </div>
        ''', unsafe_allow_html=True)


# ==============================================
# RESULT PROCESSOR
# ==============================================

class ResultProcessor:
    """Process and format analysis results"""
    
    @staticmethod
    def process_prediction(disease: str, confidence: int, remedy: str, ai_advice: str) -> Dict:
        """Process raw prediction into formatted result dictionary"""
        # Convert confidence to percentage (if it's between 0-1)
        confidence_pct = round(confidence * 100) if confidence <= 1 else confidence
        
        # Format disease name for display (remove underscores, proper capitalization)
        formatted_disease = TextFormatter.format_disease_name(disease)
        
        # Check if the plant is healthy
        is_healthy = any(
            keyword.lower() in formatted_disease.lower() or keyword.lower() in disease.lower()
            for keyword in Thresholds.healthy_keywords
        )
        
        # Calculate severity level
        severity = SeverityCalculator.calculate(confidence_pct, is_healthy)
        
        # Extract plant name from disease string
        plant = TextFormatter.extract_plant_name(disease)
        
        return {
            "disease": formatted_disease,
            "raw_disease": disease,
            "confidence": confidence_pct,
            "healthy": is_healthy,
            "severity": severity,
            "plant": plant,
            "insight": MessageTemplates.get_insight(formatted_disease, confidence_pct),
            "remedy": remedy,
            "ai_advice": ai_advice,
            "accent_color": SeverityCalculator.get_accent_color(severity, is_healthy),
        }


# ==============================================
# VALIDATION HELPERS
# ==============================================

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_file_size(file_bytes: bytes) -> bool:
        """Check if file size is within limits"""
        size_mb = len(file_bytes) / (1024 * 1024)
        return size_mb <= AppConfig.max_file_size_mb
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """Check if file extension is allowed"""
        ext = filename.split(".")[-1].lower()
        return ext in AppConfig.allowed_formats