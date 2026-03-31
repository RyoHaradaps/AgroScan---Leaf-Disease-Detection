REMEDIES = {
    "Cotton_Bacterial_blight": "Use copper-based fungicides. Avoid overhead irrigation.",
    "Cotton_Curl_virus": "Control whiteflies using neem oil or insecticides.",
    "Cotton_Fusarium_wilt": "Use resistant varieties and improve soil drainage.",

    "Pepper_Bacterial_spot": "Apply copper sprays. Remove infected leaves.",
    
    "Potato_Early_blight": "Use fungicides like chlorothalonil.",
    "Potato_Late_blight": "Use mancozeb or metalaxyl sprays.",

    "Rice_Diseased": "Apply appropriate fungicide. Maintain proper water control.",

    "Tomato_Early_blight": "Use crop rotation and fungicides.",
    "Tomato_Late_blight": "Apply copper fungicides immediately.",

    "default": "Maintain proper field hygiene and monitor regularly."
}

def get_remedy(disease):
    return REMEDIES.get(disease, REMEDIES["default"])