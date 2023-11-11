import pyodbc

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=pis2023z.database.windows.net;'
    r'DATABASE=PIS2023Z_db;'
    r'UID=ondrasz;'
    r'PWD=alfanumeryczne1@;'
)

try:
    # Connect to the SQLite database
    connection = pyodbc.connect(conn_str)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM new_tab")
    # Fetch all the records
    records = cursor.fetchall()
    connection.commit()

    for record in records:
        print(record)

    cursor.close()
    connection.close()
    print("Connection closed.")
except pyodbc.Error as e:
    print("Error connecting to the database:", e)
