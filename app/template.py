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
    """Central app configuration"""
    name: str = "AgroScan AI"
    version: str = "v1.0"
    tagline: str = "Smart Leaf Disease Detection System"
    icon: str = "🌿"
    
    # Layout
    left_col_ratio: float = 0.42
    right_col_ratio: float = 0.58
    
    # File upload
    allowed_formats: Tuple[str, ...] = ("jpg", "jpeg", "png")
    max_file_size_mb: int = 10


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
    """Text formatting utilities"""
    
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
    """Reusable UI component builder"""
    
    @staticmethod
    def render_result_card(title: str, icon: str, content_html: str, accent_color: str):
        """Render a result card with HTML content"""
        card_html = f'''
        <div class="ag-card" style="--card-accent:{accent_color};">
            <div class="ag-card-hdr">
                <span class="ag-icon">{icon}</span>
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
        """Directly render disease card"""
        if is_healthy:
            st.markdown(f'''
            <div class="ag-card" style="--card-accent:{accent_color};">
                <div class="ag-card-hdr">
                    <span class="ag-icon">🔬</span>
                    Detected Disease
                </div>
                <div class="ag-disease-ok">✓ {disease}</div>
                <div class="ag-plant">{plant}</div>
                <span class="ag-badge {SeverityCalculator.get_badge_class(severity)}">
                    ● No Disease Detected
                </span>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="ag-card" style="--card-accent:{accent_color};">
                <div class="ag-card-hdr">
                    <span class="ag-icon">🔬</span>
                    Detected Disease
                </div>
                <div class="ag-disease">{disease}</div>
                <div class="ag-plant">{plant}</div>
                <span class="ag-badge {SeverityCalculator.get_badge_class(severity)}">
                    ● Severity: {severity.upper()}
                </span>
            </div>
            ''', unsafe_allow_html=True)
    
    @staticmethod
    def render_confidence_insight_card(confidence: int, insight: str, accent_color: str):
        """Render combined Confidence + Insight card"""
        from styles import bar_gradient
        grad = bar_gradient(confidence)
        st.markdown(f'''
        <div class="ag-card" style="--card-accent:{accent_color};">
            <div class="ag-card-hdr">
                <span class="ag-icon">📊</span>
                Analysis Details
            </div>
            <div class="ag-conf-row">
                <span class="ag-conf-lbl">Model Certainty</span>
                <span class="ag-conf-pct">{confidence}%</span>
            </div>
            <div class="ag-bar-track">
                <div class="ag-bar-fill" style="width:{confidence}%;background:{grad};"></div>
            </div>
            <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(164,240,0,0.15);">
                <p class="ag-insight" style="margin-bottom: 0;">{insight}</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    @staticmethod
    def render_solution_card(remedy: str):
        """Directly render solution card"""
        st.markdown(f'''
        <div class="ag-card" style="--card-accent:#2ef2e2;">
            <div class="ag-card-hdr">
                <span class="ag-icon">🌱</span>
                Suggested Solution
            </div>
            <p class="ag-remedy">{remedy}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    @staticmethod
    def render_ai_card(ai_advice: str):
        """Directly render AI advisory card"""
        st.markdown(f'''
        <div class="ag-card" style="--card-accent:#A4F000;">
            <div class="ag-card-hdr">
                <span class="ag-icon">🤖</span>
                AI Advisory
            </div>
            <p class="ag-remedy">{ai_advice}</p>
        </div>
        ''', unsafe_allow_html=True)


# ==============================================
# RESULT PROCESSOR
# ==============================================

class ResultProcessor:
    """Process and format analysis results"""
    
    @staticmethod
    def process_prediction(disease: str, confidence: int, remedy: str, ai_advice: str) -> Dict:
        """Process raw prediction into formatted result"""
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