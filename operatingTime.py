'''

Calculate the optimal operating times for rides originating in brooklyn

'''
import pandas as pd
import numpy as np
import datetime

def getBrooklyn(df):
	df = df[df["pickup_borough"] == "Brooklyn"]
	df = df[(df["dropoff_borough"] == "Manhattan") | (df["dropoff_borough"] == "Brooklyn")]
	return df
	
def getRoundedTime(df):
	def getHour(x):
		date = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
		return datetime.datetime(date.year,date.month,date.day,date.hour,0,0)
	def weekendTest(x):
		if x <5:
			return False
		else:
			return True
	df["rounded_pickup_datetime_hour"] = df["rounded_pickup_datetime"].apply(lambda x: getHour(x))
	df["rounded_pickup_hour"] = df["rounded_pickup_datetime"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)
	df['day_of_week'] = df["rounded_pickup_datetime"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%A'))
	df["weekday"] =  df["rounded_pickup_datetime"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').weekday())
	df["weekend"] = df["weekday"].apply(lambda x: weekendTest(x))
	return df

def groupRides(total,sorters,filename):
	result = pd.DataFrame()
	for key, group in total.groupby(sorters):
		print key 
		total_avoided_taxis = np.sum(group["avoided_taxis"])
		instance = pd.DataFrame({"total_avoided_taxis":total_avoided_taxis},index=[key])
		result = result.append(instance)
		result.to_csv(filename)
	return 
	
total = pd.DataFrame()
for i in np.arange(2,8):
	df = pd.read_csv("avoided_taxis/jan"+str(i)+".csv")
	df = getBrooklyn(df) ## get only rides within brooklyn
	df = getRoundedTime(df)
	total = total.append(df)

groupRides(total,["rounded_pickup_datetime_hour"],"weekly_taxis_avoided.csv") ## Aggregation potential for the week
groupRides(total[total["weekend"]==True],["rounded_pickup_hour"],"weekend_taxis_avoided.csv") ## Aggregation potential by hour for the week
groupRides(total[total["weekend"]==False],["rounded_pickup_hour"],"weekday_taxis_avoided.csv") ## Aggregation potential for the weekend
