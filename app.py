from flask import Flask, render_template, jsonify
import pymysql
import datetime

app = Flask(__name__)

# Define database connection parameters
DB_HOST = "127.0.0.1"  # Replace with your host
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


if __name__ == "__main__":
    app.run(debug=True)
