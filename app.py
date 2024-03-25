from flask import Flask, render_template, jsonify
from sql_connect import get_connection, fetch_weather_data
import pymysql
import json
import datetime

app = Flask(__name__)

# Define database connection parameters
DB_HOST = "127.0.0.1"  # Replace with your database host
DB_USER = "root"  # Replace with your database username
DB_PASSWORD = "root"  # Replace with your database password
DB_NAME = "weather_db"  # Replace with your database name


# Function to establish database connection
def get_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection


@app.route("/weather_chart")
def weather_chart():
    connection = get_connection()
    city_data = fetch_weather_data("chennai", connection)
    connection.close()

    # Extract labels and temperatures from city_data
    labels = [
        data["time"].strftime("%%Y-%m-%d %H:%M:%S") for data in city_data
    ]
    temperatures = [data["temperature_2m"] for data in city_data]

    chart_data = {
        "labels": labels,
        "temperatures": temperatures,
    }

    chart_data_json = json.dumps(chart_data)

    return render_template("chennai_weather_chart.html", chart_data_json=chart_data_json)


if __name__ == "__main__":
    app.run(debug=True)
