import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

class CockroachDB:
    def __init__(self):
        self.connection = psycopg.connect(os.environ["CONNECTION_STRING"])

    def create_rsf_crowdometer(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS rsf_training (
                time TIMESTAMP,
                is_open BOOL,
                current_capacity INT,
                day_of_week INT,
                temperature INT,
                temp_feel INT,
                weather_code INT,
                wind_mph FLOAT,
                wind_degree INT,
                pressure_mb FLOAT,
                precipitation_mm FLOAT,
                humidity INT,
                cloudiness INT,
                uv_index FLOAT,
                gust_mph FLOAT,
                school_break STRING,
                is_holiday BOOL,
                is_rrr_week BOOL,
                is_finals_week BOOL,
                is_student_event BOOL
            );
        """

        with self.connection.cursor() as cursor:
            cursor.execute(create_table_sql)

        self.connection.commit()
    
    def drop_table(self, table_name):
        drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"

        with self.connection.cursor() as cursor:
            cursor.execute(drop_table_sql)
        
        self.connection.commit()

    def insert_only_crowdometer_data(self, time, current_capacity):
        insert_sql = """
        INSERT INTO rsf_training (time, current_capacity)
        VALUES (%(time)s, %(current_capacity)s)
        """

        data = {
            'time': time,
            'current_capacity': current_capacity
        }

        with self.connection.cursor() as cursor:
            cursor.execute(insert_sql, data)
        
        self.connection.commit()
    
    def get_all_rows(self):
        select_sql = "SELECT * FROM rsf_training"

        with self.connection.cursor() as cursor:
            cursor.execute(select_sql)
            rows = cursor.fetchall()
        
        return rows