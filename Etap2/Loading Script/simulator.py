import csv
import time
from datetime import datetime
from sqlalchemy import create_engine, text, exc
from urllib import parse
from sqlalchemy.exc import IntegrityError


def test_connection(engine):
    try:
        with engine.connect() as connection:
            # Dummy query just to test the connection
            connection.execute(text("SELECT 1"))
            return True
    except exc.SQLAlchemyError as e:
        print(f"Error connecting to the target database: {e}")
    return False


def transfer_log(log, engine):
    if record_exists(log, target_engine):
        print("    Record already exists.")
        return False

    try:
        with engine.connect() as target_conn:
            insert_query = text("""
                                INSERT INTO mining_data (
                                    CaseID, ActivityCode, StartTime, EndTime
                                ) VALUES (
                                    :Case, :ActivityCode, :Start, :End
                                );
                            """)
            target_conn.execute(insert_query, log)
            target_conn.commit()
    except IntegrityError:
        print("    Record already exists!")
        return False
    except Exception as e:
        print(f"Error during data transfer: {e}")
        return False
    return True


def read_logs_from_csv(csv_file_path, start_date):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            log_date = datetime.strptime(row['Start'], '%Y-%m-%d %H:%M:%S')
            if log_date >= start_date:
                yield row


def record_exists(log, engine):
    try:
        with engine.connect() as target_conn:
            query = text("""
                         SELECT 1 FROM mining_data WHERE
                         CaseID = :Case AND
                         ActivityCode = :ActivityCode AND
                         StartTime = :Start AND
                         EndTime = :End
                         """)
            result = target_conn.execute(query, log).fetchone()
            return result is not None
    except Exception as e:
        print(f"Error during existence check: {e}")
        return False


# Connection String and Engine Creation
SRC_CONN_STR = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER=tcp:pis.database.windows.net;"
    f"DATABASE=Main;"
    f"UID=ondrasz@pis;"
    f"PWD=alfanumeryczne@1;"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=60;"
)
target_encoded_cs = parse.quote_plus(SRC_CONN_STR)
target_conn_str = f"mssql+pyodbc:///?odbc_connect={target_encoded_cs}"
target_engine = create_engine(target_conn_str)


def main():
    csv_file_path = R'C:\Users\wojte\PycharmProjects\pis_scripts\Process Mining\sorted_csv_file.csv'
    start_date = datetime(2020, 1, 1, 0, 4, 25)

    if test_connection(target_engine):
        print("Connected to the target database.")
        for log in read_logs_from_csv(csv_file_path, start_date):
            print(f"Transferring log from {log['Start']}...")
            if transfer_log(log, target_engine):
                print(f"    Log from {log['Start']} transferred.")
                time.sleep(5)  # Adjust the sleep time as needed
            else:
                time.sleep(1)
    else:
        print("Connection to the target database failed.")


if __name__ == "__main__":
    main()
