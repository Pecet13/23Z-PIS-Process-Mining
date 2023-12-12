from urllib import parse
import pm4py
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, exc, text


def test_connection(engine):
    try:
        # Check connection to the source database
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM source_info"))
            row = result.fetchone()
            #print(f"Connected to the {row[1]} Database.")
            return True
    except exc.SQLAlchemyError as e:
        print(f"Error connecting to the source database: {e}")
    return False


# Database connection parameters
server = 'tcp:pis2023z.database.windows.net'
database = 'event_log_db'
username = 'ondrasz@pis2023z'
password = 'alfanumeryczne1@'  # Replace with your actual password
table_name = 'IncidentLogs'  # Replace with your actual table name

# Properly formatted connection string using urllib.parse.quote_plus
connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)
encoded_connection_string = parse.quote_plus(connection_string)
conn_str = f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}"
engine = create_engine(conn_str)
test_connection(engine)


csv_file_path = "incident.csv"  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# # Format datetime columns correctly
# datetime_cols = ['dateFinished', 'dueDate', 'planned', 'time:timestamp',
#                  'case:endDate', 'case:startDate', 'case:endDatePlanned', 'dateStop']
#
# for col in datetime_cols:
#     if col in df.columns:
#         # Convert to datetime, remove timezone, and format as string
#         df[col] = pd.to_datetime(df[col]).dt.tz_convert(None)
#         df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

df.to_sql(table_name, con=engine, if_exists='append', index=False)

print("Data loaded into database")