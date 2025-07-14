import pyodbc
import csv
# Database configuration
DB_SERVER = "hpsim01"
DB_NAME = "Insight_v50_0_161447876"
USERNAME = "svc-hpsim"
PASSWORD = "fbyPnGvXR5jXx06"
# Output file
OUTPUT_CSV = "hpsim_all_systems.csv"
def fetch_all_systems_and_write_to_csv():
    connection_string = f"DRIVER={{SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={USERNAME};PWD={PASSWORD}"
    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        # Query to fetch all systems
        cursor.execute("SELECT * FROM dbo.devices")  #table name (dbo.IPAddress, dbo.devices)
        rows = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]  # Get column names 
        # Write data to CSV
        with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # Write header
            writer.writerows(rows)  # Write rows
        print(f"Data successfully written to {OUTPUT_CSV}")
        # Close the connection
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    fetch_all_systems_and_write_to_csv()