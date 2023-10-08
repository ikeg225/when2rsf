import os
import psycopg
import datetime
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

    def insert_only_crowdometer_data(self, 
    time, current_capacity, day_of_the_week, temperature, temp_feel, weather, wind_mph,
    wind_degree, pressure_mb, precipitation_mm, humidity, cloudiness, uv_index, gust_mph
    ):
        insert_sql = """
        INSERT INTO rsf_training (time, current_capacity)
        VALUES (%(time)s, %(current_capacity)s)
        """

        data = {
            'time': time,
            'current_capacity': current_capacity,
            'day_of_the_week': 
            'temperature':
            'temp_feel':
            'weather':
            'wind_mph':
            'wind_degree':
            'pressure_mb':
            'precipitation_mm':
            'humidity':
            'coludiness':
            'uv_index':
            'gust_mph':
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
    
def fill_weather_data_in_rows():
    # Retrieve all timestamps from the 'rsf_training' table
    try:
        select_timestamps_sql = "SELECT DISTINCT time FROM rsf_training"
        
        with connection.cursor() as cursor:
            cursor.execute(select_timestamps_sql)
            timestamps = cursor.fetchall()

        # Iterate through the timestamps and fetch weather data for each
        for timestamp in timestamps:
            timestamp = timestamp[0]  # Extract the timestamp from the tuple

            # Round the timestamp to the nearest hour
            rounded_timestamp = timestamp.replace(minute=0, second=0, microsecond=0)

            # Convert the rounded timestamp to a formatted date string
            date_str = rounded_timestamp.strftime("%Y-%m-%d")

            # Get weather data for the entire day using the 'get_history' function
            weather_data = get_history(date_str)

            # Extract the hour from the rounded timestamp
            hour = rounded_timestamp.hour

            # Update the corresponding rows in the 'rsf_training' table with weather data for the hour
            update_sql = """
                UPDATE rsf_training
                SET 'day_of_week' = %(day_of_week)s,
                    temperature = %(temperature)s,
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
                WHERE EXTRACT(HOUR FROM time) = %(hour)s
            """

            with connection.cursor() as cursor:
                for time, weather_info in weather_data.items():
                    data = {
                        'day_of_week' : weather_info['day_of_week'],
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
                        'hour': hour,  # Use the hour extracted from the timestamp
                    }
                    cursor.execute(update_sql, data)

        # Commit the changes to the database
        connection.commit()
    except Exception as e:
        # Handle exceptions here
        print(f"An error occurred: {str(e)}")   

    
cockroach = CockroachDB()
#cockroach.bulk_insert_crowdometer_data(['2022-10-01 07:20:00', '2022-10-01 07:25:00', '2022-10-01 07:30:00', '2022-10-01 07:35:00'], [12, 34, 49, 69], [1, 7, 2, 4])
#cockroach.delete_rows()
print(len(cockroach.get_all_rows()))
