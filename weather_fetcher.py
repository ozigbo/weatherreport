import logging
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry

# Set pandas display options to show all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 5)

# --------------------------
# Logging Configuration
# --------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='msba_weather_app.log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# --------------------------
# Weather Fetching Function
# --------------------------
def fetch_weather_data(latitude, longitude):
    try:
        # Setup cached session and retry strategy
        cache_session = requests_cache.CachedSession('.cache', expire_after=86400)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Define API endpoint and parameters
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "precipitation_probability", "cloud_cover", "relative_humidity_2m",
                "wind_speed_180m", "dew_point_2m", "wind_gusts_10m",
                "surface_pressure", "pressure_msl", "weather_code"
            ]
        }

        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        logger.info(f"Fetched data for {latitude}, {longitude}")

        # Display metadata
        print(f"Coordinates: {response.Latitude()}°N, {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"UTC Offset: {response.UtcOffsetSeconds()} seconds")

        # Process hourly data
        hourly = response.Hourly()
        variable_names = [
            "precipitation_probability", "cloud_cover", "relative_humidity_2m",
            "wind_speed_180m", "dew_point_2m", "wind_gusts_10m",
            "surface_pressure", "pressure_msl", "weather_code"
        ]

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )
        }

        for i, name in enumerate(variable_names):
            hourly_data[name] = hourly.Variables(i).ValuesAsNumpy()

        df = pd.DataFrame(data=hourly_data)
        # Display selected columns in a more readable format
        print("\nWeather Forecast:")
        print(df[['date', 'precipitation_probability', 'cloud_cover', 'relative_humidity_2m', 'weather_code']].head())
        return df

    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        print(f"Failed to fetch weather data: {e}")
        return None

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