from flask import Flask, render_template, jsonify
import sqlite3
import statistics
import re

app = Flask(__name__, template_folder="templates")

# SQLite database file path
DB_FILE = 'weather.db'

def get_connection():
    return sqlite3.connect(DB_FILE)

def fetch_data(query):
    try:
        connection = get_connection()  # Assuming get_connection() returns a valid database connection
        cursor = connection.cursor()
        cursor.execute(query)
        data = [float(item[0]) for item in cursor.fetchall()]  # Convert strings to floats
        connection.close()
        return data
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error executing query: {query}")
        print(f"Error details: {str(e)}")
        return None

@app.route("/")
def home():
    return render_template("temperature.html")

@app.route("/api/temperature/<city>")
def fetch_temperature_data(city):
    try:
        query = f"SELECT time, temperature_2m FROM {city.lower()}_weather WHERE strftime('%H', time) = '09'"
        data = fetch_data(query)

        if not data:
            return jsonify({"error": f"No temperature data found for {city}"}), 404

        labels = [row[0] for row in data]
        temperatures = [row[1] for row in data]

        response = {
            "labels": labels,
            "temperatures": temperatures
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/apparent-weather-data/<city>")
def apparent_weather_data(city):
    try:
        # Construct the SQL query to fetch apparent temperature data for the specified city at 9 AM
        query = f"SELECT time, apparent_temperature FROM {city.lower()}_weather WHERE strftime('%H', time) = '09'"
        
        # Fetch data from the database using the defined query
        data = fetch_data(query)

        # Handle case where no data is returned
        if not data:
            return jsonify({"error": f"No apparent temperature data found for {city.capitalize()} at 9 AM"}), 404

        # Prepare the response data in JSON format
        response = {
            "city": city.capitalize(),
            "data": [{"time": row[0], "apparent_temperature": row[1]} for row in data]
        }

        # Return a JSON response with fetched data
        return jsonify(response), 200

    except Exception as e:
        # Handle any unexpected exceptions and return an error response
        return jsonify({"error": str(e)}), 500

    
@app.route("/api/temperature-analysis/<city>")
def temperature_analysis(city):
    try:
        # Fetch temperature analysis data for the specified city
        # Replace this with your actual logic to fetch analysis data from the database
        # Example response:
        analysis_data = {
            "meanTemperature": 28.5,
            "medianTemperature": 29.0,
            "standardDeviation": 2.1
        }
        return jsonify(analysis_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
from flask import jsonify

@app.route("/api/apparent-temperature-analysis/<city>")
def apparent_temperature_analysis(city):
    try:
        # Construct the SQL query to fetch apparent temperature data for the specified city
        query = f"SELECT apparent_temperature FROM {city.lower()}_weather WHERE strftime('%H', time) = '09'"

        # Fetch apparent temperature data from the database using your fetch_data function
        data = fetch_data(query)

        if not data:
            return jsonify({"error": f"No apparent temperature data found for {city.capitalize()} at 9 AM"}), 404

        # Extract apparent temperatures from the fetched data
        apparent_temperatures = [float(row[0]) for row in data]  # Convert to float

        # Calculate mean, median, and standard deviation of apparent temperatures
        mean_apparent_temp = statistics.mean(apparent_temperatures)
        median_apparent_temp = statistics.median(apparent_temperatures)
        std_deviation = statistics.stdev(apparent_temperatures)

        # Prepare the analysis data
        analysis_data = {
            "meanApparentTemperature": mean_apparent_temp,
            "medianApparentTemperature": median_apparent_temp,
            "standardDeviation": std_deviation
        }

        # Return the analysis data as a JSON response
        return jsonify(analysis_data), 200

    except Exception as e:
        # Handle any unexpected exceptions and return an error response
        return jsonify({"error": str(e)}), 500




@app.route("/api/surface-pressure/<city>")
def surface_pressure_data(city):
    try:
        query = f"SELECT time, surface_pressure FROM {city.lower()}_weather WHERE strftime('%H', time) = '09'"
        data = fetch_data(query)

        if not data:
            return jsonify({"error": f"No surface pressure data found for {city.capitalize()} at 9 AM"}), 404

        labels = [entry[0] for entry in data]
        pressures = [entry[1] for entry in data]

        response = {
            "city": city.capitalize(),
            "labels": labels,
            "pressures": pressures
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def sanitize(input_string):
     # Only remove characters that could potentially be harmful in a SQL query
     return re.sub(r'[;\'"--]', '', input_string)

def fetch_surface_pressures(query):
    try:
        connection = get_connection()  # Assuming get_connection() function is implemented
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()

        # Extract surface pressures and convert to float
        surface_pressures = [float(row[0]) for row in data if isinstance(row[0], str) and row[0].replace('.', '', 1).isdigit()]
        return surface_pressures
    except Exception as e:
        print(f"Error fetching surface pressures: {str(e)}")
        return []


@app.route("/api/surface-pressure-analysis/<city>")
def pressure_analysis_data(city):
    try:
        # Ensure the city parameter is safe to use in the SQL query (sanitize if necessary)
        normalized_city = sanitize(city)

        # Construct the SQL query to fetch surface pressure data for the specified city at 9 AM
        query = f"SELECT surface_pressure FROM {normalized_city.lower()}_weather WHERE strftime('%H', time) = '09'"
        app.logger.info(f"Executing query: {query}")  # Log query for debugging

        # Fetch surface pressure data from the database
        surface_pressures = fetch_surface_pressures(query)
        app.logger.info(f"Data fetched: {surface_pressures}")  # Log fetched data for debugging

        # Check if any data was returned
        if not surface_pressures:
            app.logger.error(f"No surface pressure data found for {city.capitalize()}")
            return jsonify({"error": f"No surface pressure data found for {city.capitalize()}"}), 404

        # Calculate mean, median, and standard deviation of surface pressures
        mean_pressure = statistics.mean(surface_pressures)
        median_pressure = statistics.median(surface_pressures)
        std_dev_pressure = statistics.stdev(surface_pressures) if len(surface_pressures) > 1 else 0

        # Round standard deviation to 2 decimal places
        std_dev_pressure = round(std_dev_pressure, 2)

        # Prepare response JSON
        result = {
            "meanPressure": mean_pressure,
            "medianPressure": median_pressure,
            "stdDevPressure": std_dev_pressure
        }

        # Return successful response
        return jsonify(result), 200

    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"Error fetching pressure analysis data for {city}: {str(e)}")
        # Return error response
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/relative-humidity/<city>")
def relative_humidity_data(city):
    try:
        # Construct the SQL query to fetch relative humidity data for the specified city at 9 AM
        query = f"SELECT time, relative_humidity_2m FROM {city.lower()}_weather WHERE strftime('%H', time) = '09'"
        data = fetch_data(query)

        if not data:
            return jsonify({"error": f"No relative humidity data found for {city.capitalize()} at 9 AM"}), 404

        labels = [entry[0] for entry in data]
        humidities = [entry[1] for entry in data]

        response = {
            "city": city.capitalize(),
            "labels": labels,
            "relativeHumidities": humidities
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def sanitize(city):
    return re.sub(r'\W+', '', city)

@app.route("/api/relative-humidity-analysis-data/<city>")
def humidity_analysis_data(city):
    try:
        # Ensure the city parameter is safe to use in the SQL query (sanitize if necessary)
        normalized_city = sanitize(city)

        # Construct the SQL query to fetch relative humidity data for the specified city at 9 AM
        query = f"SELECT relative_humidity_2m FROM {normalized_city.lower()}_weather WHERE strftime('%H', time) = '09'"

        print("Executing SQL query:", query)

        # Fetch relative humidity data from the database
        relative_humidities = fetch_data(query)

        # Check if any data was returned
        if not relative_humidities:
            print(f"No relative humidity data found for {city.capitalize()}")
            return jsonify({"error": f"No relative humidity data found for {city.capitalize()}"}), 404

        # Calculate mean, median, and standard deviation of relative humidities
        mean_humidity = statistics.mean(relative_humidities)
        median_humidity = statistics.median(relative_humidities)
        std_dev_humidity = statistics.stdev(relative_humidities) if len(relative_humidities) > 1 else 0

        # Round standard deviation to 2 decimal places
        std_dev_humidity = round(std_dev_humidity, 2)

        # Prepare response JSON
        result = {
            "meanRelativeHumidity": mean_humidity,
            "medianRelativeHumidity": median_humidity,
            "stdDevRelativeHumidity": std_dev_humidity
        }

        # Return successful response
        return jsonify(result), 200

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error fetching humidity analysis data for {city}: {str(e)}")
        # Return error response
        return jsonify({"error": str(e)}), 500


from flask import jsonify
import statistics

def pressure_analysis_data(city):
    try:
        print(f"Fetching surface pressure analysis data for {city}...")

        # Ensure the city parameter is safe to use in the SQL query (sanitize if necessary)
        normalized_city = sanitize(city)

        # Construct the SQL query to calculate mean surface pressure
        query = f"SELECT surface_pressure FROM {normalized_city}_weather"

        print("Executing SQL query:", query)

        # Fetch surface pressure data from the database
        surface_pressures = fetch_surface_pressures(query)

        # Check if any data was returned
        if not surface_pressures:
            print(f"No surface pressure data found for {city.capitalize()}")
            return jsonify({"error": f"No surface pressure data found for {city.capitalize()}"}), 404

        # Calculate mean, median, and standard deviation of surface pressures
        mean_pressure = statistics.mean(surface_pressures)
        median_pressure = statistics.median(surface_pressures)
        std_dev_pressure = statistics.stdev(surface_pressures) if len(surface_pressures) > 1 else 0

        # Round standard deviation to 2 decimal places
        std_dev_pressure = round(std_dev_pressure, 2)

        # Prepare response JSON
        result = {
            "meanPressure": mean_pressure,
            "medianPressure": median_pressure,
            "stdDevPressure": std_dev_pressure
        }

        # Return successful response
        return jsonify(result), 200

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error fetching pressure analysis data for {city}: {str(e)}")
        # Return error response
        return jsonify({"error": "Internal server error"}), 500

def fetch_surface_pressures(query):
    try:
        # Assume get_connection() is implemented to establish database connection
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        data = [row[0] for row in cursor.fetchall()]  # Extract surface pressures from fetched data
        connection.close()
        return data
    except Exception as e:
        print(f"Error fetching surface pressures: {str(e)}")
        return []  # Return empty list if there's an error

def sanitize(city):
    # Implement any necessary sanitation or validation of the city name here
    # Example: Convert to lowercase and replace spaces with underscores
    return city.lower().replace(" ", "_")

@app.route("/api/wind-speed/<city>")
def wind_speed_data(city):
    try:
        # Construct SQL query to fetch wind speed data for the specified city at 9 AM
        query = f"SELECT time, wind_speed_10m FROM {city.lower()}_weather WHERE strftime('%H', time) = '09'"
        
        # Fetch wind speed data from the database
        data = fetch_data(query)
        
        # Handle case where no data is returned
        if not data:
            return jsonify({"error": f"No wind speed data found for {city.capitalize()} at 9 AM"}), 404
        
        # Extract labels (time) and wind speeds from the fetched data
        labels = [entry[0] for entry in data]
        wind_speeds = [entry[1] for entry in data]
        
        # Prepare response JSON
        response = {
            "city": city.capitalize(),
            "labels": labels,
            "wind_speeds": wind_speeds
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error fetching wind speed data for {city}: {str(e)}")
        # Return error response
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/wind-speed-analysis/<city>")
def wind_speed_analysis(city):
    try:
        # Construct the SQL query to fetch wind speed data for the specified city
        query = f"SELECT wind_speed_10m FROM {city.lower()}_weather WHERE strftime('%H', time) = '09'"

        # Fetch wind speed data from the database using the fetch_data function
        data = fetch_data(query)

        # Handle case where no data is returned
        if not data:
            return jsonify({"error": f"No wind speed data found for {city.capitalize()} at 9 AM"}), 404

        # Extract wind speeds from the fetched data
        wind_speeds = data  # Use data directly

        # Calculate mean, median, and standard deviation of wind speeds
        mean_wind_speed = statistics.mean(wind_speeds)
        median_wind_speed = statistics.median(wind_speeds)
        std_deviation = statistics.stdev(wind_speeds)

        # Prepare the analysis data
        analysis_data = {
            "meanWindSpeed": mean_wind_speed,
            "medianWindSpeed": median_wind_speed,
            "standardDeviation": std_deviation
        }

        # Return the analysis data as a JSON response
        return jsonify(analysis_data), 200

    except Exception as e:
        # Handle any unexpected exceptions and return an error response
        return jsonify({"error": str(e)}), 500


# Route to render the temperature chart page
@app.route("/temperature")
def weather_chart():
    return render_template("temperature.html")

# Route to render the meteorological factors analysis page
@app.route("/meteorological-factors")
def meteorological_factors():
    return render_template("meteorological-factors.html")

if __name__ == "__main__":
    app.run(debug=True)
