# template.py — Centralized Configuration & UI Components for AgroScan
# ====================================================================
# Contains app configuration, business logic, and reusable UI components.

from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import streamlit as st
from config import AppColors, AppThresholds, AppLayout


# ==============================================
# APP CONFIGURATION
# ==============================================

@dataclass(frozen=True)
class AppConfig:
    """Main app settings - change name, tagline, layout ratios here"""
    name: str = "AgroScan"
    version: str = "v1.0"
    tagline: str = "Smart Leaf Disease Detection System"
    icon: str = "🌿"
    
    left_col_ratio: float = AppLayout.LEFT_COLUMN_RATIO
    right_col_ratio: float = AppLayout.RIGHT_COLUMN_RATIO
    allowed_formats: Tuple[str, ...] = AppLayout.ALLOWED_FORMATS
    max_file_size_mb: int = AppLayout.MAX_FILE_SIZE_MB


@dataclass(frozen=True)
class StylingConfig:
    """Adjust card sizes, fonts, and spacing globally"""
    section_label_font_size: str = "0.9rem"
    section_label_letter_spacing: str = "4px"
    section_label_margin_bottom: str = "30px"
    section_label_margin_top: str = "15px"
    section_label_alignment: str = "left"
    
    card_header_font_size: str = "0.65rem"
    card_header_letter_spacing: str = "4px"
    card_header_font_family: str = "Montserrat"
    card_header_font_weight: str = "900"
    card_header_text_transform: str = "uppercase"
    card_icon_size: str = "1.1rem"
    
    disease_font_size: str = "1.6rem"
    disease_font_weight: str = "800"
    disease_margin_bottom: str = "14px"
    
    plant_font_size: str = "0.85rem"
    plant_letter_spacing: str = "2px"
    plant_margin_bottom: str = "20px"
    plant_color: str = "#7ec8e0"
    
    badge_font_size: str = "0.7rem"
    badge_padding: str = "4px 14px"
    
    confidence_label_size: str = "0.9rem"
    confidence_label_spacing: str = "2px"
    confidence_percent_size: str = "1.8rem"
    confidence_percent_weight: str = "800"
    
    progress_bar_height: str = "8px"
    progress_bar_margin_bottom: str = "28px"
    
    insight_font_size: str = "0.9rem"
    insight_line_height: str = "1.7"
    
    card_content_margin_bottom: str = "20px"
    divider_margin_top: str = "8px"
    divider_padding_top: str = "18px"
    divider_border_width: str = "1px"
    
    remedy_font_size: str = "0.95rem"
    remedy_line_height: str = "1.8"
    remedy_padding: str = "10px 14px"


@dataclass(frozen=True)
class Thresholds:
    """Confidence thresholds for severity calculation"""
    high_confidence: int = AppThresholds.CONFIDENCE_HIGH
    medium_confidence: int = AppThresholds.CONFIDENCE_MEDIUM
    low_confidence: int = AppThresholds.CONFIDENCE_LOW
    healthy_keywords: Tuple[str, ...] = AppThresholds.HEALTHY_KEYWORDS


@dataclass(frozen=True)
class UIColors:
    """Color scheme - imports from config.py"""
    lime: str = AppColors.LIME
    teal: str = AppColors.TEAL
    warn: str = AppColors.WARN
    danger: str = AppColors.DANGER
    ok: str = AppColors.OK
    bg_root: str = AppColors.BG_ROOT
    border: str = AppColors.BORDER
    border_hi: str = AppColors.BORDER_HI
    mid: str = AppColors.MID
    dim: str = AppColors.DIM
    white: str = AppColors.WHITE


# ==============================================
# TEXT FORMATTING UTILITIES
# ==============================================

class TextFormatter:
    """Clean up model output strings"""
    
    @staticmethod
    def format_disease_name(disease: str) -> str:
        """Convert 'Potato_Late_blight' → 'Potato Late Blight'"""
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
        """Extract crop name from disease string (e.g., 'Potato' from 'Potato_Late_blight')"""
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
    """Calculate disease severity from confidence score"""
    
    @staticmethod
    def calculate(confidence: int, is_healthy: bool) -> str:
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
        badge_map = {
            "none": "b-none",
            "low": "b-low",
            "medium": "b-medium",
            "high": "b-high",
        }
        return badge_map.get(severity, "b-low")


class MessageTemplates:
    """Centralized text for UI messages"""
    
    @staticmethod
    def get_insight(disease: str, confidence: int) -> str:
        return f"Model predicts {disease} with {confidence}% confidence."
    
    @staticmethod
    def get_empty_state_messages() -> Dict[str, str]:
        return {
            "disease": "Upload an image to begin analysis...",
            "confidence": "Awaiting prediction results...",
            "insight": "AI insights will appear here...",
            "solution": "Treatment recommendations will appear here...",
        }
    
    @staticmethod
    def get_card_titles() -> Dict[str, str]:
        return {
            "disease": "Detected Disease",
            "confidence": "Confidence Score",
            "insight": "System Insight",
            "solution": "Suggested Solution",
            "ai_advisor": "AI Advisory",
        }


# ==============================================
# UI COMPONENTS
# ==============================================

class UIComponents:
    """All reusable card components"""
    
    @staticmethod
    def get_header_style() -> str:
        """Generate consistent card header CSS"""
        return (
            f"font-size: {StylingConfig.card_header_font_size}; "
            f"letter-spacing: {StylingConfig.card_header_letter_spacing}; "
            f"font-family: {StylingConfig.card_header_font_family}; "
            f"font-weight: {StylingConfig.card_header_font_weight}; "
            f"text-transform: {StylingConfig.card_header_text_transform};"
        )
    
    @staticmethod
    def render_disease_card(disease: str, plant: str, severity: str, is_healthy: bool, accent_color: str):
        """Display detected disease with severity badge"""
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
        """Display confidence score with progress bar and system insight"""
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
    def render_empty_card(title: str, icon: str, placeholder: str):
        """Display empty state placeholder card"""
        empty_html = f'<p class="ag-empty">{placeholder}</p>'
        card_html = f'''
        <div class="ag-card" style="--card-accent:{UIColors.dim};">
            <div class="ag-card-hdr" style="{UIComponents.get_header_style()}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">{icon}</span>
                {title}
            </div>
            {empty_html}
        </div>
        '''
        st.markdown(card_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_solution_card(remedy: str):
        """Action-focused treatment card - uses Ollama AI"""
        from config import AppColors
        header_style = UIComponents.get_header_style()
        import re
        
        # Remove "AI-generated overview" line from AI response
        lines = remedy.split('\n')
        filtered_lines = []
        for line in lines:
            if 'AI-generated overview' in line:
                continue
            filtered_lines.append(line)
        remedy = '\n'.join(filtered_lines)
        
        # Convert **bold** to teal-colored HTML bold
        formatted_remedy = re.sub(r'\*\*(.*?)\*\*', rf'<strong style="color: {AppColors.TEAL};">\1</strong>', remedy)
        
        # Convert dash (-) bullet points to teal bullet symbols
        lines = formatted_remedy.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('-'):
                bullet_text = line.strip()[1:].strip()
                lines[i] = f'  <span style="color: {AppColors.TEAL};">•</span> {bullet_text}'
        
        formatted_remedy = '<br>'.join(lines)
        
        st.markdown(f'''
        <div class="ag-card" style="--card-accent:#2ef2e2;">
            <div class="ag-card-hdr" style="{header_style}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">🌱</span>
                Suggested Solution
            </div>
            <div class="ag-remedy" style="font-size: {StylingConfig.remedy_font_size}; line-height: {StylingConfig.remedy_line_height}; padding: {StylingConfig.remedy_padding};">
                {formatted_remedy}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    @staticmethod
    def render_ai_card(ai_advice: str):
        """Educational AI advisory card - focuses on disease understanding"""
        from config import AppColors
        header_style = UIComponents.get_header_style()
        import re
        
        lines = ai_advice.split('\n')
        processed_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                processed_lines.append('<div style="height: 5px;"></div>')
            elif stripped.startswith('🔬') or stripped.startswith('🌧️') or stripped.startswith('⚠️') or stripped.startswith('💡'):
                # Emoji headers become teal & bold
                processed_lines.append(f'<div style="margin-top: 10px;"><strong style="color: {AppColors.TEAL};">{stripped}</strong></div>')
            elif stripped.startswith('-'):
                # Bullet points with teal symbol
                bullet_text = stripped[1:].strip()
                processed_lines.append(f'  <span style="color: {AppColors.TEAL};">•</span> {bullet_text}')
            else:
                processed_lines.append(line)
        
        formatted_advice = '<br>'.join(processed_lines)
        
        st.markdown(f'''
        <div class="ag-card" style="--card-accent:{AppColors.CARD_ACCENT_AI};">
            <div class="ag-card-hdr" style="{header_style}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">🤖</span>
                AI Advisory
            </div>
            <div class="ag-remedy" style="font-size: {StylingConfig.remedy_font_size}; line-height: {StylingConfig.remedy_line_height}; padding: {StylingConfig.remedy_padding};">
                {formatted_advice}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    @staticmethod
    def render_weather_comparison_card(comparison_data: dict):
        """Weather card - compares ideal vs actual crop conditions"""
        
        # Accent color based on suitability score
        if comparison_data['overall_score'] >= AppThresholds.SUITABILITY_EXCELLENT:
            accent_color = AppColors.SUITABILITY_EXCELLENT
        elif comparison_data['overall_score'] >= AppThresholds.SUITABILITY_GOOD:
            accent_color = AppColors.SUITABILITY_GOOD
        elif comparison_data['overall_score'] >= AppThresholds.SUITABILITY_MODERATE:
            accent_color = AppColors.SUITABILITY_MODERATE
        else:
            accent_color = AppColors.SUITABILITY_POOR
        
        # Temperature display values
        if comparison_data['temp_status'] == 'high':
            temp_arrow = "▲"
            temp_color = AppColors.TEMP_HIGH
            temp_delta = f"{comparison_data['temp_deviation']}°C above ideal"
        elif comparison_data['temp_status'] == 'low':
            temp_arrow = "▼"
            temp_color = AppColors.TEMP_LOW
            temp_delta = f"{comparison_data['temp_deviation']}°C below ideal"
        else:
            temp_arrow = "✓"
            temp_color = AppColors.TEMP_IDEAL
            temp_delta = "Within ideal range"
        
        # Humidity display values
        if comparison_data['humidity_status'] == 'high':
            humidity_arrow = "▲"
            humidity_color = AppColors.HUMIDITY_HIGH
            humidity_delta = f"{comparison_data['humidity_deviation']}% above ideal"
        elif comparison_data['humidity_status'] == 'low':
            humidity_arrow = "▼"
            humidity_color = AppColors.HUMIDITY_LOW
            humidity_delta = f"{comparison_data['humidity_deviation']}% below ideal"
        else:
            humidity_arrow = "✓"
            humidity_color = AppColors.HUMIDITY_IDEAL
            humidity_delta = "Within ideal range"
        
        # Suitability score display
        if comparison_data['overall_score'] >= AppThresholds.SUITABILITY_EXCELLENT:
            suit_emoji = "🟢"
            suit_color = AppColors.SUITABILITY_EXCELLENT
        elif comparison_data['overall_score'] >= AppThresholds.SUITABILITY_GOOD:
            suit_emoji = "🟡"
            suit_color = AppColors.SUITABILITY_GOOD
        elif comparison_data['overall_score'] >= AppThresholds.SUITABILITY_MODERATE:
            suit_emoji = "🟠"
            suit_color = AppColors.SUITABILITY_MODERATE
        else:
            suit_emoji = "🔴"
            suit_color = AppColors.SUITABILITY_POOR
        
        # Build recommendations HTML
        recommendations_html = ""
        if comparison_data["recommendations"]:
            for rec in comparison_data["recommendations"]:
                recommendations_html += f'<div style="background: rgba(255,179,71,0.1); border-left: 3px solid {AppColors.WARN}; padding: 8px 12px; margin: 8px 0; border-radius: 6px;">{rec}</div>'
        else:
            recommendations_html = f'<div style="color: {AppColors.OK};">✓ Weather conditions are ideal for this crop</div>'
        
        # Disease risk display
        if comparison_data.get("disease_risk"):
            disease_risk_html = f'<div style="background: rgba(255,92,106,0.1); border-left: 3px solid {AppColors.DANGER}; padding: 8px 12px; border-radius: 6px;">⚠️ High-risk diseases: {", ".join(comparison_data["disease_risk"][:3])}</div>'
        else:
            disease_risk_html = f'<div style="background: rgba(46,242,226,0.1); border-left: 3px solid {AppColors.TEAL}; padding: 8px 12px; border-radius: 6px;">📊 Monitor field regularly for early signs of disease</div>'
        
        html_string = f'''
        <div class="ag-card" style="--card-accent:{accent_color}; margin-bottom: 20px; padding-right: 16px;">
            <div class="ag-card-hdr" style="{UIComponents.get_header_style()}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">🌤️</span>
                Weather & Crop Suitability
            </div>
            <div style="margin-bottom: {StylingConfig.card_content_margin_bottom};">
                
                <!-- Two column layout: Requirements vs Current -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 20px;">
                    
                    <!-- LEFT: Ideal crop requirements -->
                    <div>
                        <div style="font-weight: 600; margin-bottom: 15px; color: #e8f4f0;">📋 CROP REQUIREMENTS</div>
                        
                        <div style="margin-bottom: 20px;">
                            <div style="color: #7ec8e0; font-size: 0.8rem;">Temperature Range</div>
                            <div style="display: flex; align-items: baseline; gap: 10px;">
                                <span style="font-size: 1.5rem; font-weight: 600; color: #e8f4f0;">{comparison_data['ideal_temp']}</span>
                                <span style="color: {AppColors.OK}; font-size: 0.9rem;">✓</span>
                            </div>
                            <div style="color: {AppColors.OK}; font-size: 0.75rem;">Optimal: {comparison_data['ideal_temp_optimal']}</div>
                        </div>
                        
                        <div>
                            <div style="color: #7ec8e0; font-size: 0.8rem;">Humidity Range</div>
                            <div style="display: flex; align-items: baseline; gap: 10px;">
                                <span style="font-size: 1.5rem; font-weight: 600; color: #e8f4f0;">{comparison_data['ideal_humidity']}</span>
                                <span style="color: {AppColors.OK}; font-size: 0.9rem;">✓</span>
                            </div>
                            <div style="color: {AppColors.OK}; font-size: 0.75rem;">Ideal growing conditions</div>
                        </div>
                    </div>
                    
                    <!-- RIGHT: Actual current conditions -->
                    <div style="border-left: 1px solid rgba(164,240,0,0.2); padding-left: 20px;">
                        <div style="font-weight: 600; margin-bottom: 15px; color: #e8f4f0;">📍 CURRENT CONDITIONS</div>
                        
                        <div style="margin-bottom: 20px;">
                            <div style="color: #7ec8e0; font-size: 0.8rem;">Temperature</div>
                            <div style="display: flex; align-items: baseline; gap: 10px;">
                                <span style="font-size: 1.5rem; font-weight: 600; color: #e8f4f0;">{comparison_data['actual_temp']}°C</span>
                                <span style="color: {temp_color}; font-size: 0.9rem;">{temp_arrow}</span>
                            </div>
                            <div style="color: {temp_color}; font-size: 0.75rem;">{temp_delta}</div>
                        </div>
                        
                        <div>
                            <div style="color: #7ec8e0; font-size: 0.8rem;">Humidity</div>
                            <div style="display: flex; align-items: baseline; gap: 10px;">
                                <span style="font-size: 1.5rem; font-weight: 600; color: #e8f4f0;">{comparison_data['actual_humidity']}%</span>
                                <span style="color: {humidity_color}; font-size: 0.9rem;">{humidity_arrow}</span>
                            </div>
                            <div style="color: {humidity_color}; font-size: 0.75rem;">{humidity_delta}</div>
                        </div>
                    </div>
                </div>
                
                <!-- Overall Suitability Progress Bar -->
                <div style="margin: 20px 0 15px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #7ec8e0;">Overall Suitability</span>
                        <span style="color: {suit_color}; font-weight: bold;">{suit_emoji} {comparison_data['suitability']} ({comparison_data['overall_score']}%)</span>
                    </div>
                    <div class="ag-bar-track" style="height: 6px;">
                        <div class="ag-bar-fill" style="width:{comparison_data['overall_score']}%; background: {suit_color};"></div>
                    </div>
                </div>
                
                <div style="border-top: 1px solid rgba(164,240,0,0.2); margin: 15px 0;"></div>
                
                <!-- Actionable Recommendations -->
                <div style="font-weight: 600; margin-bottom: 10px; color: #e8f4f0;">💡 MANAGEMENT RECOMMENDATIONS</div>
                {recommendations_html}
                
                <div style="border-top: 1px solid rgba(164,240,0,0.2); margin: 15px 0;"></div>
                
                <!-- Disease Risk Warning -->
                <div style="font-weight: 600; margin-bottom: 10px; color: #e8f4f0;">⚠️ DISEASE RISK ALERT</div>
                {disease_risk_html}
                
            </div>
        </div>
        '''
        
        st.html(html_string)


# ==============================================
# CROP WEATHER REQUIREMENTS
# ==============================================

@dataclass(frozen=True)
class CropWeatherRequirements:
    """Ideal temperature/humidity ranges for each crop in the model"""
    
    REQUIREMENTS = {
        "Potato": {
            "temp_min": 15, "temp_max": 20, "temp_optimal": 18,
            "humidity_min": 60, "humidity_max": 70,
            "rainfall_weekly_mm": (25, 35),
            "disease_high_risk": ["Late_Blight", "Early_Blight"],
            "alert_messages": {
                "high_temp": "🌡️ High temperature stress - Mulch and irrigate early morning",
                "high_humidity": "💧 High humidity - Watch for late blight, improve air circulation",
                "low_rainfall": "🏜️ Low rainfall - Increase irrigation frequency",
                "low_humidity": "🍂 Low humidity - Monitor for pest infestation"
            }
        },
        "Tomato": {
            "temp_min": 20, "temp_max": 27, "temp_optimal": 24,
            "humidity_min": 40, "humidity_max": 70,
            "rainfall_weekly_mm": (25, 50),
            "disease_high_risk": ["Late_Blight", "Early_Blight", "Bacterial_Spot"],
            "alert_messages": {
                "high_temp": "🔥 Heat stress - Provide shade net if possible",
                "high_humidity": "🍅 High humidity risk - Increase spacing, stake plants",
                "low_rainfall": "💦 Low moisture - Drip irrigation recommended",
                "low_humidity": "🍂 Low humidity - Monitor for spider mites"
            }
        },
        "Rice": {
            "temp_min": 20, "temp_max": 35, "temp_optimal": 28,
            "humidity_min": 70, "humidity_max": 85,
            "rainfall_weekly_mm": (100, 200),
            "disease_high_risk": ["Diseased", "Blast", "Sheath_Blight"],
            "alert_messages": {
                "high_temp": "☀️ High temperature - Maintain standing water",
                "low_humidity": "🌾 Low humidity stress - Increase irrigation frequency",
                "low_rainfall": "⚠️ Water stress - Ensure field flooding",
                "high_humidity": "💧 High humidity - Watch for fungal diseases"
            }
        },
        "Cotton": {
            "temp_min": 20, "temp_max": 35, "temp_optimal": 28,
            "humidity_min": 50, "humidity_max": 70,
            "rainfall_weekly_mm": (20, 30),
            "disease_high_risk": ["Curl_virus", "Bacterial_blight", "Fusarium_wilt"],
            "alert_messages": {
                "high_temp": "🌿 Heat stress - Ensure adequate irrigation",
                "high_humidity": "🦠 High humidity - Watch for bacterial blight",
                "low_rainfall": "💧 Water stress - Schedule regular irrigation",
                "low_humidity": "🍂 Low humidity - Monitor for whiteflies (curl virus vector)"
            }
        },
        "Pepper": {
            "temp_min": 18, "temp_max": 30, "temp_optimal": 24,
            "humidity_min": 50, "humidity_max": 70,
            "rainfall_weekly_mm": (25, 40),
            "disease_high_risk": ["Bacterial_spot"],
            "alert_messages": {
                "high_temp": "🌶️ Heat stress - Provide afternoon shade",
                "high_humidity": "🦠 High humidity - Watch for bacterial spot",
                "low_rainfall": "💧 Low moisture - Maintain consistent soil moisture",
                "low_humidity": "🍂 Low humidity - Monitor for thrips and aphids"
            }
        }
    }
    
    @staticmethod
    def get_requirements(crop_name: str) -> dict:
        """Match crop name to requirements (supports partial matching)"""
        if crop_name in CropWeatherRequirements.REQUIREMENTS:
            return CropWeatherRequirements.REQUIREMENTS[crop_name]
        
        for crop in CropWeatherRequirements.REQUIREMENTS:
            if crop.lower() == crop_name.lower():
                return CropWeatherRequirements.REQUIREMENTS[crop]
        
        for crop in CropWeatherRequirements.REQUIREMENTS:
            if crop.lower() in crop_name.lower() or crop_name.lower() in crop.lower():
                return CropWeatherRequirements.REQUIREMENTS[crop]
        
        return CropWeatherRequirements.REQUIREMENTS.get("Potato")
    
    @staticmethod
    def get_supported_crops() -> list:
        return list(CropWeatherRequirements.REQUIREMENTS.keys())


class WeatherComparison:
    """Compare current weather against crop requirements"""
    
    @staticmethod
    def compare(actual_temp: float, actual_humidity: float, crop_name: str) -> dict:
        req = CropWeatherRequirements.get_requirements(crop_name)
        
        # Temperature comparison
        temp_status = "ideal"
        temp_deviation = 0
        if actual_temp < req["temp_min"]:
            temp_status = "low"
            temp_deviation = round(req["temp_min"] - actual_temp, 1)
        elif actual_temp > req["temp_max"]:
            temp_status = "high"
            temp_deviation = round(actual_temp - req["temp_max"], 1)
        
        # Humidity comparison
        humidity_status = "ideal"
        humidity_deviation = 0
        if actual_humidity < req["humidity_min"]:
            humidity_status = "low"
            humidity_deviation = round(req["humidity_min"] - actual_humidity, 1)
        elif actual_humidity > req["humidity_max"]:
            humidity_status = "high"
            humidity_deviation = round(actual_humidity - req["humidity_max"], 1)
        
        # Generate recommendations based on deviations
        recommendations = []
        if temp_status == "high":
            recommendations.append(req["alert_messages"]["high_temp"])
        elif temp_status == "low":
            recommendations.append(f"❄️ Low temperature stress - Protect plants from cold")
            
        if humidity_status == "high":
            recommendations.append(req["alert_messages"]["high_humidity"])
        elif humidity_status == "low":
            recommendations.append(req["alert_messages"].get("low_humidity", "💧 Low humidity - Increase moisture around plants"))
        
        if actual_humidity < req["humidity_min"] and temp_status == "high":
            recommendations.append(req["alert_messages"].get("low_rainfall", "💧 Monitor soil moisture"))
        
        # Calculate suitability score (0-100)
        temp_score = 100 - (temp_deviation * 5) if temp_deviation > 0 else 100
        humidity_score = 100 - (humidity_deviation * 3) if humidity_deviation > 0 else 100
        overall_score = round((temp_score + humidity_score) / 2)
        overall_score = max(0, min(100, overall_score))
        
        # Determine suitability level
        if overall_score >= AppThresholds.SUITABILITY_EXCELLENT:
            suitability = "Excellent"
            suitability_color = AppColors.SUITABILITY_EXCELLENT
        elif overall_score >= AppThresholds.SUITABILITY_GOOD:
            suitability = "Good"
            suitability_color = AppColors.SUITABILITY_GOOD
        elif overall_score >= AppThresholds.SUITABILITY_MODERATE:
            suitability = "Moderate"
            suitability_color = AppColors.SUITABILITY_MODERATE
        else:
            suitability = "Poor"
            suitability_color = AppColors.SUITABILITY_POOR
        
        return {
            "crop": crop_name,
            "ideal_temp": f"{req['temp_min']}-{req['temp_max']}°C",
            "ideal_temp_optimal": f"{req['temp_optimal']}°C",
            "ideal_humidity": f"{req['humidity_min']}-{req['humidity_max']}%",
            "actual_temp": actual_temp,
            "actual_humidity": actual_humidity,
            "temp_status": temp_status,
            "humidity_status": humidity_status,
            "temp_deviation": temp_deviation,
            "humidity_deviation": humidity_deviation,
            "recommendations": recommendations,
            "disease_risk": req.get("disease_high_risk", []),
            "overall_score": overall_score,
            "suitability": suitability,
            "suitability_color": suitability_color
        }


# ==============================================
# RESULT PROCESSOR
# ==============================================

class ResultProcessor:
    """Format model predictions into display-ready dictionary"""
    
    @staticmethod
    def process_prediction(disease: str, confidence: int, remedy: str, ai_advice: str) -> Dict:
        confidence_pct = round(confidence * 100) if confidence <= 1 else confidence
        formatted_disease = TextFormatter.format_disease_name(disease)
        
        is_healthy = any(
            keyword.lower() in formatted_disease.lower() or keyword.lower() in disease.lower()
            for keyword in Thresholds.healthy_keywords
        )
        
        severity = SeverityCalculator.calculate(confidence_pct, is_healthy)
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
    """File upload validation utilities"""
    
    @staticmethod
    def validate_file_size(file_bytes: bytes) -> bool:
        size_mb = len(file_bytes) / (1024 * 1024)
        return size_mb <= AppConfig.max_file_size_mb
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        ext = filename.split(".")[-1].lower()
        return ext in AppConfig.allowed_formats