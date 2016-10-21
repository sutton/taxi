'''

Calculate the avoided taxis by grouping the pickup, dropoff, and pickup time (rounded to 10 min)

'''
import datetime
import pandas as pd
import numpy as np
import math

def round_down(num, divisor):
    return num - (num%divisor)
	
def formatTimeColumn(x):
	date = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
	minutes = round_down(date.minute,10)
	return datetime.datetime(date.year,date.month,date.day,date.hour,minutes,0)
	
for i in np.arange(2,8):
	with open('avoided_taxis/jan'+str(i)+'.csv', 'wb') as csvfile:
		csvfile.write("frequency,pickup_neighborhood,dropoff_neighborhood,pickup_borough,dropoff_borough,rounded_pickup_datetime,avoided_taxis\n")
		
		df = pd.read_csv("formatted/jan"+str(i)+".csv",header=0)
		df["rounded_pickup_datetime"] = df["pickup_datetime"].apply(lambda x: formatTimeColumn(x))
		frequency = pd.DataFrame()
		for key, group in df.groupby(["pickup_neighborhood","dropoff_neighborhood","rounded_pickup_datetime"]):
			print key
			if key[0]!=key[1]:
				avoided_taxis = len(group) - math.ceil((np.sum(group["passenger_count"])/4.0))
				if avoided_taxis < 0 :
					avoided_taxis = 0
				string = str(len(group))+","+key[0]+","+key[1]+","+ group.ix[group.index[0]]["pickup_borough"]+","+group.ix[group.index[0]]["dropoff_borough"]+"," +key[2].strftime('%Y-%m-%d %H:%M:%S')+","+str(avoided_taxis)+"\n"
				csvfile.write(string)
		csvfile.close()