import requests
from datetime import datetime
import os
import json
def extract():
    def fetch_weather(location):
        WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
        API_KEY = 'yourkey'

        params = {'q':location, 'appid':API_KEY, 'units':'metric'}
        response = requests.get(WEATHER_URL, params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to get weather data: status code{response.status_code}')

    def fetch_aq(lat, lon):
        AQ_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
        API_KEY = 'yourkey'

        params = {'lat':lat, 'lon':lon, 'appid':API_KEY}
        response = requests.get(AQ_URL, params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to get air quality data: status code{response.status_code}')

    extracted_data = []
    #LOCATIONS = ['Toronto,CA', 'New York,US', 'London,GB', 'Tokyo,JP']
    LOCATIONS = ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"]
    for loc in LOCATIONS:
        weather_data = fetch_weather(location=loc)   # get weather data
        
        if 'coord' in weather_data:
            lat, lon = weather_data['coord']['lat'], weather_data['coord']['lon']
            aq_data = fetch_aq(lat, lon)    # Get air quality data
        else:
            aq_data = None
        
        combined = {
            'city': loc,
            'datetime': datetime.now().isoformat(),
            'weather': weather_data,
            'air_quality': aq_data
        }
        extracted_data.append(combined)

    os.makedirs('/opt/airflow/data', exist_ok=True) # path in the airflow container
    with open('/opt/airflow/data/raw_weather.json', 'w') as f:
        json.dump(extracted_data, f)
    
    # for test on local machine
    #with open('/Users/Zjxi/Desktop/elt/extracted_data.json', 'w') as f:
    #    json.dump(extracted_data, f, indent=4)
    

if __name__ == '__main__':
    extract()
    
