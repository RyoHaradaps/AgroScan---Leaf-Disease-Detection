# weather_service.py — Weather API Integration for AgroScan
# ==========================================================
# Handles weather data fetching from various free APIs
# Supports pincode and city name lookups for Indian locations

import requests
import streamlit as st
from datetime import datetime


class WeatherService:
    """Weather service for Indian locations using free APIs (wttr.in and postalpincode.in)"""
    
    @staticmethod
    def get_city_from_pincode(pincode: str) -> str:
        """
        Get city/district name from Indian pincode using postalpincode.in API
        
        Args:
            pincode: 6-digit Indian postal code
            
        Returns:
            City/District name or None if not found
        """
        try:
            url = f"https://api.postalpincode.in/pincode/{pincode}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and data[0].get('Status') == 'Success':
                    post_offices = data[0].get('PostOffice', [])
                    if post_offices and len(post_offices) > 0:
                        # Try to get District, fallback to City, then State
                        city = post_offices[0].get('District', '')
                        if not city:
                            city = post_offices[0].get('City', '')
                        if not city:
                            city = post_offices[0].get('State', '')
                        return city
        except Exception:
            pass
        return None
    
    @staticmethod
    def get_weather_by_pincode(pincode: str) -> dict:
        """
        Fetch current weather data for a given Indian pincode
        
        Args:
            pincode: 6-digit Indian postal code
            
        Returns:
            Dictionary containing weather data (temp, humidity, location, etc.)
        """
        try:
            # wttr.in provides free weather data without API key
            url = f"https://wttr.in/{pincode}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                # Get location name from pincode API first
                location_name = WeatherService.get_city_from_pincode(pincode)
                
                # Fallback to wttr.in's nearest_area data if pincode API fails
                if not location_name:
                    nearest_area = data.get('nearest_area', [])
                    if nearest_area and len(nearest_area) > 0:
                        area = nearest_area[0]
                        area_names = area.get('areaName', [])
                        region_names = area.get('region', [])
                        if area_names and len(area_names) > 0:
                            location_name = area_names[0].get('value', '')
                        elif region_names and len(region_names) > 0:
                            location_name = region_names[0].get('value', '')
                
                # Final fallback
                if not location_name:
                    location_name = f"Location (Pincode: {pincode})"
                
                return {
                    "temp": int(current.get('temp_C', 0)),
                    "humidity": int(current.get('humidity', 0)),
                    "condition": current.get('weatherDesc', [{}])[0].get('value', 'Unknown'),
                    "wind_kph": int(current.get('windspeedKmph', 0)),
                    "pressure": int(current.get('pressure', 0)),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "location": location_name,
                    "pincode": pincode
                }
        except Exception as e:
            st.warning(f"Could not fetch weather for pincode {pincode}: {e}")
        
        # Return fallback data when API fails
        return WeatherService._get_fallback_weather(f"Pincode: {pincode}")
    
    @staticmethod
    def get_weather_by_city(city_name: str) -> dict:
        """
        Fetch current weather data for a given city name
        
        Args:
            city_name: Name of the city (e.g., "Mumbai", "Bangalore")
            
        Returns:
            Dictionary containing weather data (temp, humidity, location, etc.)
        """
        try:
            url = f"https://wttr.in/{city_name}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                # Extract actual location name from API response
                actual_location = city_name.title()
                nearest_area = data.get('nearest_area', [])
                if nearest_area and len(nearest_area) > 0:
                    area = nearest_area[0]
                    area_names = area.get('areaName', [])
                    if area_names and len(area_names) > 0:
                        actual_location = area_names[0].get('value', city_name)
                
                return {
                    "temp": int(current.get('temp_C', 0)),
                    "humidity": int(current.get('humidity', 0)),
                    "condition": current.get('weatherDesc', [{}])[0].get('value', 'Unknown'),
                    "wind_kph": int(current.get('windspeedKmph', 0)),
                    "pressure": int(current.get('pressure', 0)),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "location": actual_location,
                    "city": city_name
                }
        except Exception as e:
            st.warning(f"Could not fetch weather for city {city_name}: {e}")
        
        # Return fallback data when API fails
        return WeatherService._get_fallback_weather(city_name)
    
    @staticmethod
    def _get_fallback_weather(location_name: str = "Demo") -> dict:
        """
        Generate fallback weather data when API calls fail
        
        Args:
            location_name: Name to display for the location
            
        Returns:
            Dictionary with realistic default weather data
        """
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
    def get_user_location() -> dict:
        """
        Auto-detect user's location based on IP address
        
        Returns:
            Dictionary containing city, region, and pincode information
        """
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data.get('city', 'Unknown'),
                    "region": data.get('region', 'Unknown'),
                    "pincode": data.get('postal', 'Unknown')
                }
        except Exception:
            pass
        
        # Default fallback location
        return {"city": "Delhi", "region": "Delhi", "pincode": "110001"}