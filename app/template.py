# template.py — Centralized Configuration & Reusable Components
# ==============================================================

from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import streamlit as st

# ==============================================
# APP CONFIGURATION
# ==============================================

@dataclass(frozen=True)
class AppConfig:
    """Central app configuration - Change app-wide settings here"""
    name: str = "AgroScan"
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
    section_label_font_size: str = "0.9rem"
    section_label_letter_spacing: str = "4px"
    section_label_margin_bottom: str = "30px"
    section_label_margin_top: str = "15px"
    section_label_alignment: str = "left"
    
    # ===== CARD HEADER STYLES =====
    card_header_font_size: str = "0.65rem"
    card_header_letter_spacing: str = "4px"
    card_header_font_family: str = "Montserrat"
    card_header_font_weight: str = "900"
    card_header_text_transform: str = "uppercase"
    card_icon_size: str = "1.1rem"
    
    # ===== DISEASE CARD STYLES =====
    disease_font_size: str = "1.6rem"
    disease_font_weight: str = "800"
    disease_margin_bottom: str = "14px"
    
    plant_font_size: str = "0.85rem"
    plant_letter_spacing: str = "2px"
    plant_margin_bottom: str = "20px"
    plant_color: str = "#7ec8e0"
    
    badge_font_size: str = "0.7rem"
    badge_padding: str = "4px 14px"
    
    # ===== ANALYSIS CARD STYLES =====
    confidence_label_size: str = "0.9rem"
    confidence_label_spacing: str = "2px"
    confidence_percent_size: str = "1.8rem"
    confidence_percent_weight: str = "800"
    
    progress_bar_height: str = "8px"
    progress_bar_margin_bottom: str = "28px"
    
    insight_font_size: str = "0.9rem"
    insight_line_height: str = "1.7"
    
    # ===== CARD SPACING =====
    card_content_margin_bottom: str = "20px"
    divider_margin_top: str = "8px"
    divider_padding_top: str = "18px"
    divider_border_width: str = "1px"
    
    # ===== SOLUTION & AI CARDS =====
    remedy_font_size: str = "0.95rem"
    remedy_line_height: str = "1.8"
    remedy_padding: str = "10px 14px"


@dataclass(frozen=True)
class Thresholds:
    """Confidence and severity thresholds"""
    high_confidence: int = 85
    medium_confidence: int = 60
    low_confidence: int = 0
    healthy_keywords: Tuple[str, ...] = ("Healthy", "health", "good condition")


@dataclass(frozen=True)
class UIColors:
    """Centralized color scheme"""
    lime: str = "#a4f000"
    teal: str = "#2ef2e2"
    warn: str = "#ffb347"
    danger: str = "#ff5c6a"
    ok: str = "#5efa5e"
    bg_root: str = "#060d10"
    border: str = "#14303f"
    border_hi: str = "#1d4a5c"
    mid: str = "#4a8a7a"
    dim: str = "#1e4a3a"
    white: str = "#e8f4f0"


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
        """Extract plant name from disease string"""
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
    """Centralized message templates"""
    
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
# REUSABLE UI COMPONENTS
# ==============================================

class UIComponents:
    """Reusable UI component builder with centralized styling"""
    
    @staticmethod
    def get_header_style() -> str:
        return (
            f"font-size: {StylingConfig.card_header_font_size}; "
            f"letter-spacing: {StylingConfig.card_header_letter_spacing}; "
            f"font-family: {StylingConfig.card_header_font_family}; "
            f"font-weight: {StylingConfig.card_header_font_weight}; "
            f"text-transform: {StylingConfig.card_header_text_transform};"
        )
    
    @staticmethod
    def render_result_card(title: str, icon: str, content_html: str, accent_color: str):
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
        empty_html = f'<p class="ag-empty">{placeholder}</p>'
        UIComponents.render_result_card(
            title=title,
            icon=icon,
            content_html=empty_html,
            accent_color=UIColors.dim,
        )
    
    @staticmethod
    def render_disease_card(disease: str, plant: str, severity: str, is_healthy: bool, accent_color: str):
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
    
    @staticmethod
    def render_weather_comparison_card(comparison_data: dict):
        """Render weather comparison card - no padding version"""
        
        # Determine accent color based on suitability
        if comparison_data['overall_score'] >= 80:
            accent_color = "#5efa5e"
        elif comparison_data['overall_score'] >= 60:
            accent_color = "#a4f000"
        elif comparison_data['overall_score'] >= 40:
            accent_color = "#ffb347"
        else:
            accent_color = "#ff5c6a"
        
        # Determine colors for current conditions display
        if comparison_data['temp_status'] == 'high':
            temp_arrow = "▲"
            temp_color = "#ffb347"
            temp_delta = f"{comparison_data['temp_deviation']}°C above ideal"
        elif comparison_data['temp_status'] == 'low':
            temp_arrow = "▼"
            temp_color = "#4a8a7a"
            temp_delta = f"{comparison_data['temp_deviation']}°C below ideal"
        else:
            temp_arrow = "✓"
            temp_color = "#5efa5e"
            temp_delta = "Within ideal range"
        
        if comparison_data['humidity_status'] == 'high':
            humidity_arrow = "▲"
            humidity_color = "#ffb347"
            humidity_delta = f"{comparison_data['humidity_deviation']}% above ideal"
        elif comparison_data['humidity_status'] == 'low':
            humidity_arrow = "▼"
            humidity_color = "#4a8a7a"
            humidity_delta = f"{comparison_data['humidity_deviation']}% below ideal"
        else:
            humidity_arrow = "✓"
            humidity_color = "#5efa5e"
            humidity_delta = "Within ideal range"
        
        # Suitability emoji and color
        if comparison_data['overall_score'] >= 80:
            suit_emoji = "🟢"
            suit_color = "#5efa5e"
        elif comparison_data['overall_score'] >= 60:
            suit_emoji = "🟡"
            suit_color = "#a4f000"
        elif comparison_data['overall_score'] >= 40:
            suit_emoji = "🟠"
            suit_color = "#ffb347"
        else:
            suit_emoji = "🔴"
            suit_color = "#ff5c6a"
        
        # Build recommendations HTML
        recommendations_html = ""
        if comparison_data["recommendations"]:
            for rec in comparison_data["recommendations"]:
                recommendations_html += f'<div style="background: rgba(255,179,71,0.1); border-left: 3px solid #ffb347; padding: 8px 12px; margin: 8px 0; border-radius: 6px;">{rec}</div>'
        else:
            recommendations_html = '<div style="color: #5efa5e;">✓ Weather conditions are ideal for this crop</div>'
        
        # Disease risk HTML
        if comparison_data.get("disease_risk"):
            disease_risk_html = f'<div style="background: rgba(255,92,106,0.1); border-left: 3px solid #ff5c6a; padding: 8px 12px; border-radius: 6px;">⚠️ High-risk diseases: {", ".join(comparison_data["disease_risk"][:3])}</div>'
        else:
            disease_risk_html = '<div style="background: rgba(46,242,226,0.1); border-left: 3px solid #2ef2e2; padding: 8px 12px; border-radius: 6px;">📊 Monitor field regularly for early signs of disease</div>'
        
        # NO PADDING COLUMNS - render directly
        html_string = f'''
        <div class="ag-card" style="--card-accent:{accent_color}; margin-bottom: 20px; padding-right: 16px;">
            <div class="ag-card-hdr" style="{UIComponents.get_header_style()}">
                <span class="ag-icon" style="font-size: {StylingConfig.card_icon_size};">🌤️</span>
                Weather & Crop Suitability
            </div>
            <div style="margin-bottom: {StylingConfig.card_content_margin_bottom};">
                
                <!-- Two columns using CSS grid -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 20px;">
                    
                    <!-- LEFT COLUMN: CROP REQUIREMENTS -->
                    <div>
                        <div style="font-weight: 600; margin-bottom: 15px; color: #e8f4f0;">📋 CROP REQUIREMENTS</div>
                        
                        <div style="margin-bottom: 20px;">
                            <div style="color: #7ec8e0; font-size: 0.8rem;">Temperature Range</div>
                            <div style="display: flex; align-items: baseline; gap: 10px;">
                                <span style="font-size: 1.5rem; font-weight: 600; color: #e8f4f0;">{comparison_data['ideal_temp']}</span>
                                <span style="color: #5efa5e; font-size: 0.9rem;">✓</span>
                            </div>
                            <div style="color: #5efa5e; font-size: 0.75rem;">Optimal: {comparison_data['ideal_temp_optimal']}</div>
                        </div>
                        
                        <div>
                            <div style="color: #7ec8e0; font-size: 0.8rem;">Humidity Range</div>
                            <div style="display: flex; align-items: baseline; gap: 10px;">
                                <span style="font-size: 1.5rem; font-weight: 600; color: #e8f4f0;">{comparison_data['ideal_humidity']}</span>
                                <span style="color: #5efa5e; font-size: 0.9rem;">✓</span>
                            </div>
                            <div style="color: #5efa5e; font-size: 0.75rem;">Ideal growing conditions</div>
                        </div>
                    </div>
                    
                    <!-- RIGHT COLUMN: CURRENT CONDITIONS -->
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
                
                <!-- Overall Suitability -->
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
                
                <!-- Recommendations -->
                <div style="font-weight: 600; margin-bottom: 10px; color: #e8f4f0;">💡 MANAGEMENT RECOMMENDATIONS</div>
                {recommendations_html}
                
                <div style="border-top: 1px solid rgba(164,240,0,0.2); margin: 15px 0;"></div>
                
                <!-- Disease Risk -->
                <div style="font-weight: 600; margin-bottom: 10px; color: #e8f4f0;">⚠️ DISEASE RISK ALERT</div>
                {disease_risk_html}
                
            </div>
        </div>
        '''
        
        # Render directly - NO padding columns
        st.html(html_string)

# ==============================================
# CROP WEATHER REQUIREMENTS
# ==============================================

@dataclass(frozen=True)
class CropWeatherRequirements:
    """Ideal weather conditions for different crops"""
    
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
            "disease_high_risk": ["Early_Blight", "Leaf_Mold", "Bacterial_Spot"],
            "alert_messages": {
                "high_temp": "🔥 Heat stress - Provide shade net if possible",
                "high_humidity": "🍅 High humidity risk - Increase spacing, stake plants",
                "low_rainfall": "💦 Low moisture - Drip irrigation recommended"
            }
        },
        "Rice": {
            "temp_min": 20, "temp_max": 35, "temp_optimal": 28,
            "humidity_min": 70, "humidity_max": 85,
            "rainfall_weekly_mm": (100, 200),
            "disease_high_risk": ["Blast", "Sheath_Blight", "Brown_Spot"],
            "alert_messages": {
                "high_temp": "☀️ High temperature - Maintain standing water",
                "low_humidity": "🌾 Low humidity stress - Increase irrigation frequency",
                "low_rainfall": "⚠️ Water stress - Ensure field flooding"
            }
        },
        "Wheat": {
            "temp_min": 12, "temp_max": 25, "temp_optimal": 18,
            "humidity_min": 40, "humidity_max": 60,
            "rainfall_weekly_mm": (15, 25),
            "disease_high_risk": ["Rust", "Powdery_Mildew"],
            "alert_messages": {
                "high_temp": "🌾 Heat stress - Early morning irrigation",
                "high_humidity": "🍄 Humidity risk - Watch for rust development",
                "low_rainfall": "💧 Low moisture - Light irrigation needed"
            }
        },
        "Maize": {
            "temp_min": 18, "temp_max": 30, "temp_optimal": 24,
            "humidity_min": 50, "humidity_max": 75,
            "rainfall_weekly_mm": (25, 50),
            "disease_high_risk": ["Rust", "Leaf_Blight"],
            "alert_messages": {
                "high_temp": "🌽 Heat stress - Provide wind breaks",
                "high_humidity": "⚠️ High humidity - Monitor for leaf diseases",
                "low_rainfall": "💦 Low moisture - Drip irrigation recommended"
            }
        }
    }
    
    @staticmethod
    def get_requirements(crop_name: str) -> dict:
        """Get weather requirements for a crop"""
        if crop_name in CropWeatherRequirements.REQUIREMENTS:
            return CropWeatherRequirements.REQUIREMENTS[crop_name]
        
        for crop in CropWeatherRequirements.REQUIREMENTS:
            if crop.lower() in crop_name.lower() or crop_name.lower() in crop.lower():
                return CropWeatherRequirements.REQUIREMENTS[crop]
        
        return CropWeatherRequirements.REQUIREMENTS.get("Potato")
    
    @staticmethod
    def get_supported_crops() -> list:
        return list(CropWeatherRequirements.REQUIREMENTS.keys())


class WeatherComparison:
    """Compare actual vs ideal weather conditions"""
    
    @staticmethod
    def compare(actual_temp: float, actual_humidity: float, crop_name: str) -> dict:
        """Compare actual weather with crop requirements"""
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
        
        # Generate recommendations
        recommendations = []
        if temp_status == "high":
            recommendations.append(req["alert_messages"]["high_temp"])
        elif temp_status == "low":
            recommendations.append(f"❄️ Low temperature stress - Protect plants from cold")
            
        if humidity_status == "high":
            recommendations.append(req["alert_messages"]["high_humidity"])
        elif humidity_status == "low":
            recommendations.append(req["alert_messages"].get("low_humidity", "💧 Low humidity - Increase moisture around plants"))
        
        # Calculate overall suitability score
        temp_score = 100 - (temp_deviation * 5) if temp_deviation > 0 else 100
        humidity_score = 100 - (humidity_deviation * 3) if humidity_deviation > 0 else 100
        overall_score = round((temp_score + humidity_score) / 2)
        overall_score = max(0, min(100, overall_score))
        
        # Determine suitability level
        if overall_score >= 80:
            suitability = "Excellent"
            suitability_color = "#5efa5e"
        elif overall_score >= 60:
            suitability = "Good"
            suitability_color = "#a4f000"
        elif overall_score >= 40:
            suitability = "Moderate"
            suitability_color = "#ffb347"
        else:
            suitability = "Poor"
            suitability_color = "#ff5c6a"
        
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
    """Process and format analysis results"""
    
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
    """Input validation utilities"""
    
    @staticmethod
    def validate_file_size(file_bytes: bytes) -> bool:
        size_mb = len(file_bytes) / (1024 * 1024)
        return size_mb <= AppConfig.max_file_size_mb
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        ext = filename.split(".")[-1].lower()
        return ext in AppConfig.allowed_formats