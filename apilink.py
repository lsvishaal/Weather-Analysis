import requests
import json
import sqlconnect as mq

# Function to fetch data from API and insert into SQL table
def fetch_and_insert_data(url, city):
    # Fetch data from the API
    response = requests.get(url)

    # Parse JSON response
    data = response.json()

    # Extract hourly data
    hourly_data = data.get('hourly', [])

    # Extract relevant information from hourly data
    records = []
    for entry in hourly_data:
        temperature = entry.get('temperature_2m')
        apparent_temperature = entry.get('apparent_temperature')
        surface_pressure = entry.get('surface_pressure')
        humidity = entry.get('relative_humidity_2m')
        windspeed = entry.get('wind_speed_10m')
        precipitation = entry.get('precipitation')
        day = entry.get('is_day')
        records.append((temperature, apparent_temperature, surface_pressure, humidity, windspeed, precipitation, day))

    # Batch insertion into SQL table
    batch_size = 100  # Adjust batch size as needed
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        insert_batch(batch, city)

# Function to insert a batch of records into SQL table
def insert_batch(batch, city):
    # Construct the SQL query for batch insertion
    query = f"INSERT INTO {city}_weather (temperature, apparent_temperature, surface_pressure, humidity, windspeed, precipitation, day) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    # Execute the batch insertion query
    mq.mycursor.executemany(query, batch)
    mq.mydb.commit()

# Define the URLs for Chennai and Madurai
chennai_url = "https://archive-api.open-meteo.com/v1/archive?latitude=13.0878&longitude=80.2785&start_date=2023-12-01&end_date=2024-03-24&hourly=temperature_2m,rain&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_hours&timezone=auto"
madurai_url = "https://archive-api.open-meteo.com/v1/archive?latitude=9.919&longitude=78.1195&start_date=2023-12-01&end_date=2024-03-24&hourly=temperature_2m,rain&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_hours&timezone=auto"

# Fetch and insert data for Chennai
fetch_and_insert_data(chennai_url, "chennai")

# Fetch and insert data for Madurai
fetch_and_insert_data(madurai_url, "madurai")
