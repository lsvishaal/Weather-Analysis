import csv
import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="weather_db"
)
mycursor = mydb.cursor()

# Path to your CSV file
csv_file_path = r"C:\Users\Atomic_Sneaks\Downloads\open-meteo-13.11N80.25E15m.csv"  # Use raw string literal

# SQL query to insert data into the table
insert_query = "INSERT INTO chennai_weather (_date_, temprature, precipitation) VALUES (%s, %s, %s)"

# Read data from the CSV file and insert into the table
with open(csv_file_path, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')  # Assuming tab-separated values
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        time = row[0]
        temperature = row[1]
        rain = row[2]
        values = (time, temperature, rain)
        mycursor.execute(insert_query, values)

# Commit the changes
mydb.commit()

# Close the cursor and database connection
mycursor.close()
mydb.close()

print("Data inserted successfully!")
