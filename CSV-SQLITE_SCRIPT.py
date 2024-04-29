import sqlite3
import csv

# SQLite database file path
db_file = 'weather.db'

# Function to create SQLite database from CSV file
def create_sqlite_db_from_csv(csv_files, db_file):
    # Establish SQLite connection
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Iterate over CSV files and corresponding table names
    for csv_file, table_name in csv_files.items():
        # Construct full path to CSV file using relative path
        csv_path = f'./{csv_file}'  # Assuming CSV files are in the same directory as the script

        # Read CSV file and get headers
        with open(csv_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Read the headers from the CSV file

            # Create SQLite table based on CSV headers
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(f'{header} TEXT' for header in headers)})"
            cursor.execute(create_table_sql)

            # Reopen CSV file and recreate CSV reader for data insertion
            with open(csv_path, 'r', newline='') as file:
                csv_reader = csv.reader(file)  # Recreate CSV reader
                next(csv_reader)  # Skip headers

                # Insert data into SQLite table
                insert_sql = f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(headers))})"
                for row in csv_reader:
                    cursor.execute(insert_sql, row)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"SQLite database '{db_file}' created from CSV files")

# Define dictionary mapping CSV file names to table names
csv_files = {
    'chennai_weather.csv': 'chennai_weather',
    'madurai_weather.csv': 'madurai_weather'
}

# Call the function to create SQLite database from CSV files
create_sqlite_db_from_csv(csv_files, db_file)
