import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

# Configuration for the connection pool
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "weather",
    "pool_name": "weather_pool",
    "pool_size": 5  # Adjust pool size as needed
}

# Create a connection pool
pool = mysql.connector.pooling.MySQLConnectionPool(**config)


def get_connection():
    try:
        connection = pool.get_connection()
        return connection
    except Error as e:
        print(f"Error getting connection from pool: {e}")
        return None


def fetch_weather_data(city, connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {city}_weather WHERE TIME(time) = '09:00:00';"
            )
            data = cursor.fetchall()
            return data
    except Error as e:
        print(f"Error fetching data for {city}: {e}")
        return None
