import csv
import mysql.connector

# Open the CSV file
with open(
    "C:\\Users\\Atomic_Sneaks\\Downloads\\open-meteo-9.95N78.11E139m.csv",
    newline="",
    encoding="utf-8",
) as csvfile:
    reader = csv.reader(csvfile)  # Assuming comma-separated data
    lines = list(reader)

# Extract column headers and replace degree symbol with suitable representation
headers = [header.strip().replace("°C", "_Celsius") for header in lines[0]]

# Prepare the SQL query template
sql_template = "INSERT INTO madurai_weather ({})\nVALUES\n".format(", ".join(headers))

# Process each line and format it in SQL INSERT INTO statement format
sql_values = []
for line in lines[1:]:
    formatted_values = "('{}')".format("', '".join([value.strip() for value in line]))
    sql_values.append(formatted_values)

# Combine SQL template and values
sql_query = sql_template + ",\n".join(sql_values) + ";"

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="127.0.0.1", user="root", password="root", database="weather_db"
)
cursor = conn.cursor()

# Execute the SQL query to create the table if it doesn't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS madurai_weather (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    time DATETIME,
                    temperature_2m FLOAT,
                    apparent_temperature FLOAT,
                    surface_pressure FLOAT,
                    relative_humidity_2m FLOAT,
                    wind_speed_10m FLOAT,
                    precipitation FLOAT,
                    is_day BOOLEAN
                );"""
)

# Execute the SQL query to insert data
cursor.execute(sql_query)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into madurai_weather table in weather_db database.")
