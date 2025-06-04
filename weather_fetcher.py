import logging
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
import requests

# Set pandas display options to show all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 5)

# --------------------------
# Logging Configuration
# --------------------------
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the cache with a 1-hour expiration
requests_cache.install_cache('.cache', expire_after=3600)

# Setup the Open-Meteo API client with cache
openmeteo = openmeteo_requests.Client()

# --------------------------
# Weather Fetching Function
# --------------------------
def fetch_weather_data(latitude, longitude):
    """
    Fetch weather data from OpenMeteo API for a given location
    """
    print("\n=== Weather Fetcher Debug ===")
    print(f"Fetching weather data for: {latitude}, {longitude}")
    
    try:
        # Get timezone for the location
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
        if not timezone_str:
            timezone_str = "UTC"
        
        print(f"Using timezone: {timezone_str}")
        
        # Make API request
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone_str,  # Use location's timezone
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
            "daily": ["sunrise", "sunset"],  # Request daily sunrise/sunset times
            "forecast_days": 7,
            "current_weather": True
        }
        
        print("Making API request...")
        print(f"URL: {url}")
        print(f"Parameters: {params}")
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        print("API request successful!")
        
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
        
        # Add timezone information to hourly data
        hourly_df['time'] = hourly_df['time'].dt.tz_localize(timezone_str)
        
        # Process daily data with sunrise/sunset times
        daily_df = pd.DataFrame({
            'date': pd.to_datetime(data['daily']['time']),
            'sunrise': pd.to_datetime(data['daily']['sunrise']),
            'sunset': pd.to_datetime(data['daily']['sunset'])
        })
        
        # Convert sunrise/sunset times to datetime with timezone
        daily_df['sunrise'] = daily_df['sunrise'].dt.tz_localize(timezone_str)
        daily_df['sunset'] = daily_df['sunset'].dt.tz_localize(timezone_str)
        
        print("\nFirst day data:")
        print(f"Date: {daily_df['date'].iloc[0]}")
        print(f"Sunrise: {daily_df['sunrise'].iloc[0]}")
        print(f"Sunset: {daily_df['sunset'].iloc[0]}")
        
        print("=== End Weather Fetcher Debug ===\n")
        
        return hourly_df, daily_df
        
    except Exception as e:
        print(f"Error fetching weather data: {str(e)}")
        print(f"Response data: {data if 'data' in locals() else 'No data received'}")
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