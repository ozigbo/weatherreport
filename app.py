from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_daq as daq
from weather_fetcher import fetch_weather_data
from weather_codes import get_weather_info
from datetime import datetime, timedelta
import time
import plotly.graph_objects as go
import pandas as pd
import pytz
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo

# Add timestamp for cache busting
current_timestamp = int(time.time())

# Initialize the Dash app with a modern theme and Font Awesome
app = Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        'https://use.fontawesome.com/releases/v5.15.4/css/all.css',
        'https://fonts.googleapis.com/css2?family=Courier+Prime&family=DM+Serif+Display&display=swap'
    ]
)

# Custom CSS for the components
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .current-weather-card {
                background-color: #f5f5dc;
                border: 2px solid #000080;
                border-radius: 15px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                width: 300px;
            }

            .current-weather-title {
                font-family: 'DM Serif Display', serif;
                font-size: 1rem;
                letter-spacing: 0.1em;
                color: #000080;
                margin-bottom: 1rem;
                text-transform: uppercase;
            }

            .current-weather-location {
                font-family: 'DM Serif Display', serif;
                font-size: 2rem;
                color: #333;
                margin-bottom: 1rem;
            }

            .current-weather-main {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1.5rem;
            }

            .current-weather-temp {
                font-family: 'Courier Prime', monospace;
                font-size: 3.5rem;
                font-weight: bold;
                color: #333;
            }

            .current-weather-icon {
                width: 64px;
                height: 64px;
            }

            .current-weather-details {
                display: flex;
                justify-content: space-between;
                font-family: 'Courier Prime', monospace;
                color: #666;
                padding-top: 1rem;
                border-top: 1px solid #000080;
            }

            .current-weather-detail-item {
                text-align: center;
            }

            .detail-label {
                font-size: 0.8rem;
                margin-bottom: 0.25rem;
            }

            .detail-value {
                font-size: 1.1rem;
                color: #333;
            }

            /* Weekly Forecast Styles */
            .forecast-section {
                width: 50%;
            }

            .forecast-card {
                background-color: #f5f5dc;
                border: 2px solid #000080;
                border-radius: 15px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                width: 100%;  /* Ensure full width */
            }

            .forecast-header {
                font-family: 'DM Serif Display', serif;
                font-size: 1rem;
                letter-spacing: 0.2em;
                color: #000080;
                margin-bottom: 1rem;
                text-transform: uppercase;
                text-align: left;
            }

            .forecast-row {
                display: flex;
                flex-wrap: nowrap !important;
                margin: 0;
                gap: 1rem;  /* Add space between day cards */
            }

            .day-col {
                flex: 1;
                min-width: 0;
                padding: 0.5rem;
            }

            .day-card {
                text-align: center;
                padding: 0.5rem;
                font-family: 'Courier Prime', monospace;
            }

            .day-name {
                font-family: 'DM Serif Display', serif;
                font-size: 1rem;
                margin-bottom: 0.25rem;
            }

            .weather-icon {
                width: 48px;
                height: 48px;
                margin: 0.25rem auto;
                display: block;
            }

            .high-temp {
                font-size: 1.4rem;
                font-weight: bold;
                margin: 0.25rem 0;
            }

            .low-temp {
                font-size: 1rem;
                color: #666;
            }

            .temp-toggle-container {
                text-align: center;
                font-family: 'Courier Prime', monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                padding: 10px;
            }

            .temp-toggle-options {
                display: flex;
                justify-content: center;
                gap: 60px;  /* Space between the two option columns */
            }

            .temp-option {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;  /* Space between label and radio button */
            }

            /* Retro radio button styling */
            .temp-toggle-container input[type="radio"] {
                appearance: none;
                width: 24px;
                height: 24px;
                border: 2px solid #8b4513;
                border-radius: 50%;
                position: relative;
                cursor: pointer;
            }

            .temp-toggle-container input[type="radio"]:checked {
                border-color: #8b4513;
                background-color: #f5f5dc;
            }

            .temp-toggle-container input[type="radio"]:checked::after {
                content: '';
                width: 12px;
                height: 12px;
                background: #8b4513;
                border-radius: 50%;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }

            .unit-label {
                font-size: 1.2rem;
                color: #8b4513;
            }

            .current-weather-card.forecast {
                width: 100%;
                min-width: 600px;  /* Ensure minimum width for readability */
            }

            .precipitation-card {
                margin-top: 1.5rem;
                width: 100%;  /* Ensure full width */
            }

            .precipitation-graph {
                background-color: #f5f5dc;
                border-radius: 15px;
                padding: 1rem;
                width: 100%;  /* Ensure full width */
            }

            .sunrise-sunset-card {
                background-color: #f5f5dc;
                border: 2px solid #000080;
                border-radius: 15px;
                padding: 2.5rem 1.5rem;  /* Increased top/bottom padding */
                margin-top: 1.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                min-height: 250px;  /* Increased to accommodate larger icons */
            }

            .sun-divider {
                width: 2px;
                height: 160px;  /* Increased to match new icon size */
                background-color: #000080;
                opacity: 0.3;
                margin: 0 1rem;
            }

            .sun-section {
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 1rem;  /* Increased from 0.5rem for better spacing */
                padding: 0.5rem;  /* Added padding for breathing room */
            }

            .sun-label {
                font-family: 'DM Serif Display', serif;
                font-size: 1.2rem;  /* Increased from 1rem */
                letter-spacing: 0.2em;
                color: #000080;
                margin-bottom: 0.5rem;
                text-align: center;  /* Ensure centered text */
            }

            .sun-time {
                font-family: 'Courier Prime', monospace;
                font-size: 2.2rem;  /* Increased from 2rem */
                font-weight: bold;
                color: #000080;
                text-align: center;  /* Ensure centered text */
            }

            .sun-icon {
                width: 96px;  /* Increased from 64px to 96px (50% larger) */
                height: 96px; /* Increased from 64px to 96px (50% larger) */
                margin-bottom: 1rem;
                object-fit: contain;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define cities grouped by country
cities_by_country = {
    'United States': {
        'Akron': (41.08, -81.52),
        'Albany': (42.65, -73.75),
        'Albuquerque': (35.08, -106.65),
        'Amarillo': (35.22, -101.83),
        'Anaheim': (33.84, -117.91),
        'Anchorage': (61.22, -149.90),
        'Ann Arbor': (42.28, -83.74),
        'Arlington TX': (32.74, -97.11),
        'Arlington VA': (38.88, -77.10),
        'Atlanta': (33.75, -84.39),
        'Augusta': (33.47, -81.97),
        'Aurora CO': (39.73, -104.83),
        'Austin': (30.27, -97.74),
        'Bakersfield': (35.37, -119.02),
        'Baltimore': (39.29, -76.61),
        'Baton Rouge': (30.45, -91.15),
        'Bellevue': (47.61, -122.20),
        'Berkeley': (37.87, -122.27),
        'Billings': (45.79, -108.54),
        'Birmingham': (33.52, -86.80),
        'Boise': (43.62, -116.21),
        'Boston': (42.36, -71.06),
        'Boulder': (40.01, -105.27),
        'Bridgeport': (41.19, -73.20),
        'Buffalo': (42.89, -78.88),
        'Burlington': (44.48, -73.21),
        'Cambridge': (42.37, -71.11),
        'Cape Coral': (26.56, -81.95),
        'Carlsbad': (33.16, -117.35),
        'Carrollton': (32.98, -96.89),
        'Cary': (35.79, -78.78),
        'Cedar Rapids': (41.98, -91.67),
        'Chandler': (33.31, -111.84),
        'Charleston': (32.78, -79.93),
        'Charlotte': (35.23, -80.84),
        'Chattanooga': (35.05, -85.31),
        'Chesapeake': (36.77, -76.29),
        'Chicago': (41.88, -87.63),
        'Chula Vista': (32.64, -117.08),
        'Cincinnati': (39.10, -84.51),
        'Cleveland': (41.50, -81.69),
        'Colorado Springs': (38.83, -104.82),
        'Columbia': (34.00, -81.03),
        'Columbus OH': (39.96, -82.99),
        'Concord': (37.98, -122.03),
        'Coral Springs': (26.27, -80.27),
        'Corona': (33.88, -117.57),
        'Corpus Christi': (27.80, -97.40),
        'Dallas': (32.78, -96.80),
        'Dayton': (39.76, -84.19),
        'Denton': (33.21, -97.13),
        'Denver': (39.74, -104.99),
        'Des Moines': (41.59, -93.62),
        'Detroit': (42.33, -83.05),
        'Durham': (35.99, -78.90),
        'El Paso': (31.76, -106.49),
        'Elk Grove': (38.41, -121.38),
        'Eugene': (44.05, -123.09),
        'Evansville': (37.97, -87.56),
        'Everett': (47.98, -122.20),
        'Fairfax': (38.85, -77.30),
        'Fargo': (46.88, -96.79),
        'Fayetteville': (35.05, -78.88),
        'Fort Collins': (40.59, -105.08),
        'Fort Lauderdale': (26.12, -80.14),
        'Fort Wayne': (41.08, -85.14),
        'Fort Worth': (32.75, -97.33),
        'Fremont': (37.55, -121.99),
        'Fresno': (36.74, -119.77),
        'Frisco': (33.15, -96.82),
        'Gainesville': (29.65, -82.32),
        'Garden Grove': (33.77, -117.94),
        'Garland': (32.91, -96.64),
        'Gilbert': (33.35, -111.79),
        'Glendale AZ': (33.54, -112.19),
        'Glendale CA': (34.14, -118.25),
        'Grand Prairie': (32.75, -96.99),
        'Grand Rapids': (42.96, -85.66),
        'Green Bay': (44.52, -88.02),
        'Greensboro': (36.07, -79.79),
        'Gresham': (45.50, -122.43),
        'Hampton': (37.03, -76.35),
        'Hartford': (41.76, -72.67),
        'Henderson': (36.04, -114.98),
        'Hialeah': (25.86, -80.28),
        'Hollywood': (26.01, -80.15),
        'Honolulu': (21.31, -157.86),
        'Houston': (29.76, -95.37),
        'Huntington Beach': (33.66, -118.00),
        'Huntsville': (34.73, -86.59),
        'Independence': (39.09, -94.42),
        'Indianapolis': (39.77, -86.16),
        'Irvine': (33.68, -117.83),
        'Irving': (32.81, -96.95),
        'Jackson': (32.30, -90.18),
        'Jacksonville': (30.33, -81.66),
        'Jersey City': (40.73, -74.07),
        'Joliet': (41.53, -88.08),
        'Kansas City': (39.10, -94.58),
        'Kent': (47.38, -122.23),
        'Killeen': (31.12, -97.73),
        'Knoxville': (35.96, -83.92),
        'Lafayette': (30.22, -92.02),
        'Lakeland': (28.04, -81.95),
        'Lakewood': (39.70, -105.08),
        'Lancaster': (34.70, -118.14),
        'Lansing': (42.73, -84.55),
        'Laredo': (27.51, -99.51),
        'Las Vegas': (36.17, -115.14),
        'Lexington': (38.04, -84.50),
        'Lincoln': (40.81, -96.68),
        'Little Rock': (34.74, -92.33),
        'Long Beach': (33.77, -118.19),
        'Los Angeles': (34.05, -118.24),
        'Louisville': (38.25, -85.76),
        'Lubbock': (33.58, -101.86),
        'Madison': (43.07, -89.40),
        'Manchester': (42.99, -71.46),
        'McAllen': (26.20, -98.23),
        'Memphis': (35.15, -90.05),
        'Mesa': (33.42, -111.83),
        'Miami': (25.77, -80.19),
        'Midland': (31.99, -102.08),
        'Milwaukee': (43.04, -87.91),
        'Minneapolis': (44.98, -93.27),
        'Mobile': (30.69, -88.04),
        'Modesto': (37.64, -121.00),
        'Montgomery': (32.37, -86.30),
        'Moreno Valley': (33.94, -117.23),
        'Murfreesboro': (35.85, -86.39),
        'Naperville': (41.78, -88.15),
        'Nashville': (36.16, -86.78),
        'New Haven': (41.31, -72.92),
        'New Orleans': (29.95, -90.07),
        'New York': (40.71, -74.01),
        'Newark': (40.74, -74.17),
        'Newport News': (37.08, -76.47),
        'Norfolk': (36.85, -76.29),
        'Norman': (35.22, -97.44),
        'North Las Vegas': (36.20, -115.12),
        'Oakland': (37.80, -122.27),
        'Oceanside': (33.20, -117.38),
        'Oklahoma City': (35.47, -97.51),
        'Omaha': (41.26, -95.93),
        'Ontario': (34.06, -117.65),
        'Orange': (33.79, -117.85),
        'Orlando': (28.54, -81.38),
        'Overland Park': (38.98, -94.67),
        'Oxnard': (34.20, -119.21),
        'Palm Bay': (28.03, -80.59),
        'Palmdale': (34.58, -118.10),
        'Pasadena': (29.69, -95.21),
        'Paterson': (40.92, -74.17),
        'Pearland': (29.56, -95.29),
        'Pembroke Pines': (26.01, -80.34),
        'Peoria': (40.69, -89.59),
        'Philadelphia': (39.95, -75.17),
        'Phoenix': (33.45, -112.07),
        'Pittsburgh': (40.44, -80.00),
        'Plano': (33.02, -96.70),
        'Pomona': (34.06, -117.75),
        'Portland': (45.52, -122.68),
        'Port St. Lucie': (27.27, -80.35),
        'Providence': (41.82, -71.42),
        'Provo': (40.23, -111.66),
        'Pueblo': (38.25, -104.61),
        'Raleigh': (35.78, -78.64),
        'Rancho Cucamonga': (34.11, -117.59),
        'Reno': (39.53, -119.81),
        'Richmond': (37.54, -77.44),
        'Riverside': (33.95, -117.40),
        'Rochester': (43.16, -77.61),
        'Rockford': (42.27, -89.09),
        'Sacramento': (38.58, -121.49),
        'Salem': (44.94, -123.03),
        'Salinas': (36.68, -121.66),
        'Salt Lake City': (40.76, -111.89),
        'San Antonio': (29.42, -98.49),
        'San Bernardino': (34.11, -117.29),
        'San Diego': (32.72, -117.16),
        'San Francisco': (37.77, -122.42),
        'San Jose': (37.34, -121.89),
        'Santa Ana': (33.75, -117.87),
        'Santa Clara': (37.35, -121.95),
        'Santa Clarita': (34.39, -118.54),
        'Santa Rosa': (38.44, -122.71),
        'Savannah': (32.08, -81.09),
        'Scottsdale': (33.49, -111.93),
        'Seattle': (47.61, -122.33),
        'Shreveport': (32.52, -93.75),
        'Sioux Falls': (43.54, -96.73),
        'South Bend': (41.68, -86.25),
        'Spokane': (47.66, -117.43),
        'Springfield MO': (37.21, -93.29),
        'St. Louis': (38.63, -90.20),
        'St. Paul': (44.95, -93.09),
        'St. Petersburg': (27.77, -82.64),
        'Stamford': (41.05, -73.54),
        'Sterling Heights': (42.58, -83.03),
        'Stockton': (37.96, -121.29),
        'Sunnyvale': (37.37, -122.04),
        'Syracuse': (43.05, -76.15),
        'Tacoma': (47.25, -122.44),
        'Tallahassee': (30.44, -84.28),
        'Tampa': (27.95, -82.46),
        'Tempe': (33.42, -111.94),
        'Thornton': (39.87, -104.97),
        'Toledo': (41.66, -83.58),
        'Topeka': (39.05, -95.68),
        'Torrance': (33.84, -118.34),
        'Tucson': (32.22, -110.93),
        'Tulsa': (36.15, -95.99),
        'Tyler': (32.35, -95.30),
        'Vallejo': (38.10, -122.26),
        'Vancouver': (45.63, -122.67),
        'Ventura': (34.27, -119.23),
        'Virginia Beach': (36.85, -75.98),
        'Visalia': (36.33, -119.29),
        'Waco': (31.55, -97.15),
        'Warren': (42.49, -83.03),
        'Washington DC': (38.91, -77.04),
        'Waterbury': (41.56, -73.05),
        'West Valley City': (40.69, -112.00),
        'Westminster': (39.84, -105.04),
        'Wichita': (37.69, -97.34),
        'Wilmington': (34.23, -77.94),
        'Winston-Salem': (36.10, -80.24),
        'Worcester': (42.26, -71.80),
        'Yonkers': (40.93, -73.90)
    },
    'China': {
        'Beijing': (39.90, 116.41),
        'Changsha': (28.20, 112.97),
        'Chengdu': (30.57, 104.07),
        'Chongqing': (29.56, 106.55),
        'Dalian': (38.91, 121.60),
        'Dongguan': (23.05, 113.74),
        'Foshan': (23.02, 113.12),
        'Guangzhou': (23.13, 113.26),
        'Hangzhou': (30.25, 120.17),
        'Harbin': (45.75, 126.65),
        'Jinan': (36.67, 117.00),
        'Nanjing': (32.06, 118.78),
        'Qingdao': (36.07, 120.38),
        'Shanghai': (31.23, 121.47),
        'Shenzhen': (22.54, 114.06),
        'Tianjin': (39.13, 117.20),
        'Wuhan': (30.59, 114.31),
        'Xi\'an': (34.34, 108.94),
        'Zhengzhou': (34.75, 113.63)
    },
    'Japan': {
        'Fukuoka': (33.59, 130.40),
        'Nagoya': (35.18, 136.91),
        'Osaka': (34.69, 135.50),
        'Tokyo': (35.68, 139.77)
    },
    'India': {
        'Ahmedabad': (23.03, 72.58),
        'Bangalore': (12.97, 77.59),
        'Chennai': (13.08, 80.27),
        'Delhi': (28.61, 77.21),
        'Hyderabad': (17.38, 78.47),
        'Kolkata': (22.57, 88.36),
        'Mumbai': (19.08, 72.88),
        'Pune': (18.52, 73.86),
        'Surat': (21.20, 72.84)
    },
    'United Kingdom': {
        'London': (51.51, -0.13)
    },
    'France': {
        'Paris': (48.85, 2.35)
    },
    'Russia': {
        'Moscow': (55.75, 37.62),
        'Saint Petersburg': (59.93, 30.34)
    },
    'Brazil': {
        'Belo Horizonte': (-19.92, -43.94),
        'Rio de Janeiro': (-22.91, -43.17),
        'Sao Paulo': (-23.55, -46.63)
    },
    'Canada': {
        'Montreal': (45.50, -73.57),
        'Toronto': (43.65, -79.38),
        'Vancouver': (49.28, -123.12)
    },
    'Other Asia': {
        'Bangkok': (13.75, 100.50),
        'Dhaka': (23.81, 90.41),
        'Hanoi': (21.03, 105.85),
        'Ho Chi Minh City': (10.82, 106.63),
        'Hong Kong': (22.32, 114.17),
        'Jakarta': (-6.21, 106.85),
        'Karachi': (24.86, 67.01),
        'Kuala Lumpur': (3.14, 101.69),
        'Lahore': (31.55, 74.34),
        'Manila': (14.60, 120.98),
        'Singapore': (1.35, 103.82),
        'Taipei': (25.03, 121.57),
        'Tehran': (35.69, 51.39),
        'Yangon': (16.87, 96.20)
    },
    'Middle East': {
        'Baghdad': (33.34, 44.40),
        'Dubai': (25.20, 55.27),
        'Istanbul': (41.01, 28.95),
        'Riyadh': (24.63, 46.72)
    },
    'Europe': {
        'Ankara': (39.93, 32.85),
        'Barcelona': (41.39, 2.17),
        'Kiev': (50.45, 30.52),
        'Madrid': (40.42, -3.70),
        'Milan': (45.46, 9.19),
        'Rome': (41.90, 12.50)
    },
    'Africa': {
        'Alexandria': (31.20, 29.92),
        'Cairo': (30.04, 31.24),
        'Khartoum': (15.50, 32.56),
        'Kinshasa': (-4.32, 15.32),
        'Lagos': (6.52, 3.37),
        'Luanda': (-8.84, 13.23)
    },
    'Latin America': {
        'Bogota': (4.71, -74.07),
        'Buenos Aires': (-34.60, -58.38),
        'Guadalajara': (20.67, -103.35),
        'Lima': (-12.04, -77.03),
        'Mexico City': (19.43, -99.13),
        'Santiago': (-33.45, -70.67)
    },
    'Oceania': {
        'Melbourne': (-37.81, 144.96),
        'Sydney': (-33.87, 151.21)
    }
}

# Flatten cities dictionary for easy lookup while keeping the structure for the dropdown
cities = {}
for country, country_cities in cities_by_country.items():
    cities.update(country_cities)

# Create the app layout with Bootstrap components
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Weather Dashboard', className='text-primary text-center mb-4 mt-4'),
            html.Hr()
        ])
    ]),
    
    dbc.Row([
        # Location Dropdown (70% width)
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Select Location', className='card-title'),
                    dcc.Dropdown(
                        id='city-dropdown',
                        options=[
                            {'label': f"{city} ({country})", 'value': city}
                            for country in cities_by_country
                            for city in cities_by_country[country]
                        ],
                        value='New York',
                        className='mb-3'
                    )
                ])
            ], className='mb-4')
        ], width=8),  # 8/12 = ~70%
        
        # Temperature Toggle (30% width)
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Unit', className='card-title'),
                    html.Div([
                        html.Div([
                            # Temperature options with labels
                            html.Div([
                                html.Span("°C", className='unit-label')
                            ], className='temp-option'),
                            html.Div([
                                html.Span("°F", className='unit-label')
                            ], className='temp-option')
                        ], className='temp-toggle-options'),
                        # Single radio button group below
                        dcc.RadioItems(
                            id='temp-unit-toggle',
                            options=[
                                {'label': '', 'value': 'C'},
                                {'label': '', 'value': 'F'}
                            ],
                            value='C',
                            className='radio-group',
                            style={'display': 'flex', 'gap': '60px', 'margin-top': '8px'}
                        )
                    ], className='temp-toggle-container')
                ])
            ], className='mb-4')
        ], width=4)  # 4/12 = ~30%
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='weather-display')
        ])
    ])
], fluid=True)

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

@callback(
    Output('weather-display', 'children'),
    [Input('city-dropdown', 'value'),
     Input('temp-unit-toggle', 'value')]
)
def update_weather(selected_city, temp_unit):
    if selected_city is None:
        return html.P('Please select a city')
    
    # Get coordinates for selected city
    lat, lon = cities[selected_city]
    
    # Fetch weather data
    df, daily_df = fetch_weather_data(lat, lon)
    
    if df is not None and daily_df is not None:
        # Get timezone for the selected city
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        city_tz = ZoneInfo(timezone_str)
        
        # Get current time in city's timezone
        now = datetime.now(city_tz)
        today = now.date()
        
        # Debug logging for sunrise/sunset times
        print("\n=== App Timezone Conversion Debug ===")
        print(f"Selected city: {selected_city}")
        print(f"Coordinates: {lat}, {lon}")
        print(f"Detected timezone: {timezone_str}")
        print(f"Current time in city: {now}")
        print(f"Today's date: {today}")
        
        # Find today's data in the daily DataFrame
        today_data = daily_df[daily_df['date'].dt.date == today]
        if today_data.empty:
            print("WARNING: No data found for today, using first available day")
            today_data = daily_df.iloc[0:1]
        
        today_sun = today_data.iloc[0]
        
        print("\nBefore conversion:")
        print(f"Raw sunrise: {today_sun['sunrise']} ({today_sun['sunrise'].tzinfo})")
        print(f"Raw sunset: {today_sun['sunset']} ({today_sun['sunset'].tzinfo})")
        
        # Format times
        sunrise_str = today_sun['sunrise'].strftime('%I:%M %p').lstrip('0')
        sunset_str = today_sun['sunset'].strftime('%I:%M %p').lstrip('0')
        
        print("\nFormatted times:")
        print(f"Sunrise string: {sunrise_str}")
        print(f"Sunset string: {sunset_str}")
        print("=================================\n")

        # Create sunrise/sunset component
        sun_times = html.Div([
            # Sunrise section
            html.Div([
                html.Img(src=f'/assets/sunrise.png?v={current_timestamp}', className='sun-icon'),
                html.Div("SUNRISE", className='sun-label'),
                html.Div(sunrise_str, className='sun-time')
            ], className='sun-section'),
            
            # Divider
            html.Div(className='sun-divider'),
            
            # Sunset section
            html.Div([
                html.Img(src=f'/assets/sunset.png?v={current_timestamp}', className='sun-icon'),
                html.Div("SUNSET", className='sun-label'),
                html.Div(sunset_str, className='sun-time')
            ], className='sun-section')
        ], className='current-weather-card sunrise-sunset-card')

        # Convert the DataFrame dates to city timezone and find current data
        df['local_time'] = df['time'].dt.tz_convert(city_tz)
        now = datetime.now(city_tz)
        
        # Find the closest forecast hour
        time_diffs = abs(df['local_time'] - now)
        closest_idx = time_diffs.idxmin()
        
        # Get 12 hours of data starting from the closest hour
        today_data = df.iloc[closest_idx:closest_idx + 12]
        
        # Get weather description and icon name for current conditions
        current_weather_code = df['weather_code'].iloc[0]
        weather_desc, icon_name = get_weather_info(current_weather_code)

        # Convert temperatures if needed
        current_temp = df['dew_point_2m'].iloc[0]
        if temp_unit == 'F':
            current_temp = celsius_to_fahrenheit(current_temp)

        # Create current weather component
        current_weather = html.Div([
            # Current Weather Card
            html.Div([
                # Title
                html.Div("CURRENT WEATHER", className="current-weather-title"),
                
                # Location
                html.Div(selected_city, className="current-weather-location"),
                
                # Temperature and Icon
                html.Div([
                    html.Div(f"{int(current_temp)}°{temp_unit}", className="current-weather-temp"),
                    html.Img(src=f'/assets/{icon_name}.png?v={current_timestamp}', className="current-weather-icon")
                ], className="current-weather-main"),
                
                # Details Row
                html.Div([
                    # Wind Speed
                    html.Div([
                        html.Div("WIND", className="detail-label"),
                        html.Div(f"{df['wind_speed_180m'].iloc[0]:.1f} mph", className="detail-value")
                    ], className="current-weather-detail-item"),
                    
                    # Humidity
                    html.Div([
                        html.Div("HUMIDITY", className="detail-label"),
                        html.Div(f"{df['relative_humidity_2m'].iloc[0]:.0f}%", className="detail-value")
                    ], className="current-weather-detail-item")
                ], className="current-weather-details")
            ], className="current-weather-card")
        ])

        # Update forecast cards with correct temperature unit
        forecast_cards = []
        current_date = datetime.now()
        for i in range(0, 7):
            day_data = df.iloc[i * 24]
            weather_code = day_data['weather_code']
            _, icon_name = get_weather_info(weather_code)
            
            temp = day_data['dew_point_2m']
            temp_low = temp - 5  # Simulated low temp
            
            if temp_unit == 'F':
                temp = celsius_to_fahrenheit(temp)
                temp_low = celsius_to_fahrenheit(temp_low)
            
            display_date = current_date.strftime('%a')
            if i == 0:
                display_date = 'Today'
            
            day_card = dbc.Col([
                html.Div([
                    html.Div(
                        display_date,
                        className='day-name'
                    ),
                    html.Img(
                        src=f'/assets/{icon_name}.png?v={current_timestamp}',
                        className='weather-icon'
                    ),
                    html.Div(
                        f"{int(temp)}°{temp_unit}",
                        className='high-temp'
                    ),
                    html.Div(
                        f"{int(temp_low)}°{temp_unit}",
                        className='low-temp'
                    )
                ], className='day-card')
            ], className='day-col', width=True)
            
            forecast_cards.append(day_card)
            current_date = current_date.replace(day=current_date.day + 1)

        # Create precipitation probability graph with local time
        hours = [d.strftime('%I %p').lstrip('0') for d in today_data['local_time']]
        probabilities = today_data['precipitation_probability']
        
        # Calculate y-axis range
        y_max = max(max(probabilities), 10)  # At least 10%

        # Define color bins
        def get_marker_color(prob):
            if prob < 20:
                return '#4575b4'  # Light blue
            elif prob < 40:
                return '#74add1'  # Medium blue
            elif prob < 60:
                return '#abd9e9'  # Dark blue
            elif prob < 80:
                return '#fdae61'  # Orange
            else:
                return '#d73027'  # Red

        # Update title to reflect time range
        start_time = now.strftime('%I %p').lstrip('0')
        end_time = (now + timedelta(hours=12)).strftime('%I %p').lstrip('0')
        
        fig = go.Figure()
        
        # Add the line with data labels
        fig.add_trace(go.Scatter(
            x=hours,
            y=probabilities,
            mode='lines+markers+text',
            name='Precipitation Probability',
            line=dict(
                color='#000080',
                width=2
            ),
            marker=dict(
                size=10,
                color=[get_marker_color(p) for p in probabilities],
                line=dict(
                    color='#000080',
                    width=1
                )
            ),
            text=[f'{int(p)}%' for p in probabilities],
            textposition='top center',
            textfont=dict(
                family='Courier Prime, monospace',
                size=16,
                color='#000080'
            )
        ))
        
        # Update layout for retro style
        fig.update_layout(
            plot_bgcolor='#f5f5dc',
            paper_bgcolor='#f5f5dc',
            font=dict(
                family='Courier Prime, monospace',
                size=12,
                color='#000080'
            ),
            title=dict(
                text='<span style="letter-spacing: 0.2em">PRECIPITATION PROBABILITY</span>',
                font=dict(
                    family='DM Serif Display, serif',
                    size=24,
                    color='#000080'
                ),
                x=0,
                xanchor='left',
                y=0.95
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,128,0.1)',
                tickangle=45,
                tickfont=dict(size=10),
                nticks=13  # One tick per hour
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,128,0.1)',
                ticksuffix='%',
                range=[0, y_max * 1.1],
                dtick=5
            ),
            margin=dict(t=40, r=20, b=40, l=40),
            height=300,
            width=None,
            autosize=True
        )

        precipitation_graph = html.Div([
            dcc.Graph(
                figure=fig,
                config={'displayModeBar': False},
                style={'width': '100%', 'height': '100%'}  # Ensure graph fills container
            )
        ], className='current-weather-card precipitation-card')

        # Create temperature trend chart
        temp_data = today_data.iloc[::2]  # Take every 2nd hour for 2-hour increments
        hours_temp = [d.strftime('%I %p').lstrip('0') for d in temp_data['local_time']]
        temperatures = temp_data['dew_point_2m']
        
        if temp_unit == 'F':
            temperatures = [celsius_to_fahrenheit(t) for t in temperatures]

        # Create color scale based on temperature
        min_temp = min(temperatures)
        max_temp = max(temperatures)
        
        # Generate colors based on temperature values
        colors = []
        for temp in temperatures:
            # Calculate position in the temperature range (0 to 1)
            position = (temp - min_temp) / (max_temp - min_temp) if max_temp != min_temp else 0.5
            
            if position < 0.2:
                color = '#4575b4'  # Cool blue
            elif position < 0.4:
                color = '#74add1'  # Light blue
            elif position < 0.6:
                color = '#abd9e9'  # Very light blue
            elif position < 0.8:
                color = '#fdae61'  # Light orange
            else:
                color = '#f46d43'  # Orange
                
            colors.append(color)

        temp_fig = go.Figure()
        
        # Add the temperature bars with data labels
        temp_fig.add_trace(go.Bar(
            x=hours_temp,
            y=temperatures,
            text=[f'{int(t)}°{temp_unit}' for t in temperatures],
            textposition='outside',
            marker_color=colors,  # Use our temperature-based colors
            marker_line_color='#000080',
            marker_line_width=1,
            textfont=dict(
                family='Courier Prime, monospace',
                size=16,
                color='#000080'
            ),
            hoverinfo='none'
        ))
        
        # Update layout for retro style matching the precipitation chart
        temp_fig.update_layout(
            plot_bgcolor='#f5f5dc',
            paper_bgcolor='#f5f5dc',
            font=dict(
                family='Courier Prime, monospace',
                size=12,
                color='#000080'
            ),
            title=dict(
                text='<span style="letter-spacing: 0.2em">TEMPERATURE TREND</span>',
                font=dict(
                    family='DM Serif Display, serif',
                    size=24,
                    color='#000080'
                ),
                x=0,
                xanchor='left',
                y=0.95
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,128,0.1)',
                tickangle=45,
                tickfont=dict(
                    size=14,  # Increased time label size
                    family='Courier Prime, monospace'
                )
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,128,0.1)',
                ticksuffix=f'°{temp_unit}',
                dtick=5,
                range=[min(temperatures) - 5, max(temperatures) + 10],  # Add padding for labels
                tickfont=dict(size=12)
            ),
            margin=dict(t=40, r=20, b=50, l=40),  # Increased bottom margin for larger labels
            height=300,
            width=None,
            autosize=True,
            showlegend=False,
            bargap=0.2
        )

        temperature_graph = html.Div([
            dcc.Graph(
                figure=temp_fig,
                config={'displayModeBar': False},
                style={'width': '100%', 'height': '100%'}
            )
        ], className='current-weather-card precipitation-card')

        return [
            dbc.Row([
                # Current Weather Section
                dbc.Col([
                    current_weather,
                    sun_times
                ], width=4),
                
                # 7-Day Forecast Section
                dbc.Col([
                    html.Div([
                        html.Div("WEEK FORECAST", className="current-weather-title"),
                        dbc.Row(
                            forecast_cards,
                            className='forecast-row'
                        )
                    ], className='current-weather-card forecast')
                ], width=6)
            ]),
            # Precipitation Graph Row
            dbc.Row([
                dbc.Col([precipitation_graph], width=12)
            ]),
            # Temperature Trend Graph Row
            dbc.Row([
                dbc.Col([temperature_graph], width=12)
            ])
        ]
    else:
        return dbc.Alert('Error fetching weather data', color='danger')

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 