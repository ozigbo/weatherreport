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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize API client with caching (1-hour expiration)
requests_cache.install_cache('.cache', expire_after=3600)
openmeteo = openmeteo_requests.Client()

def fetch_weather_data(latitude: float, longitude: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetch weather data from OpenMeteo API for a given location.
    
    Args:
        latitude (float): Location latitude
        longitude (float): Location longitude
        
    Returns:
        tuple: (hourly_df, daily_df) containing weather data
            hourly_df: DataFrame with hourly weather metrics
            daily_df: DataFrame with daily sunrise/sunset times
    """
    try:
        # Get timezone for the location
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude) or "UTC"
        
        # API request parameters
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone_str,
            "hourly": [
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
            "forecast_days": 7,
            "current_weather": True
        }
        
        # Make API request
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Process hourly data
        hourly_df = pd.DataFrame({
            'time': pd.to_datetime(data['hourly']['time']),
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
        
        # Add timezone information
        hourly_df['time'] = hourly_df['time'].dt.tz_localize(timezone_str)
        
        # Process daily data
        daily_df = pd.DataFrame({
            'date': pd.to_datetime(data['daily']['time']),
            'sunrise': pd.to_datetime(data['daily']['sunrise']),
            'sunset': pd.to_datetime(data['daily']['sunset'])
        })
        
        # Add timezone information to sunrise/sunset
        daily_df['sunrise'] = daily_df['sunrise'].dt.tz_localize(timezone_str)
        daily_df['sunset'] = daily_df['sunset'].dt.tz_localize(timezone_str)
        
        return hourly_df, daily_df
        
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return None, None

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