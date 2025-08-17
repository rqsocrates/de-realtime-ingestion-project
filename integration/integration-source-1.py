import requests
import json
from minio import Minio
from io import BytesIO

client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Configuration
API_KEY = "ec550498bf4399da18bc6cae4765dafe"
CITY = "Manila"



# Function to fetch weather data
def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}, {response.text}")
        return None


data_api = fetch_weather_data(CITY)
json_data = json.dumps(data_api)
api_data = json_data.encode("utf-8")
format_data = BytesIO(api_data)

print(f"Weather data for {CITY}:\n{format_data}")


bucket_name = "dl-source-data"
data_json = 'raw.json'


found = client.bucket_exists(bucket_name)

if not found:
    client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' created.")
else:
    print(f"Bucket '{bucket_name}' already exists.")


client.put_object(
    bucket_name,
    data_json,
    format_data,
    len(api_data)
)