import pandas as pd
import os
import psycopg
from dotenv import load_dotenv
from cockroachdb import CockroachDB


load_dotenv()


raw = pd.read_csv(r"C:/Users/kerry/when2rsf/when2rsf/cleanedData.csv")

raw.drop(['ratio','temp','temp_feel','hour','minute','pressure','humidity','temp_min',"temp_max",'by15','minute15'], axis=1, inplace=True)


raw['Timestamp'] = pd.to_datetime(raw['by5'])

#raw['Year'] = raw["Timestamp"].dt.year
#raw['Month'] = raw["Timestamp"].dt.month
#raw['Day'] = raw["Timestamp"].dt.day   #November 13 is Sunday, (1), Monday (2), Tuesday (3)
#raw['Hour'] = raw["Timestamp"].dt.hour
#raw['Minute'] = raw["Timestamp"].dt.minute

raw.drop('by5', axis=1, inplace=True)

raw = raw.reindex(columns=['Timestamp','weekday','count'])
#print(raw.mean)
print(raw.head)

#db=CockroachDB()
#db.bulk_insert_crowdometer_data(raw['Timestamp'],raw['count'],raw['weekday'])
