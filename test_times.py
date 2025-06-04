from datetime import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
from weather_fetcher import fetch_weather_data

print("=== Testing timezone conversion ===")
# Test New York coordinates
lat, lon = 40.71, -74.01

# Get timezone
tf = TimezoneFinder()
timezone_str = tf.timezone_at(lat=lat, lng=lon)
print(f"\nTimezone for New York: {timezone_str}")

# Get actual weather data
print("\nFetching actual weather data...")
df, daily_df = fetch_weather_data(lat, lon)

if daily_df is not None:
    print("\nActual sunrise/sunset times from API:")
    today_data = daily_df.iloc[0]
    
    # Get raw UTC times
    sunrise_utc = today_data['sunrise']
    sunset_utc = today_data['sunset']
    print(f"Raw sunrise (UTC): {sunrise_utc}")
    print(f"Raw sunset (UTC): {sunset_utc}")
    
    # Convert to NY time
    ny_tz = ZoneInfo(timezone_str)
    sunrise_ny = sunrise_utc.tz_convert(ny_tz)
    sunset_ny = sunset_utc.tz_convert(ny_tz)
    print(f"\nConverted to NY time:")
    print(f"Sunrise (NY): {sunrise_ny}")
    print(f"Sunset (NY): {sunset_ny}")
    
    # Format times
    sunrise_str = sunrise_ny.strftime('%I:%M %p').lstrip('0')
    sunset_str = sunset_ny.strftime('%I:%M %p').lstrip('0')
    print(f"\nFormatted times:")
    print(f"Sunrise: {sunrise_str}")
    print(f"Sunset: {sunset_str}")
else:
    print("Failed to fetch weather data")

# Create a test timestamp (7 PM UTC)
test_time_utc = datetime.now(tz=ZoneInfo("UTC")).replace(hour=19, minute=0)
print(f"\nTest time (UTC): {test_time_utc}")

# Convert to New York time
ny_tz = ZoneInfo(timezone_str)
test_time_ny = test_time_utc.astimezone(ny_tz)
print(f"Test time (New York): {test_time_ny}")

# Format the time like we do in the app
formatted_time = test_time_ny.strftime('%I:%M %p').lstrip('0')
print(f"Formatted time: {formatted_time}")

# Let's also test a morning time (7 AM UTC)
test_time_utc = datetime.now(tz=ZoneInfo("UTC")).replace(hour=7, minute=0)
print(f"\nMorning test time (UTC): {test_time_utc}")
test_time_ny = test_time_utc.astimezone(ny_tz)
print(f"Morning test time (New York): {test_time_ny}")
formatted_time = test_time_ny.strftime('%I:%M %p').lstrip('0')
print(f"Formatted morning time: {formatted_time}") 