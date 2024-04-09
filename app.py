from flask import Flask, render_template, jsonify
from datetime import datetime
import numpy as np
import pymysql
import datetime

app = Flask(__name__)

# Define database connection parameters
DB_HOST = "127.0.0.1"  # Replace with your host
DB_USER = "root"  # Replace with your database username
DB_PASSWORD = "root"  # Replace with your database password
DB_NAME = "weather"  # Replace with your database name


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


# Function to fetch weather data
def fetch_weather_data(city, connection):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {city}_weather WHERE HOUR(time) = 9")
        return cursor.fetchall()


# Function to fetch apparent temperature data
def fetch_apparent_temp_data(city, connection):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT time, apparent_temperature FROM {city}_weather WHERE HOUR(time) = 9"
        )
        return cursor.fetchall()


# Function to fetch meteorological factors data
def fetch_meteorological_factors_data(city, connection):
    with connection.cursor() as cursor:
        if city.lower() not in ["chennai", "madurai"]:
            raise ValueError(f"Invalid city: {city}")

        cursor.execute(
            f"SELECT time, surface_pressure, relative_humidity_2m as relative_humidity, wind_speed_10m as wind_speed FROM {city.lower()}_weather WHERE HOUR(time) = 9"
        )
        return cursor.fetchall()


@app.route("/api/weather-data/<city>")
def weather_data(city):
    connection = get_connection()
    city_data = fetch_weather_data(city, connection)
    connection.close()

    # Extract labels and temperatures from city_data
    labels = [data["time"].strftime("%Y-%m-%d %H:%M:%S") for data in city_data]
    temperatures = [data["temperature_2m"] for data in city_data]

    chart_data = {
        "labels": labels,
        "temperatures": temperatures,
    }

    return jsonify(chart_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/temperature")
def weather_chart():
    return render_template("temperature.html")


@app.route("/api/apparent-weather-data/<city>")
def apparent_weather_data(city):
    connection = get_connection()
    city_data = fetch_apparent_temp_data(city, connection)
    connection.close()

    # Extract labels and apparent temperatures from city_data
    labels = [data["time"].strftime("%Y-%m-%d %H:%M:%S") for data in city_data]
    apparent_temperatures = [data["apparent_temperature"] for data in city_data]

    chart_data = {
        "labels": labels,
        "apparentTemperatures": apparent_temperatures,
    }

    return jsonify(chart_data)


@app.route("/api/meteorological-factors-data/<city>")
def meteorological_factors_data(city):
    connection = get_connection()
    city_data = fetch_meteorological_factors_data(city, connection)
    connection.close()

    # Extract labels and meteorological factors from city_data
    labels = [data["time"].strftime("%Y-%m-%d %H:%M:%S") for data in city_data]
    surface_pressures = [data["surface_pressure"] for data in city_data]
    relative_humidities = [data["relative_humidity"] for data in city_data]
    wind_speeds = [data["wind_speed"] for data in city_data]

    chart_data = {
        "labels": labels,
        "surfacePressures": surface_pressures,
        "relativeHumidities": relative_humidities,
        "windSpeeds": wind_speeds,
    }

    return jsonify(chart_data)


@app.route("/meteorological-factors")
def meteorological_factors_chart():
    return render_template("meteorological-factors.html")


# Function to fetch temperature data for analysis
def fetch_temperature_data(city, connection):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT temperature_2m FROM {city}_weather WHERE HOUR(time) = 9"
        )
        return [row["temperature_2m"] for row in cursor.fetchall()]


@app.route("/api/analysis-data/<city>")
def analysis_data(city):
    connection = get_connection()
    temperatures = fetch_temperature_data(city, connection)
    connection.close()

    # Calculate mean, median, and standard deviation
    mean_temp = round(np.mean(temperatures), 2)
    median_temp = round(np.median(temperatures), 2)
    std_dev = round(np.std(temperatures), 2)

    return jsonify(
        {
            "meanTemp": mean_temp,
            "medianTemp": median_temp,
            "stdDev": std_dev,
        }
    )


# Function to fetch apparent temperature data for analysis
def fetch_apparent_temp_data_for_analysis(city, connection):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT apparent_temperature FROM {city}_weather WHERE HOUR(time) = 9"
        )
        return [row["apparent_temperature"] for row in cursor.fetchall()]


@app.route("/api/apparent-analysis-data/<city>")
def apparent_analysis_data(city):
    connection = get_connection()
    apparent_temperatures = fetch_apparent_temp_data_for_analysis(city, connection)
    connection.close()

    # Calculate mean, median, and standard deviation
    mean_app_temp = round(np.mean(apparent_temperatures), 2)
    median_app_temp = round(np.median(apparent_temperatures), 2)
    std_dev_app = round(np.std(apparent_temperatures), 2)

    return jsonify(
        {
            "meanAppTemp": mean_app_temp,
            "medianAppTemp": median_app_temp,
            "stdDevApp": std_dev_app,
        }
    )




@app.route("/table")
def table():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM chennai_weather WHERE HOUR(time) = 9")
        chennai_data = cursor.fetchall()
        for row in chennai_data:
            row['time'] = row['time'].strftime('%Y-%m-%d')

        cursor.execute("SELECT * FROM madurai_weather WHERE HOUR(time) = 9")
        madurai_data = cursor.fetchall()
        for row in madurai_data:
            row['time'] = row['time'].strftime('%Y-%m-%d')
    connection.close()
    return render_template("Table.html", chennai_data=chennai_data, madurai_data=madurai_data)


if __name__ == "__main__":
    app.run(debug=True)
