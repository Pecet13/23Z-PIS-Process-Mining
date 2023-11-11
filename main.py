import pyodbc

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=pis2023z.database.windows.net;'
    r'DATABASE=PIS2023Z_db;'
    r'UID=ondrasz;'
    r'PWD=alfanumeryczne1@;'
)

# Replace with your database file path
db_file = "pis2023z.database.windows.net"



# SQL statement to select all records from the table
select_records_sql = """
SELECT * FROM sample_table
"""

try:
    # Connect to the SQLite database
    connection = pyodbc.connect(conn_str)

    cursor = connection.cursor()

    # Execute the SQL statement to select all records
    cursor.execute("CREATE TABLE new_tab (id INT, name VARCHAR(20))")
    cursor.execute("INSERT INTO new_tab VALUES (1, 'Chris'), (2, 'John'), (3, 'Mike')")
    cursor.execute("SELECT * FROM new_tab")
    # Fetch all the records
    records = cursor.fetchall()
    connection.commit()


    # Print the retrieved records
    for record in records:
        print(record)

    # Don't forget to close the cursor and connection when done
    cursor.close()
    connection.close()
    print("Connection closed.")
except pyodbc.Error as e:
    print("Error connecting to the database:", e)