from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_daq as daq
from weather_fetcher import fetch_weather_data

# Initialize the Dash app with a modern theme and Font Awesome
app = Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        'https://use.fontawesome.com/releases/v5.15.4/css/all.css'
    ]
)

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
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='weather-display')
        ])
    ])
], fluid=True)

@callback(
    Output('weather-display', 'children'),
    Input('city-dropdown', 'value')
)
def update_weather(selected_city):
    if selected_city is None:
        return html.P('Please select a city')
    
    # Get coordinates for selected city
    lat, lon = cities[selected_city]
    
    # Fetch weather data
    df = fetch_weather_data(lat, lon)
    
    if df is not None:
        # Create temperature trend graph
        fig = px.line(
            df.head(24),  # First 24 hours
            x='date',
            y='dew_point_2m',
            title='24-Hour Temperature Trend',
            labels={'date': 'Time', 'dew_point_2m': 'Temperature (°C)'}
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=30, b=30, l=30, r=30)
        )

        return [
            dbc.Card([
                dbc.CardHeader(
                    dbc.Row([
                        dbc.Col(html.H3(f'Weather in {selected_city}', className='text-primary mb-0'), width=8),
                        dbc.Col(
                            html.Div([
                                html.I(className="fas fa-map-marker-alt me-2"),
                                f"{lat}°N, {lon}°E"
                            ], className='text-muted text-end'),
                            width=4
                        )
                    ])
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(figure=fig, config={'displayModeBar': False})
                        ], width=12, className='mb-4'),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Table([
                                html.Thead(html.Tr([
                                    html.Th('Time'),
                                    html.Th('Cloud Cover'),
                                    html.Th('Temperature'),
                                    html.Th('Precipitation')
                                ], className='table-primary')),
                                html.Tbody([
                                    html.Tr([
                                        html.Td(df['date'].iloc[i].strftime('%H:%M')),
                                        html.Td([
                                            html.I(className="fas fa-cloud me-2"),
                                            f"{df['cloud_cover'].iloc[i]}%"
                                        ]),
                                        html.Td([
                                            html.I(className="fas fa-thermometer-half me-2"),
                                            f"{df['dew_point_2m'].iloc[i]}°C"
                                        ]),
                                        html.Td([
                                            html.I(className="fas fa-tint me-2"),
                                            f"{df['precipitation_probability'].iloc[i]}%"
                                        ])
                                    ]) for i in range(5)
                                ])
                            ], bordered=True, hover=True, responsive=True, striped=True)
                        ])
                    ])
                ])
            ], className='mb-4 shadow')
        ]
    else:
        return dbc.Alert('Error fetching weather data', color='danger')

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 