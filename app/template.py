# template.py — Centralized Configuration & Reusable Components
# ==============================================================
# Single source of truth for:
# - App constants and thresholds
# - Severity logic and mappings
# - Reusable UI components
# - Text templates and messages
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
    # Severity thresholds (disease only, not healthy)
    high_confidence: int = 85      # > 85% = low severity
    medium_confidence: int = 60    # 60-85% = medium severity  
    low_confidence: int = 0        # < 60% = high severity
    
    # Healthy detection
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
# BUSINESS LOGIC (Reusable)
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
        """Get accent color based on severity"""
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
        """Get CSS badge class for severity"""
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
    """Reusable UI component builder"""
    
    @staticmethod
    def render_result_card(
        title: str,
        icon: str,
        content_html: str,
        accent_color: str,
    ):
        """Render a standardized result card"""
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
        UIComponents.render_result_card(
            title=title,
            icon=icon,
            content_html=f'<p class="ag-empty">{placeholder}</p>',
            accent_color=UIColors.dim,
        )
    
    @staticmethod
    def render_disease_card(disease: str, plant: str, severity: str, is_healthy: bool) -> str:
        """Generate disease card HTML content"""
        if is_healthy:
            return f'''
            <div class="ag-disease-ok">✓ {disease}</div>
            <div class="ag-plant">{plant}</div>
            <span class="ag-badge {SeverityCalculator.get_badge_class(severity)}">
                ● No Disease Detected
            </span>
            '''
        else:
            return f'''
            <div class="ag-disease">{disease}</div>
            <div class="ag-plant">{plant}</div>
            <span class="ag-badge {SeverityCalculator.get_badge_class(severity)}">
                ● Severity: {severity.upper()}
            </span>
            '''
    
    @staticmethod
    def render_confidence_card(confidence: int) -> str:
        """Generate confidence card HTML content"""
        from styles import bar_gradient
        grad = bar_gradient(confidence)
        return f'''
        <div class="ag-conf-row">
            <span class="ag-conf-lbl">Model Certainty</span>
            <span class="ag-conf-pct">{confidence}%</span>
        </div>
        <div class="ag-bar-track">
            <div class="ag-bar-fill" style="width:{confidence}%;background:{grad};"></div>
        </div>
        '''


# ==============================================
# RESULT PROCESSOR
# ==============================================

class ResultProcessor:
    """Process and format analysis results"""
    
    @staticmethod
    def process_prediction(disease: str, confidence: int, remedy: str, ai_advice: str) -> Dict:
        """Process raw prediction into formatted result"""
        # Handle confidence (if it's between 0-1, convert to percentage)
        confidence_pct = round(confidence * 100) if confidence <= 1 else confidence
        
        # Check if healthy
        is_healthy = any(
            keyword.lower() in disease.lower() 
            for keyword in Thresholds.healthy_keywords
        )
        
        # Calculate severity
        severity = SeverityCalculator.calculate(confidence_pct, is_healthy)
        
        # Extract plant name (handles formats like "Apple_Scab" or "Tomato___Healthy")
        if "_" in disease:
            plant = disease.split("_")[0]
        else:
            plant = disease.split()[0] if " " in disease else disease
        
        # Clean up plant name (remove any extra underscores)
        plant = plant.replace("___", " ").replace("__", " ")
        
        return {
            "disease": disease,
            "confidence": confidence_pct,
            "healthy": is_healthy,
            "severity": severity,
            "plant": plant,
            "insight": MessageTemplates.get_insight(disease, confidence_pct),
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