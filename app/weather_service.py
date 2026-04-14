# weather_service.py
import requests
import streamlit as st
from datetime import datetime

class WeatherService:
    """Simple weather service for Indian locations"""
    
    @staticmethod
    def get_city_from_pincode(pincode):
        """Get city name from pincode using free API"""
        try:
            # Using postalpincode.in API (free, no key required)
            url = f"https://api.postalpincode.in/pincode/{pincode}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and data[0]['Status'] == 'Success':
                    # Get the first post office's district/city
                    post_offices = data[0]['PostOffice']
                    if post_offices and len(post_offices) > 0:
                        city = post_offices[0].get('District', '')
                        if not city:
                            city = post_offices[0].get('City', '')
                        if not city:
                            city = post_offices[0].get('State', '')
                        return city
        except:
            pass
        return None
    
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
                
                # Try to get location name from pincode API
                location_name = WeatherService.get_city_from_pincode(pincode)
                
                # If no location name found from API, try from wttr.in response
                if not location_name:
                    if 'nearest_area' in data and len(data['nearest_area']) > 0:
                        area = data['nearest_area'][0]
                        if 'areaName' in area and len(area['areaName']) > 0:
                            location_name = area['areaName'][0]['value']
                        elif 'region' in area and len(area['region']) > 0:
                            location_name = area['region'][0]['value']
                
                # If still no location name, use the pincode
                if not location_name:
                    location_name = f"Location"
                
                return {
                    "temp": int(current['temp_C']),
                    "humidity": int(current['humidity']),
                    "condition": current['weatherDesc'][0]['value'],
                    "wind_kph": int(current['windspeedKmph']),
                    "pressure": int(current['pressure']),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "location": location_name,
                    "pincode": pincode  # Always include the pincode
                }
        except Exception as e:
            st.warning(f"Could not fetch weather: {e}")
        
        # Fallback data (for demo/offline)
        return WeatherService._get_fallback_weather(pincode)
    
    @staticmethod
    def get_weather_by_city(city_name):
        """Get weather by city name"""
        try:
            url = f"https://wttr.in/{city_name}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                # Get the actual city name from response
                actual_location = city_name
                if 'nearest_area' in data and len(data['nearest_area']) > 0:
                    area = data['nearest_area'][0]
                    if 'areaName' in area and len(area['areaName']) > 0:
                        actual_location = area['areaName'][0]['value']
                
                return {
                    "temp": int(current['temp_C']),
                    "humidity": int(current['humidity']),
                    "condition": current['weatherDesc'][0]['value'],
                    "wind_kph": int(current['windspeedKmph']),
                    "pressure": int(current['pressure']),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "location": actual_location,
                    "city": city_name  # Include the original city name
                }
        except Exception as e:
            st.warning(f"Could not fetch weather: {e}")
        
        return WeatherService._get_fallback_weather(city_name)
    
    @staticmethod
    def _get_fallback_weather(location_name="Demo"):
        """Fallback weather data when API fails"""
        return {
            "temp": 28,
            "humidity": 65,
            "condition": "Partly Cloudy",
            "wind_kph": 12,
            "pressure": 1013,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": location_name if location_name else "Demo Location"
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