import pandas as pd

raw = pd.read_csv(r"C:/Users/kerry/when2rsf/when2rsf/RSF_crowd_meter.csv")

raw.drop(['capacity_fulll','temp_max','pressure','humidity','temp','temp_feel','temp_min'], axis=1, inplace=True)


raw['Timestamp'] = pd.to_datetime(raw['Timestamp'])

raw['Year'] = raw["Timestamp"].dt.year
raw['Month'] = raw["Timestamp"].dt.month
raw['Day'] = raw["Timestamp"].dt.day
raw['Hour'] = raw["Timestamp"].dt.hour
raw['Minute'] = raw["Timestamp"].dt.minute

raw.drop('Timestamp', axis=1, inplace=True)

raw = raw.reindex(columns=['Year','Month','Day','Hour','Minute','current_count','capacity_ratio'])

print(raw.head(5))
