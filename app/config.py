# config.py — Central Configuration for AgroScan
# ==============================================
# Single source of truth for all colors, thresholds, and app settings
# Change anything here and it will reflect throughout the application

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AppColors:
    """Centralized color definitions - Change colors here only"""
    
    # ===== Primary Accent Colors =====
    LIME: str = "#a4f000"      # Primary accent (greenish-yellow)
    TEAL: str = "#2ef2e2"      # Secondary accent (cyan/teal)
    WARN: str = "#ffb347"      # Warning color (orange)
    DANGER: str = "#ff5c6a"    # Danger/error color (red)
    OK: str = "#5efa5e"        # Success/healthy color (green)
    
    # ===== Background & Borders =====
    BG_ROOT: str = "#060d10"   # Main background (very dark)
    BORDER: str = "#14303f"    # Subtle border (dark teal)
    BORDER_HI: str = "#1d4a5c" # Highlight border (lighter teal)
    
    # ===== Text Colors =====
    MID: str = "#4a8a7a"       # Mid-tone text (muted teal)
    DIM: str = "#1e4a3a"       # Dim text (dark green-teal)
    WHITE: str = "#e8f4f0"     # White text (off-white)
    
    # ===== Weather Card Specific =====
    TEMP_HIGH: str = "#ffb347"      # Temperature high warning
    TEMP_LOW: str = "#4a8a7a"       # Temperature low warning
    TEMP_IDEAL: str = "#5efa5e"     # Temperature ideal
    HUMIDITY_HIGH: str = "#ffb347"  # Humidity high warning
    HUMIDITY_LOW: str = "#4a8a7a"   # Humidity low warning
    HUMIDITY_IDEAL: str = "#5efa5e" # Humidity ideal
    
    # ===== Suitability Colors =====
    SUITABILITY_EXCELLENT: str = "#5efa5e"
    SUITABILITY_GOOD: str = "#a4f000"
    SUITABILITY_MODERATE: str = "#ffb347"
    SUITABILITY_POOR: str = "#ff5c6a"
    
    # ===== Card Accents =====
    CARD_ACCENT_LOW: str = "#a4f000"
    CARD_ACCENT_MEDIUM: str = "#ffb347"
    CARD_ACCENT_HIGH: str = "#ff5c6a"
    CARD_ACCENT_HEALTHY: str = "#5efa5e"
    CARD_ACCENT_SOLUTION: str = "#2ef2e2"
    CARD_ACCENT_AI: str = "#A4F000"
    
    # ===== Progress Bar Gradients =====
    PROGRESS_HIGH: Tuple[str, str] = ("#2ecc71", "#a4f000")
    PROGRESS_MEDIUM: Tuple[str, str] = ("#ffb347", "#ffd166")
    PROGRESS_LOW: Tuple[str, str] = ("#ff5c6a", "#ff8c69")


@dataclass(frozen=True)
class AppFonts:
    """Centralized font definitions"""
    PRIMARY: str = "Orbitron"
    SECONDARY: str = "Syne"
    MONO: str = "JetBrains Mono"
    
    URL: str = (
        "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900"
        "&family=Syne:wght@400;500;600;700"
        "&family=JetBrains+Mono:wght@300;400;500&display=swap"
    )


@dataclass(frozen=True)
class AppThresholds:
    """Centralized threshold values"""
    CONFIDENCE_HIGH: int = 85
    CONFIDENCE_MEDIUM: int = 60
    CONFIDENCE_LOW: int = 0
    
    SUITABILITY_EXCELLENT: int = 80
    SUITABILITY_GOOD: int = 60
    SUITABILITY_MODERATE: int = 40
    
    HEALTHY_KEYWORDS: Tuple[str, ...] = ("Healthy", "health", "good condition")


@dataclass(frozen=True)
class AppLayout:
    """Centralized layout configuration"""
    LEFT_COLUMN_RATIO: float = 0.42
    RIGHT_COLUMN_RATIO: float = 0.58
    
    ALLOWED_FORMATS: Tuple[str, ...] = ("jpg", "jpeg", "png")
    MAX_FILE_SIZE_MB: int = 10


@dataclass(frozen=True)
class WeatherConfig:
    """Weather service configuration"""
    WTTR_URL: str = "https://wttr.in"
    POSTAL_API_URL: str = "https://api.postalpincode.in/pincode"
    IPAPI_URL: str = "https://ipapi.co/json/"
    TIMEOUT_SECONDS: int = 10