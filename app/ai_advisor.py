import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_ai_advice(disease, confidence):
    prompt = f"""
You are an agricultural expert.

A plant disease has been detected:
Disease: {disease}
Confidence: {confidence}%

Explain in simple terms:
1. What is this disease?
2. Why does it occur?
3. Step-by-step treatment
4. Prevention tips

Keep it practical for farmers. Avoid technical jargon.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "AI advice not available."