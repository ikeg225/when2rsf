import os
import psycopg
from dotenv import load_dotenv
from weather import get_history

load_dotenv()

connection = psycopg.connect(os.environ["CONNECTION_STRING"])

class CockroachDB:
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

        with connection.cursor() as cursor:
            cursor.execute(create_table_sql)

        connection.commit()
    
    def drop_table(self, table_name):
        drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"

        with connection.cursor() as cursor:
            cursor.execute(drop_table_sql)
        
        connection.commit()

    def insert_only_crowdometer_data(self, time, current_capacity):
        insert_sql = """
        INSERT INTO rsf_training (time, current_capacity)
        VALUES (%(time)s, %(current_capacity)s)
        """

        data = {
            'time': time,
            'current_capacity': current_capacity
        }

        with connection.cursor() as cursor:
            cursor.execute(insert_sql, data)
        
        connection.commit()
    
    def get_all_rows(self):
        select_sql = "SELECT * FROM rsf_training"

        with connection.cursor() as cursor:
            cursor.execute(select_sql)
            rows = cursor.fetchall()
        
        return rows

    def update_rows(weather_data):
        update_sql = """
        UPDATE rsf_training
        SET temperature = %(temperature)s,
            temp_feel = %(temp_feel)s,
            weather_code = %(weather_code)s,
            wind_mph = %(wind_mph)s,
            wind_degree = %(wind_degree)s,
            pressure_mb = %(pressure_mb)s,
            precipitation_mm = %(precipitation_mm)s,
            humidity = %(humidity)s,
            cloudiness = %(cloudiness)s,
            uv_index = %(uv_index)s,
            gust_mph = %(gust_mph)s
        WHERE time = %(time)s
        """

        with connection.cursor() as cursor:
            for date, weather_info in weather_data.items():
                data = {
                    'temperature': weather_info['temperature'],
                    'temp_feel': weather_info['temp_feel'],
                    'weather_code': weather_info['weather_code'],
                    'wind_mph': weather_info['wind_mph'],
                    'wind_degree': weather_info['wind_degree'],
                    'pressure_mb': weather_info['pressure_mb'],
                    'precipitation_mm': weather_info['precipitation_mm'],
                    'humidity': weather_info['humidity'],
                    'cloudiness': weather_info['cloudiness'],
                    'uv_index': weather_info['uv_index'],
                    'gust_mph': weather_info['gust_mph'],
                    'time': date
                }
                cursor.execute(update_sql, data)
        
        connection.commit()

    def bulk_insert_crowdometer_data(self, time_series, current_capacity_series, day_of_week):
        inserts_sql = """
        INSERT INTO rsf_training (time, current_capacity, day_of_week)
        VALUES (%(time)s, %(current_capacity)s, %(day_of_week)s)
        """
    
        # Assuming time_series, current_capacity_series, and day_of_week are lists
        big_data = list(zip(time_series, current_capacity_series, day_of_week))
    
        batch_size = 500  # Batch size to send 500 rows at a time

        data_batches = [big_data[i:i + batch_size] for i in range(0, len(big_data), batch_size)]

        with connection.cursor() as cursor:
            for batch in data_batches:
                batch_dict = [{'time': row[0], 'current_capacity': row[1], 'day_of_week': row[2]} for row in batch]
                cursor.executemany(inserts_sql, batch_dict)
                connection.commit()
                print(batch_dict)

    def delete_rows(self):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE rsf_training")

    
cockroach = CockroachDB()
#cockroach.bulk_insert_crowdometer_data(['2022-10-01 07:20:00', '2022-10-01 07:25:00', '2022-10-01 07:30:00', '2022-10-01 07:35:00'], [12, 34, 49, 69], [1, 7, 2, 4])
#cockroach.delete_rows()
print(len(cockroach.get_all_rows()))
