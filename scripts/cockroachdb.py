import os
import psycopg
from dotenv import load_dotenv

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
    time, current_capacity, day_of_week, temperature, temp_feel, weather_code, wind_mph,
    wind_degree, pressure_mb, precipitation_mm, humidity, cloudiness, uv_index, gust_mph
    ):
        insert_sql = """
        INSERT INTO rsf_training (time, current_capacity, day_of_week, temperature, temp_feel, weather_code, wind_mph, wind_degree, 
        pressure_mb, precipitation_mm, humidity, cloudiness, uv_index, gust_mph)
        VALUES (%(time)s, %(current_capacity)s, %(day_of_week)s, %(temperature)s, %(temp_feel)s, %(weather_code)s, %(wind_mph)s, 
         %(wind_degree)s, %(pressure_mb)s, %(precipitation_mm)s, %(humidity)s, %(cloudiness)s, %(uv_index)s, %(gust_mph)s)
        """

        data = {
            'time': time,
            'current_capacity': current_capacity,
            'day_of_week': day_of_week, 
            'temperature': temperature,
            'temp_feel': temp_feel,
            'weather_code': weather_code,
            'wind_mph': wind_mph,
            'wind_degree': wind_degree,
            'pressure_mb': pressure_mb,
            'precipitation_mm': precipitation_mm,
            'humidity': humidity,
            'cloudiness': cloudiness,
            'uv_index': uv_index,
            'gust_mph': gust_mph

        }

        with connection.cursor() as cursor:
            cursor.execute(insert_sql, data)
        
        connection.commit()
    
    def get_all_rows(self):
        select_sql = "SELECT * FROM rsf_training ORDER BY time DESC LIMIT 1 "

        with connection.cursor() as cursor:
            cursor.execute(select_sql)
            rows = cursor.fetchall()
        
        return rows

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
            cursor.execute("DELETE FROM rsf_training")
            connection.commit()
    
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

        def dates(self, timestamp):
            retrieve = """
                SELECT
                    DAY(timestamp) AS day,
                    MONTH(timestamp) AS month,
                    YEAR(timestamp) AS year
                FROM
                    rsf_training;
                """
            self.cursor.execute(retrieve)
                # Fetch the results
            results = self.cursor.fetchall()
            extracted_dates = {}
            for row in results:
                day, month, year = row
                extracted_dates.append({'day': day, 'month': month, 'year': year})
                # Return the list of dictionaries containing day, month, and year
            return extracted_dates
    
    def special_day(day, month, year):
        # Fall 2022
        {day: 3, month: 9, year: 2022, 'is_student_event': True} 
        {day: 5, month: 9, year: 2022, 'is_holiday': True} 
        {day: 10, month: 9, year: 2022, 'is_student_event': True} 
        {day: 24, month: 9, year: 2022, 'is_student_event': True} 
        {day: 22, month: 10, year: 2022, 'is_student_event': True} 
        {day: 29, month: 10, year: 2022, 'is_student_event': True} 
        {day: 11, month: 11, year: 2022, 'is_holiday': True} 
        {day: 19, month: 11, year: 2022, 'is_student_event': True} 
        {day: 23, month: 11, year: 2022, 'school_break': True} 
        {day: 24, month: 11, year: 2022, 'school_break': True} 
        {day: 25, month: 11, year: 2022, 'school_break': True, 'is_student_event': True} 
        {day: 26, month: 11, year: 2022, 'school_break': True} 
        {day: 27, month: 11, year: 2022, 'school_break': True} 
        {day: 5, month: 12, year: 2022, 'is_rrr_week': True}
        {day: 6, month: 12, year: 2022, 'is_rrr_week': True}
        {day: 7, month: 12, year: 2022, 'is_rrr_week': True}
        {day: 8, month: 12, year: 2022, 'is_rrr_week': True}
        {day: 9, month: 12, year: 2022, 'is_rrr_week': True}
        {day: 12, month: 12, year: 2022, 'is_finals_week': True}
        {day: 13, month: 12, year: 2022, 'is_finals_week': True}
        {day: 14, month: 12, year: 2022, 'is_finals_week': True}
        {day: 15, month: 12, year: 2022, 'is_finals_week': True}
        {day: 16, month: 12, year: 2022, 'is_finals_week': True}
        {day: 17, month: 12, year: 2022, 'is_student_event': True}
        {day: 23, month: 12, year: 2022, 'is_holiday': True} 
        {day: 26, month: 12, year: 2022, 'is_holiday': True}
        {day: 30, month: 12, year: 2022, 'is_holiday': True}
        {day: 2, month: 1, year: 2023, 'is_holiday': True}
        # Spring 2023
        {day: 16, month: 1, year: 2023, 'is_holiday': True}
        {day: 25, month: 2, year: 2023, 'is_holiday': True}
        {day: 26, month: 3, year: 2023, 'school_break': True}
        {day: 2, month: 3, year: 2023, 'school_break': True}
        {day: 27, month: 3, year: 2023, 'school_break': True}
        {day: 28, month: 3, year: 2023, 'school_break': True}
        {day: 29, month: 3, year: 2023, 'school_break': True}
        {day: 30, month: 3, year: 2023, 'school_break': True}
        {day: 31, month: 3, year: 2023, 'school_break': True}
        {day: 1, month: 4, year: 2023, 'school_break': True}
        {day: 2, month: 4, year: 2023, 'school_break': True}
        {day: 22, month: 4, year: 2023, 'is_student_event': True}
        {day: 1, month: 5, year: 2023, 'is_rrr_week': True}
        {day: 2, month: 5, year: 2023, 'is_rrr_week': True}
        {day: 3, month: 5, year: 2023, 'is_rrr_week': True}
        {day: 4, month: 5, year: 2023, 'is_rrr_week': True}
        {day: 5, month: 5, year: 2023, 'is_rrr_week': True}
        {day: 8, month: 5, year: 2023, 'is_finals_week': True}
        {day: 9, month: 5, year: 2023, 'is_finals_week': True}
        {day: 10, month: 5, year: 2023, 'is_finals_week': True}
        {day: 11, month: 5, year: 2023, 'is_finals_week': True}
        {day: 12, month: 5, year: 2023, 'is_finals_week': True}
        {day: 13, month: 5, year: 2023, 'is_student_event': True}
        {day: 29, month: 5, year: 2023, 'is_holiday': True}
        # Summer 2023
        {day: 19, month: 6, year: 2023, 'is_holiday': True}
        {day: 4, month: 7, year: 2023, 'is_holiday': True}
        # Fall 2023
        {day: 4, month: 9, year: 2023, 'is_holiday': True}
        {day: 9, month: 9, year: 2023, 'is_student_event': True}
        {day: 16, month: 9, year: 2023, 'is_student_event': True}
        {day: 30, month: 9, year: 2023, 'is_student_event': True}
        {day: 7, month: 10, year: 2023, 'is_student_event': True}
        {day: 28, month: 10, year: 2023, 'is_student_event': True}
        {day: 10, month: 11, year: 2023, 'is_holiday': True}
        {day: 11, month: 11, year: 2023, 'is_student_event': True}
        {day: 22, month: 11, year: 2023, 'school_break': True}
        {day: 23, month: 11, year: 2023, 'school_break': True}
        {day: 24, month: 11, year: 2023, 'school_break': True}
        {day: 25, month: 11, year: 2023, 'school_break': True}
        {day: 26, month: 11, year: 2023, 'school_break': True}
        {day: 4, month: 12, year: 2023, 'is_rrr_week': True}
        {day: 5, month: 12, year: 2023, 'is_rrr_week': True}
        {day: 6, month: 12, year: 2023, 'is_rrr_week': True}
        {day: 7, month: 12, year: 2023, 'is_rrr_week': True}
        {day: 8, month: 12, year: 2023, 'is_rrr_week': True}
        {day: 11, month: 12, year: 2023, 'is_finals_week': True}
        {day: 12, month: 12, year: 2023, 'is_finals_week': True}
        {day: 13, month: 12, year: 2023, 'is_finals_week': True}
        {day: 14, month: 12, year: 2023, 'is_finals_week': True}
        {day: 15, month: 12, year: 2023, 'is_finals_week': True}
        {day: 15, month: 12, year: 2023, 'is_student_event': True}
        {day: 25, month: 12, year: 2023, 'is_holiday': True}
        {day: 26, month: 12, year: 2023, 'is_holiday': True}
        {day: 1, month: 1, year: 2024, 'is_holiday': True}
        {day: 2, month: 1, year: 2024, 'is_holiday': True}
        # Spring 2024
        {day: 15, month: 1, year: 2024, 'is_holiday': True}
        {day: 19, month: 2, year: 2024, 'is_holiday': True}
        {day: 23, month: 3, year: 2024, 'school_break': True}
        {day: 24, month: 3, year: 2024, 'school_break': True}
        {day: 25, month: 3, year: 2024, 'school_break': True}
        {day: 26, month: 3, year: 2024, 'school_break': True}
        {day: 27, month: 3, year: 2024, 'school_break': True}
        {day: 28, month: 3, year: 2024, 'school_break': True}
        {day: 29, month: 3, year: 2024, 'school_break': True}
        {day: 30, month: 3, year: 2024, 'school_break': True}
        {day: 31, month: 3, year: 2024, 'school_break': True}
        # {Cal Day TBD}
        {day: 29, month: 4, year: 2024, 'is_rrr_week': True}
        {day: 30, month: 4, year: 2024, 'is_rrr_week': True}
        {day: 1, month: 5, year: 2024, 'is_rrr_week': True}
        {day: 2, month: 5, year: 2024, 'is_rrr_week': True}
        {day: 3, month: 5, year: 2024, 'is_rrr_week': True}
        {day: 6, month: 5, year: 2024, 'is_finals_week': True}
        {day: 7, month: 5, year: 2024, 'is_finals_week': True}
        {day: 8, month: 5, year: 2024, 'is_finals_week': True}
        {day: 9, month: 5, year: 2024, 'is_finals_week': True}
        {day: 10, month: 5, year: 2024, 'is_finals_week': True}
        {day: 11, month: 5, year: 2024, 'is_student_event': True}
        return None #continue this 
    
        # create dictionary for the special dates 
        
    
    #Make a function that grabs a date, (day, month, and year) and returns if the date is a holiday, school_break, finals_week
    #week before finals (rrr week), or if is a student event'''

    # what if it is two of the following categories above? write for both 
    
cockroach = CockroachDB()
#cockroach.bulk_insert_crowdometer_data(['2022-10-01 07:20:00', '2022-10-01 07:25:00', '2022-10-01 07:30:00', '2022-10-01 07:35:00'], [12, 34, 49, 69], [1, 7, 2, 4])
#cockroach.delete_rows()
#print(len(cockroach.get_all_rows()))
