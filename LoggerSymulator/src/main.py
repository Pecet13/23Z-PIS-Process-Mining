import time
from datetime import datetime, timedelta

from sqlalchemy import create_engine, text, exc
from urllib import parse
import argparse
from sqlalchemy.exc import IntegrityError


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


def transfer_logs(start_date):
    with source_engine.connect() as source_conn:
        query = text("SELECT TOP 1 * FROM IncidentLogs WHERE sys_created_on >= :start_date ORDER BY sys_created_on")
        result = source_conn.execute(query, {'start_date': start_date})
        row = result.fetchone()
        if not row:
            return False, None
        else:
            with target_engine.connect() as target_conn:
                insert_query = text("""
                                    INSERT INTO IncidentLogs (
                                        number, sys_created_on, sys_created_by, opened_at, resolved_at,
                                        reopened_time, activity_due, closed_at, closed_by, due_date,
                                        sla_due, contact_type, category, urgency, short_description,
                                        priority, state, escalation
                                    ) VALUES (
                                        :number, :sys_created_on, :sys_created_by, :opened_at, :resolved_at,
                                        :reopened_time, :activity_due, :closed_at, :closed_by, :due_date,
                                        :sla_due, :contact_type, :category, :urgency, :short_description,
                                        :priority, :state, :escalation
                                    );
                                """)
                row_dict = {column: value for column, value in zip(result.keys(), row)}
                try:
                    target_conn.execute(insert_query, row_dict)
                    target_conn.commit()
                except IntegrityError as e:
                    if 'PK__Logs__' in str(e) or 'primary key constraint' in str(e).lower():
                        print("    Record already exists.")
                    else:
                        print(f"Integrity error during data transfer: {e}")
                    return False, None
                except Exception as e:
                    print(f"Error during data transfer: {e}")
                    return False, None
            return True, row_dict['sys_created_on']


SRC_CONN_STR = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER=tcp:pis2023z.database.windows.net;"
    f"DATABASE=event_log_db;"
    f"UID=ondrasz@pis2023z;"
    f"PWD=alfanumeryczne1@;"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)
TARGET_CONN_STR = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER=tcp:pis2023z.database.windows.net;"
    f"DATABASE=PIS2023Z_db;"
    f"UID=ondrasz;"
    f"PWD=alfanumeryczne1@;"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)
source_encoded_cs = parse.quote_plus(SRC_CONN_STR)
target_encoded_cs = parse.quote_plus(TARGET_CONN_STR)
source_conn_str = f"mssql+pyodbc:///?odbc_connect={source_encoded_cs}"
target_conn_str = f"mssql+pyodbc:///?odbc_connect={target_encoded_cs}"
source_engine = create_engine(source_conn_str)
target_engine = create_engine(target_conn_str)


def main():
    # parser = argparse.ArgumentParser(description="Transfer logs from source to target database.")
    # parser.add_argument("--start_id", type=int, required=True, help="Starting log ID")
    # parser.add_argument("--time_sleep", type=int, required=True, help="Time to sleep between transfers (in seconds)")
    # args = parser.parse_args()
    date_format = '%Y-%m-%d %H:%M:%S'
    if test_connection(source_engine) and test_connection(target_engine):
        print("Connected to both databases.")
        start_date = datetime(2020, 1, 1, 0, 2, 15)
        while True:
            print(f"Transfering log from {start_date}...")
            transfer_output = transfer_logs(start_date)
            if transfer_output[0]:
                date_str = transfer_output[1]
                start_date = datetime.strptime(date_str, date_format)
                print(f"    Log {start_date} transferred.")
            print(f"    Waiting for 5 seconds...")
            start_date += timedelta(seconds=1)  # Increment the date by 1 day (adjust as needed)
            if transfer_output[0]:
                time.sleep(5)
            else:
                time.sleep(0.1)

    else:
        print("Connection to the databases failed.")


if __name__ == "__main__":
    main()


