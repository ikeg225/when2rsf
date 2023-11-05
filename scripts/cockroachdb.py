import os
import psycopg
from dotenv import load_dotenv
import datetime 
import pandas as pd
from weather import get_history

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
    

    def insert_only_crowdometer_data(self, 
        time, current_capacity, day_of_week, temperature, temp_feel, weather_code, wind_mph,
        wind_degree, pressure_mb, precipitation_mm, humidity, cloudiness, uv_index, gust_mph,
        school_break, is_holiday, is_rrr_week, is_finals_week, is_student_event
    ):
        insert_sql = """
        INSERT INTO rsf_training (time, current_capacity, day_of_week, temperature, temp_feel, weather_code, wind_mph, wind_degree, 
        pressure_mb, precipitation_mm, humidity, cloudiness, uv_index, gust_mph, school_break, is_holiday, is_rrr_week, is_finals_week, is_student_event)
        VALUES (%(time)s, %(current_capacity)s, %(day_of_week)s, %(temperature)s, %(temp_feel)s, %(weather_code)s, %(wind_mph)s, 
         %(wind_degree)s, %(pressure_mb)s, %(precipitation_mm)s, %(humidity)s, %(cloudiness)s, %(uv_index)s, %(gust_mph)s, 
         %(school_break)s, %(is_holiday)s, %(is_rrr_week)s, %(is_finals_week)s, %(is_student_event)s)
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
            'gust_mph': gust_mph,
            'school_break': school_break, 
            'is_holiday': is_holiday, 
            'is_rrr_week': is_rrr_week, 
            'is_finals_week': is_finals_week, 
            'is_student_event': is_student_event
        }

        with self.connection.cursor() as cursor:
            cursor.execute(insert_sql, data)
        
        self.connection.commit()
    
    def get_all_rows(self):
        select_sql = "SELECT * FROM rsf_training ORDER BY time DESC LIMIT 5"

        with self.connection.cursor() as cursor:
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

        with self.connection.cursor() as cursor:
            for batch in data_batches:
                batch_dict = [{'time': row[0], 'current_capacity': row[1], 'day_of_week': row[2]} for row in batch]
                cursor.executemany(inserts_sql, batch_dict)
                self.connection.commit()
                print(batch_dict)

    def delete_rows(self):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM rsf_training")
            self.connection.commit()
    
    def delete_on_timestamp(self, timestamp):
        # Create a cursor
        cursor = self.connection.cursor()

        # Define the DELETE statement
        delete_query = "DELETE FROM rsf_training WHERE time = %s"

        # Execute the DELETE statement with the provided timestamp
        cursor.execute(delete_query, (timestamp,))

        # Commit the transaction
        self.connection.commit()

        # Close the cursor and the connection
        cursor.close()

    def backfill_dates(self, timestamps, event, event_value):
        query = """
            UPDATE rsf_training
            SET {event} = %(event_value)s
            WHERE rsf_training.time = %(timestamp)s
        """.format(event=event)

        with self.connection.cursor() as cursor:
            for timestamp in timestamps:
                cursor.execute(query, {'timestamp': timestamp, 'event_value': event_value})
        self.connection.commit()
        
    def special_day(self, timestamp):
        # Fall 2022
        special_days_dictionary = {
        '9/3/2022': ['is_student_event'],
        '9/5/2022': ['is_holiday'], 
        '9/10/2022': ['is_student_event'], 
        '9/24/2022': ['is_student_event'], 
        '10/22/2022': ['is_student_event'], 
        '10/29/2022': ['is_student_event'], 
        '11/11/2022': ['is_holiday'], 
        '11/19/2022': ['is_student_event'], 
        '11/23/2022': ['school_break'], 
        '11/24/2022': ['school_break'], 
        '11/25/2022': ['school_break','is_student_event'], 
        '11/26/2022': ['school_break'], 
        '11/27/2022': ['school_break'], 
        '12/5/2022': ['is_rrr_week'],
        '12/6/2022': ['is_rrr_week'],
        '12/7/2022': ['is_rrr_week'],
        '12/9/2022': ['is_rrr_week'],
        '12/9/2022': ['is_rrr_week'],
        '12/12/2022': ['is_finals_week'],
        '12/13/2022': ['is_finals_week'],
        '12/14/2022': ['is_finals_week'],
        '12/15/2022': ['is_finals_week'],
        '12/16/2022': ['is_finals_week'],
        '12/17/2022': ['is_student_event'],
        '12/23/2022': ['is_holiday'], 
        '12/26/2022': ['is_holiday'],
        '12/30/2022': ['is_holiday'],
        '1/2/2023': ['is_holiday'],
        # Spring 2023
        '1/16/2023': ['is_holiday'],
        '2/25/2023': ['is_holiday'],
        '3/26/2023': ['school_break'],
        '3/27/2023': ['school_break'],
        '3/28/2023': ['school_break'],
        '3/29/2023': ['school_break'],
        '3/30/2023': ['school_break'],
        '3/1/2023': ['school_break'],
        '4/1/2023': ['school_break'],
        '4/2/2023': ['school_break'],
        '4/22/2023': ['is_student_event'],
        '5/1/2023': ['is_rrr_week'],
        '5/2/2023': ['is_rrr_week'],
        '5/3/2023': ['is_rrr_week'],
        '5/4/2023': ['is_rrr_week'],
        '5/5/2023': ['is_rrr_week'],
        '5/8/2023': ['is_finals_week'],
        '5/9/2023': ['is_finals_week'],
        '5/10/2023': ['is_finals_week'],
        '5/11/2023': ['is_finals_week'],
        '5/12/2023': ['is_finals_week'],
        '5/13/2023': ['is_student_event'],
        '5/29/2023': ['is_holiday'],
        # Summer 2023
        '6/19/2023': ['is_holiday'],
        '7/4/2023': ['is_holiday'],
        # Fall 2023
        '9/4/2023': ['is_holiday'],
        '9/9/2023': ['is_student_event'],
        '9/16/2023': ['is_student_event'],
        '9/30/2023': ['is_student_event'],
        '10/7/2023': ['is_student_event'],
        '10/28/2023': ['is_student_event'],
        '11/10/2023': ['is_holiday'],
        '11/11/2023': ['is_student_event'],
        '11/22/2023': ['school_break'],
        '11/23/2023': ['school_break'],
        '11/24/2023': ['school_break'],
        '11/25/2023': ['school_break'],
        '11/26/2023': ['school_break'],
        '12/4/2023': ['is_rrr_week'],
        '12/5/2023': ['is_rrr_week'],
        '12/6/2023': ['is_rrr_week'],
        '12/7/2023': ['is_rrr_week'],
        '12/8/2023': ['is_rrr_week'],
        '12/11/2023': ['is_finals_week'],
        '12/12/2023': ['is_finals_week'],
        '12/13/2023': ['is_finals_week'],
        '12/14/2023': ['is_finals_week'],
        '12/15/2023': ['is_student_event','is_finals_week'],
        '12/25/2023': ['is_holiday'],
        '12/26/2023': ['is_holiday'],
        '1/1/2024': ['is_holiday'],
        '1/2/2024': ['is_holiday'],
        # Spring 2024
        '1/15/2024': ['is_holiday'],
        '2/19/2024': ['is_holiday'],
        '3/23/2024': ['school_break'],
        '3/24/2024': ['school_break'],
        '3/25/2024': ['school_break'],
        '3/26/2024': ['school_break'],
        '3/27/2024': ['school_break'],
        '3/28/2024': ['school_break'],
        '3/29/2024': ['school_break'],
        '3/30/2024': ['school_break'],
        '3/31/2024': ['school_break'],
        # {Cal Day TBD}
        '4/29/2024': ['is_rrr_week'],
        '4/30/2024': ['is_rrr_week'],
        '5/1/2024': ['is_rrr_week'],
        '5/2/2024': ['is_rrr_week'],
        '5/3/2024': ['is_rrr_week'],
        '5/6/2024': ['is_finals_week'],
        '5/7/2024': ['is_finals_week'],
        '5/8/2024': ['is_finals_week'],
        '5/9/2024': ['is_finals_week'],
        '5/10/2024': ['is_finals_week'],
        '5/11/2024': ['is_student_event']
        }

        TimeStamp = pd.to_datetime(timestamp)
        dayInput = TimeStamp.day
        monthInput = TimeStamp.month
        yearInput = TimeStamp.year
        dateInput = f"{monthInput}/{dayInput}/{yearInput}"

        if dateInput in special_days_dictionary:
            event = special_days_dictionary[dateInput]
            return event
        return []
    
    def use_backfill_dates(self):
        cockroach = CockroachDB()

        start_date = datetime.datetime(2022, 10, 1, 7, 20, 0)
        end_date = datetime.datetime(2023, 9, 21, 21, 20, 0)

        interval = datetime.timedelta(minutes=5)

        current_date = start_date
        rrr_dates = []
        holiday_dates = []
        finals_dates = []
        student_event_dates = []
        break_dates = []

        while (current_date <= end_date):
            if 'is_rrr_week' in cockroach.special_day(current_date):
                rrr_dates.append(current_date)
            if 'is_holiday' in cockroach.special_day(current_date):
                holiday_dates.append(current_date)
            if 'is_finals_week' in cockroach.special_day(current_date):
                finals_dates.append(current_date)
            if 'is_student_event' in cockroach.special_day(current_date):
                student_event_dates.append(current_date)
            if 'school_break' in cockroach.special_day(current_date):
                break_dates.append(current_date)
            current_date += interval

        cockroach.backfill_dates(rrr_dates, 'is_rrr_week', True)
        cockroach.backfill_dates(holiday_dates, 'is_holiday', True)
        cockroach.backfill_dates(finals_dates, 'is_finals_week', True)
        cockroach.backfill_dates(student_event_dates, 'is_student_event', True)
        cockroach.backfill_dates(break_dates, 'school_break', True)
                
        return None

    def fill_weather_data_in_rows(self):
        # Retrieve all timestamps from the 'rsf_training' table
        try:
            select_timestamps_sql = "SELECT DISTINCT time FROM rsf_training WHERE time >= %s"
            with self.connection.cursor() as cursor:
                timestampval = (datetime.datetime(2023, 10, 19),) #Make sure the change this to 1 year past to real time
                cursor.execute(select_timestamps_sql, timestampval) 
                timestamps = cursor.fetchall()
            self.connection.commit()

            done = set()

            # Iterate through the timestamps and fetch weather data for each
            for timestamp in timestamps:
                timestamp = timestamp[0]  # Extract the timestamp from the tuple

                # Round the timestamp to the nearest hour
                rounded_timestamp = timestamp.replace(minute=0, second=0, microsecond=0)

                # Convert the rounded timestamp to a formatted date string
                date_str = rounded_timestamp.strftime("%Y-%m-%d")

                if date_str in done:
                    continue
                else:
                    done.add(date_str)
                
                print(date_str)

                # Get weather data for the entire day using the 'get_history' function
                weather_data = get_history(date_str)

                # Update the corresponding rows in the 'rsf_training' table with weather data for the hour
                update_sql = """
                    UPDATE rsf_training
                    SET day_of_week = %(day_of_week)s,
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
                    WHERE date_trunc('hour', time) = %(timestamp)s;
                """

                with self.connection.cursor() as cursor:
                    for time, weather_info in weather_data.items():
                        new_timestamp = datetime.datetime(rounded_timestamp.year, rounded_timestamp.month, rounded_timestamp.day, datetime.datetime.strptime(time, "%Y-%m-%d %H:%M").hour)
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
                            'timestamp': new_timestamp
                        }
                        cursor.execute(update_sql, data)
                self.connection.commit()            
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
    
    


            

        
        
 

    
if __name__ == "__main__":
    cockroach = CockroachDB()
    #cockroach.bulk_insert_crowdometer_data(['2022-10-01 07:20:00', '2022-10-01 07:25:00', '2022-10-01 07:30:00', '2022-10-01 07:35:00'], [12, 34, 49, 69], [1, 7, 2, 4])
    #cockroach.delete_rows()
    #print(len(cockroach.get_all_rows()))
    #print(cockroach.get_all_rows())   
    #print(cockroach.special_day(timestamp = '2024-5-25 14:30:00'))
    # cockroach.use_backfill_dates()
    #cockroach.use_backfill_dates()

