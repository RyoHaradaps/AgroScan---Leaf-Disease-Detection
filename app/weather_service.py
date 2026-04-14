# weather_service.py
import requests
import streamlit as st
from datetime import datetime

class WeatherService:
    """Simple weather service for Indian locations"""
    
    @staticmethod
    def get_weather_by_pincode(pincode):
        """Get weather using Indian pincode"""
        try:
            # Using wttr.in for free weather (no API key needed)
            url = f"https://wttr.in/{pincode}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                return {
                    "temp": int(current['temp_C']),
                    "humidity": int(current['humidity']),
                    "condition": current['weatherDesc'][0]['value'],
                    "wind_kph": int(current['windspeedKmph']),
                    "pressure": int(current['pressure']),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception as e:
            st.warning(f"Could not fetch weather: {e}")
        
        # Fallback data (for demo/offline)
        return WeatherService._get_fallback_weather()
    
    @staticmethod
    def get_weather_by_city(city_name):
        """Get weather by city name"""
        try:
            url = f"https://wttr.in/{city_name}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                return {
                    "temp": int(current['temp_C']),
                    "humidity": int(current['humidity']),
                    "condition": current['weatherDesc'][0]['value'],
                    "wind_kph": int(current['windspeedKmph']),
                    "pressure": int(current['pressure']),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "location": city_name
                }
        except Exception as e:
            st.warning(f"Could not fetch weather: {e}")
        
        return WeatherService._get_fallback_weather()
    
    @staticmethod
    def _get_fallback_weather():
        """Fallback weather data when API fails"""
        return {
            "temp": 28,
            "humidity": 65,
            "condition": "Partly Cloudy",
            "wind_kph": 12,
            "pressure": 1013,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": "Unknown (using demo data)"
        }
    
    @staticmethod
    def get_user_location():
        """Get user's location based on IP (optional)"""
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data.get('city', 'Unknown'),
                    "region": data.get('region', 'Unknown'),
                    "pincode": data.get('postal', 'Unknown')
                }
        except:
            pass
        return {"city": "Delhi", "region": "Delhi", "pincode": "110001"}