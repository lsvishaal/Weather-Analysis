import csv
import mysql.connector
import pandas as pd
from datetime import datetime

# Define the path to the CSV file
csv_file_path = "C:\\Users\\lsvis\\Downloads\\open-meteo-madurai.csv"

# Establish connection to the MySQL database
conn = mysql.connector.connect(
    host="127.0.0.1", user="root", password="root", database="weather"
)
cursor = conn.cursor()

try:
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        # Extract values from the row
        time_str = row['time']
        temperature_2m = float(row['temperature_2m'])
        relative_humidity_2m = float(row['relative_humidity_2m'])
        apparent_temperature = float(row['apparent_temperature'])
        surface_pressure = float(row['surface_pressure'])
        wind_speed_10m = float(row['wind_speed_10m'])

        # Parse datetime string from CSV (in ISO 8601 format)
        time_dt = datetime.fromisoformat(time_str)

        # Prepare SQL query to insert data into the database for madurai_weather
        sql_query = """
            INSERT INTO madurai_weather (time, temperature_2m, relative_humidity_2m, apparent_temperature, surface_pressure, wind_speed_10m)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Execute the SQL query to insert data into the madurai_weather table
        cursor.execute(sql_query, (time_dt, temperature_2m, relative_humidity_2m, apparent_temperature, surface_pressure, wind_speed_10m))

    # Commit the transaction
    conn.commit()
    print("Data inserted successfully into madurai_weather table in weather database.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
