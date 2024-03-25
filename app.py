from flask import Flask
import sqlconnect as mq

app = Flask(__name__)


# Route to display Madurai weather data
@app.route("/madurai_weather")
def madurai_weather():
    # Execute SQL query to fetch Madurai weather data from the database
    mq.mycursor.execute("SELECT * FROM madurai_weather")
    # Fetch all rows from the result set
    madurai_data = mq.mycursor.fetchall()
    # Return the data as a string (you can format it as needed)
    return str(madurai_data)


# Route to display Chennai weather data
@app.route("/chennai_weather")
def chennai_weather():
    # Execute SQL query to fetch Chennai weather data from the database
    mq.mycursor.execute("SELECT * FROM chennai_weather")
    # Fetch all rows from the result set
    chennai_data = mq.mycursor.fetchall()
    # Return the data as a string (you can format it as needed)
    return str(chennai_data)


if __name__ == "__main__":
    app.run(debug=True)
