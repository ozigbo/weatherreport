"""
Weather code mappings based on WMO (World Meteorological Organization) codes.
Each code maps to a tuple of (description, suggested_icon_name)
"""

WEATHER_CODES = {
    0: ("Clear sky", "sun"),
    1: ("Mainly clear", "sun-cloud"),
    2: ("Partly cloudy", "sun-cloud"),
    3: ("Overcast", "cloud"),
    45: ("Foggy", "fog"),
    48: ("Depositing rime fog", "fog"),
    51: ("Light drizzle", "drizzle"),
    53: ("Moderate drizzle", "drizzle"),
    55: ("Dense drizzle", "drizzle"),
    56: ("Light freezing drizzle", "sleet"),
    57: ("Dense freezing drizzle", "sleet"),
    61: ("Slight rain", "rain"),
    63: ("Moderate rain", "rain"),
    65: ("Heavy rain", "heavy-rain"),
    66: ("Light freezing rain", "sleet"),
    67: ("Heavy freezing rain", "sleet"),
    71: ("Slight snow fall", "snow"),
    73: ("Moderate snow fall", "snow"),
    75: ("Heavy snow fall", "heavy-snow"),
    77: ("Snow grains", "snow"),
    80: ("Slight rain showers", "rain"),
    81: ("Moderate rain showers", "rain"),
    82: ("Violent rain showers", "heavy-rain"),
    85: ("Slight snow showers", "snow"),
    86: ("Heavy snow showers", "heavy-snow"),
    95: ("Thunderstorm", "thunder"),
    96: ("Thunderstorm with slight hail", "thunder-hail"),
    99: ("Thunderstorm with heavy hail", "thunder-hail")
}

def get_weather_info(code):
    """
    Get weather description and icon name for a given weather code.
    
    Args:
        code (int): WMO weather code
        
    Returns:
        tuple: (description, icon_name) or ("Unknown", "question") if code not found
    """
    return WEATHER_CODES.get(code, ("Unknown", "question")) 