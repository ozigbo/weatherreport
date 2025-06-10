"""
Weather data fetcher module for the Weather Dashboard application.
Uses the Open-Meteo API to fetch weather data for specified locations.
"""

import logging
import pandas as pd
import requests
from timezonefinder import TimezoneFinder
import requests_cache
import openmeteo_requests
from retry_requests import retry
import json
from datetime import datetime
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize API client with caching (1-hour expiration)
# Temporarily disabled caching for testing
# requests_cache.install_cache('.cache', expire_after=3600)
openmeteo = openmeteo_requests.Client()

def create_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 503, 504),
    session=None,
):
    """Create a requests Session with retry strategy"""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def fetch_weather_data(latitude: float, longitude: float) -> tuple:
    """
    Fetch weather data from Open-Meteo API
    Returns: tuple(hourly_df, daily_df, timezone_str)
    """
    try:
        # Get timezone string for the location
        timezone_str = "auto"  # Let the API handle timezone conversion
        
        # API request parameters
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone_str,
            "hourly": [
                "temperature_2m",
                "precipitation_probability",
                "cloud_cover",
                "relative_humidity_2m",
                "wind_speed_180m",
                "dew_point_2m",
                "wind_gusts_10m",
                "surface_pressure",
                "pressure_msl",
                "weather_code"
            ],
            "daily": ["sunrise", "sunset"],
            "forecast_days": 7
        }
        
        logger.debug(f"Making API request to {url}")
        logger.debug(f"Request parameters: {params}")
        
        # Make API request
        response = requests.get(url, params=params)
        
        # Debug logging
        logger.debug(f"API Response Status Code: {response.status_code}")
        logger.debug(f"API Response Headers: {response.headers}")
        logger.debug(f"API Response Content: {response.text[:1000]}...")  # First 1000 chars
        
        # Check if request was successful
        if response.status_code != 200:
            logger.error(f"API request failed with status code {response.status_code}")
            logger.error(f"Error response: {response.text}")
            return None, None, None
            
        try:
            data = response.json()
            timezone_str = data.get('timezone', 'UTC')  # Get timezone from response
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response as JSON: {e}")
            logger.error(f"Raw response: {response.text}")
            return None, None, None
        
        logger.debug("Successfully received API response, processing data...")
        
        # Process hourly data
        hourly_df = pd.DataFrame({
            'time': pd.to_datetime(data['hourly']['time']),
            'temperature_2m': data['hourly']['temperature_2m'],
            'precipitation_probability': data['hourly']['precipitation_probability'],
            'cloud_cover': data['hourly']['cloud_cover'],
            'relative_humidity_2m': data['hourly']['relative_humidity_2m'],
            'wind_speed_180m': data['hourly']['wind_speed_180m'],
            'dew_point_2m': data['hourly']['dew_point_2m'],
            'wind_gusts_10m': data['hourly']['wind_gusts_10m'],
            'surface_pressure': data['hourly']['surface_pressure'],
            'pressure_msl': data['hourly']['pressure_msl'],
            'weather_code': data['hourly']['weather_code']
        })
        
        # Process daily data for sunrise/sunset
        daily_df = pd.DataFrame({
            'date': pd.to_datetime(data['daily']['time']),
            'sunrise': pd.to_datetime(data['daily']['sunrise']),
            'sunset': pd.to_datetime(data['daily']['sunset'])
        })
        
        # Localize all timestamps to the correct timezone from the API
        hourly_df['time'] = hourly_df['time'].dt.tz_localize(timezone_str)
        daily_df['date'] = daily_df['date'].dt.tz_localize(timezone_str)
        daily_df['sunrise'] = daily_df['sunrise'].dt.tz_localize(timezone_str)
        daily_df['sunset'] = daily_df['sunset'].dt.tz_localize(timezone_str)
        
        return hourly_df, daily_df, timezone_str
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return None, None, None
    except KeyError as e:
        logger.error(f"Data parsing error - missing key: {str(e)}")
        return None, None, None
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return None, None, None

# --------------------------
# Main Entry Point
# --------------------------
def main():
    # Berlin coordinates
    latitude = 52.52
    longitude = 13.41
    fetch_weather_data(latitude, longitude)

if __name__ == "__main__":
    main() 