# ai_advisor.py — AI Integration for AgroScan
# ==============================================
# Handles communication with Ollama for generating:
# - Structured treatment remedies (Suggested Solution card)
# - Detailed AI advisory (AI Advisory card)
# - Fallback static remedies when Ollama is unavailable

import requests
import streamlit as st

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral:latest"


def is_ollama_available() -> bool:
    """Check if Ollama is running and the model is available"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            
            # Check if our model exists
            for model in model_names:
                if OLLAMA_MODEL in model:
                    return True
            
            print(f"Warning: Model '{OLLAMA_MODEL}' not found. Available: {model_names}")
            return False
    except:
        print("Warning: Ollama server not running at http://localhost:11434")
    return False


def get_ai_remedy(disease: str) -> str:
    """Get structured treatment remedy from Ollama for the Suggested Solution card"""
    
    # Check if Ollama is available
    if not is_ollama_available():
        return get_fallback_remedy(disease)
    
    prompt = f"""You are an agricultural expert. Provide a comprehensive treatment plan for {disease} in the following EXACT format:


**Immediate Actions for Infected Plants**
- [First immediate action]
- [Second immediate action]
- [Third immediate action]

**Chemical Control**
- [First chemical/treatment option]
- [Second chemical/treatment option]
- [Rotation or organic advice]

**Preventive Cultural Practices**
- [First preventive practice]
- [Second preventive practice]
- [Third preventive practice]

Important rules:
- Each section MUST have the exact headers shown above with **bold** formatting
- Use dashes (-) for bullet points
- Keep each point concise and actionable
- Do not add any extra text before or after the format
- Write in simple, farmer-friendly language"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "top_p": 0.9,
                    "max_tokens": 800
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            remedy = response.json().get("response", "")
            if remedy and len(remedy) > 100:
                return remedy.strip()
            else:
                return get_fallback_remedy(disease)
        else:
            return get_fallback_remedy(disease)
            
    except Exception as e:
        print(f"Ollama error: {e}")
        return get_fallback_remedy(disease)


def get_ai_advice(disease: str, confidence: int) -> str:
    """Get educational AI advisory (KNOWLEDGE focused - not actions)"""
    
    # Check if Ollama is available
    if not is_ollama_available():
        return get_fallback_advice(disease, confidence)
    
    prompt = f"""You are an agricultural educator. Provide educational information about {disease} (detected with {confidence}% confidence) in the following EXACT format:

🔬 Understanding {disease.split('_')[0] if '_' in disease else disease} {disease.split('_')[1] if '_' in disease else 'Disease'}
[Write 2-3 sentences explaining what causes this disease and its scientific background]

🌧️ Favorable Conditions
• [Condition 1 that promotes disease development]
• [Condition 2 that promotes disease development]
• [Condition 3 that promotes disease development]

⚠️ Early Warning Signs
• [Sign 1 - visual symptom]
• [Sign 2 - visual symptom]
• [Sign 3 - visual symptom]

💡 Why Early Detection Matters
[Write 2 sentences explaining how quickly the disease spreads and why early action is critical]

Important rules:
- Use the exact emoji headers shown above (🔬, 🌧️, ⚠️, 💡)
- Use dashes (-) for bullet points under Favorable Conditions and Early Warning Signs
- Focus on EDUCATION (what, why, how it spreads), not actions
- Do NOT include treatment steps or prevention tips (those go in Suggested Solution card)
- Keep language simple and farmer-friendly
- Do not add any extra text before or after the format"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.6,
                    "top_p": 0.9,
                    "max_tokens": 600
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            advice = response.json().get("response", "")
            if advice and len(advice) > 100:
                return advice.strip()
            else:
                return get_fallback_advice(disease, confidence)
        else:
            return get_fallback_advice(disease, confidence)
            
    except Exception as e:
        print(f"Ollama error: {e}")
        return get_fallback_advice(disease, confidence)

def get_fallback_remedy(disease: str) -> str:
    """Fallback static remedies when Ollama is unavailable"""
    
    # Extract crop name from disease string
    crop = disease.split('_')[0] if '_' in disease else disease.split()[0]
    crop = crop.lower()
    
    remedies = {
        "potato": f"""**Immediate Actions for Infected Plants**
- Remove and destroy infected leaves and stems immediately
- Cut stems down to ground level if severely infected
- Wait 2-3 weeks before harvesting tubers to prevent tuber infection

**Chemical Control**
- Apply copper-based fungicides as a preventative measure
- Use metalaxyl or mancozeb for active infections
- Rotate between different fungicide types to prevent resistance

**Preventive Cultural Practices**
- Plant resistant varieties like Kufri Moti, Kufri Surya
- Ensure proper plant spacing for good air circulation
- Avoid overhead irrigation, especially in evenings""",
        
        "tomato": f"""**AI-generated overview**
{disease} spreads rapidly in wet, cool conditions. Early detection and treatment are critical for saving your crop.

**Immediate Actions for Infected Plants**
- Remove affected leaves and fruits immediately
- Destroy infected plant material away from the garden
- Improve air circulation by pruning lower leaves

**Chemical Control**
- Apply chlorothalonil or copper fungicides preventively
- Use mancozeb as a treatment for active infections
- Spray every 7-10 days during wet weather

**Preventive Cultural Practices**
- Water at the base of plants, not on leaves
- Stake or cage plants for better airflow
- Practice 3-year crop rotation""",
        
        "rice": f"""**AI-generated overview**
{disease} are fungal diseases that thrive in humid conditions with dense planting.

**Immediate Actions for Infected Plants**
- Remove and destroy infected leaves and tillers
- Reduce nitrogen fertilizer application
- Drain fields temporarily to reduce humidity

**Chemical Control**
- Apply tricyclazole or isoprothiolane for blast control
- Use validamycin or hexaconazole for sheath blight
- Follow local recommendations for fungicide application

**Preventive Cultural Practices**
- Use resistant varieties like IR64, Swarna
- Plant at recommended spacing
- Avoid excessive nitrogen fertilizer""",
        
        "cotton": f"""**AI-generated overview**
{disease} require integrated management for effective control.

**Immediate Actions for Infected Plants**
- Remove and destroy infected plants immediately
- Control whiteflies to prevent curl virus spread
- Avoid working in fields when plants are wet

**Chemical Control**
- Use imidacloprid for whitefly control
- Apply copper oxychloride for bacterial blight
- Use carbendazim or thiophanate-methyl for wilt management

**Preventive Cultural Practices**
- Plant disease-resistant varieties
- Maintain proper plant spacing
- Practice crop rotation with non-host crops""",
        
        "pepper": f"""**AI-generated overview**
{disease} causes dark lesions on leaves and fruits, spreading rapidly in warm, humid conditions.

**Immediate Actions for Infected Plants**
- Remove and destroy infected leaves and fruits
- Avoid overhead irrigation
- Disinfect tools after working with infected plants

**Chemical Control**
- Apply copper-based bactericides preventively
- Use streptomycin or kasugamycin for active infections
- Combine with mancozeb for better control

**Preventive Cultural Practices**
- Use disease-free seeds and transplants
- Practice 2-3 year crop rotation
- Maintain good air circulation through proper spacing""",
    }
    
    # Try to find matching crop
    for key, value in remedies.items():
        if key in crop:
            return value
    
    # Default fallback for unknown crops
    return f"""**AI-generated overview**
{disease} requires prompt attention and proper management to prevent crop loss.

**Immediate Actions for Infected Plants**
- Remove and destroy infected plant parts immediately
- Clean tools after handling infected plants
- Isolate infected plants if possible

**Chemical Control**
- Consult your local agricultural extension for recommended treatments
- Apply appropriate fungicides or bactericides as per label instructions
- Consider organic alternatives like neem oil or copper sprays

**Preventive Cultural Practices**
- Practice crop rotation (2-3 years)
- Maintain proper plant spacing for air circulation
- Water at the base of plants, avoid wetting leaves"""


def get_fallback_advice(disease: str, confidence: int) -> str:
    """Fallback educational advice when Ollama is unavailable"""
    
    crop = disease.split('_')[0] if '_' in disease else disease.split()[0]
    
    fallbacks = {
        "Potato": f"""🔬 Understanding Potato {disease.split('_')[1] if '_' in disease else 'Disease'}
This disease is caused by a fungal pathogen that thrives in humid conditions. It's one of the most destructive diseases affecting potato crops worldwide.

🌧️ Favorable Conditions
• Temperatures between 15-20°C (59-68°F)
• High humidity above 90%
• Leaves remaining wet for 6+ hours
• Cool nights with morning dew

⚠️ Early Warning Signs
• Dark, water-soaked lesions on leaves
• White, fuzzy growth on leaf undersides
• Brown, rotting spots on tubers
• Rapid spread during wet weather

💡 Why Early Detection Matters
This disease can destroy an entire field in 7-10 days under ideal conditions. Spores travel through wind and can infect fields miles away from the source.""",

        "Tomato": f"""🔬 Understanding Tomato {disease.split('_')[1] if '_' in disease else 'Disease'}
This is a fungal disease that spreads rapidly in wet, warm conditions. It affects both leaves and fruits, causing significant yield loss.

🌧️ Favorable Conditions
• Temperatures between 18-25°C (64-77°F)
• Prolonged leaf wetness
• High humidity above 85%
• Overcrowded planting

⚠️ Early Warning Signs
• Small dark spots on lower leaves
• Yellow halos around leaf spots
• Sunken lesions on fruits
• Defoliation starting from bottom

💡 Why Early Detection Matters
Once symptoms appear, the disease can spread to the entire plant within days. Early detection allows for better management and prevents crop loss.""",

        "Rice": f"""🔬 Understanding Rice Disease
This fungal disease is prevalent in dense, humid rice paddies. It can cause significant yield reduction if not identified early.

🌧️ Favorable Conditions
• High nitrogen fertilizer use
• Dense planting
• High humidity above 90%
• Temperatures between 25-30°C

⚠️ Early Warning Signs
• Gray-green lesions on leaves
• White or gray centers with brown borders
• Infected panicles (neck blast)
• Premature drying of plants

💡 Why Early Detection Matters
The disease spreads rapidly through water splashes and wind. Early detection helps in adjusting nitrogen levels and water management.""",
    }
    
    for key, value in fallbacks.items():
        if key in crop:
            return value
    
    # Default fallback
    return f"""🔬 Understanding {disease}
This is a common agricultural disease that requires proper understanding for effective management.

🌧️ Favorable Conditions
• High humidity and moisture
• Poor air circulation
• Stress on plants
• Warm to moderate temperatures

⚠️ Early Warning Signs
• Unusual spots or lesions on leaves
• Discoloration of plant tissue
• Wilting or stunted growth
• Unusual patterns on fruits or tubers

💡 Why Early Detection Matters
Early detection of plant diseases is crucial for effective management. Most diseases spread quickly under favorable conditions, and early intervention can save your crop."""

def test_ollama_connection() -> bool:
    """Test if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            st.success(f"✅ Ollama connected! Available models: {[m['name'] for m in models]}")
            return True
    except:
        st.error("❌ Cannot connect to Ollama. Please run 'ollama serve' in terminal")
    return False