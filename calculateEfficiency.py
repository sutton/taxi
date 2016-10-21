'''

Calculate the "efficiency" metric for all areas of Manhattan

'''
import pandas as pd
import numpy as np
import datetime

def getServiceTimes(df):
	df['day_of_week'] = df["rounded_pickup_datetime"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%A'))
	df['hour'] = df["rounded_pickup_datetime"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)
	
	df = df.drop(df[df["hour"]<6].index)
	df = df.drop(df[(df["hour"]<10) & (df["day_of_week"]=="Saturday")].index)
	df = df.drop(df[(df["hour"]<10) & (df["day_of_week"]=="Sunday")].index)
	df = df.drop(df[(df["hour"]>9) & (df["day_of_week"]=="Sunday")].index)
	
	return df
	
def getServiceArea(df):
	df = df[(df["pickup_borough"] == "Manhattan") | (df["pickup_borough"] == "Brooklyn")]
	df = df[(df["dropoff_borough"] == "Manhattan") | (df["dropoff_borough"] == "Brooklyn")]
	neighborhoods = ["Central Harlem North-Polo Grounds","Hamilton Heights",
	"Manhattanville","Washington Heights South","Washington Heights North","park-cemetery-etc-Manhattan","park-cemetery-etc-Manhattan",
	"Marble Hill-Inwood"]
	for n in neighborhoods:
		df = df[(df["pickup_neighborhood"] !=n) & (df["dropoff_neighborhood"]!=n)]
	return df

def getBrooklyn(df):
	df = df.drop(df[(df["pickup_borough"]=="Manhattan")&(df["dropoff_borough"]=="Brooklyn")].index)
	df = df.drop(df[(df["dropoff_borough"]=="Manhattan")&(df["pickup_borough"]=="Brooklyn")].index)
	return df

def getCrossBorough(df):
	df = df.drop(df[(df["dropoff_borough"]=="Brooklyn")&(df["pickup_borough"]=="Brooklyn")].index)
	return df
	
total = pd.DataFrame()
for i in np.arange(1,8):
	df = pd.read_csv("avoided_taxis/jan"+str(i)+".csv")
	df = getServiceArea(df) ## get only via service area
	df = getServiceTimes(df) ## get only hours  of operation 
	# df = getBrooklyn(df) ## get only rides within brooklyn
	# df = getCrossBorough(df) ## get only cross borough
	total = total.append(df)

efficiency = pd.DataFrame()
for n in total["pickup_neighborhood"].unique():
	avoided_taxis = np.sum(total[total["pickup_neighborhood"]==n]["avoided_taxis"])
	nEfficiency = pd.DataFrame({"avoided_taxis":avoided_taxis},index=[n])
	efficiency = efficiency.append(nEfficiency)

neighborhoods = pd.read_csv("neighborhoods.csv") ## Load neighborhoods which were omitted for the mapping
neighborhoods.index = neighborhoods[neighborhoods.columns[0]]

finalEfficiency = pd.concat([neighborhoods,efficiency],axis=1)
finalEfficiency = finalEfficiency.fillna(value=0)
finalEfficiency.to_csv("finalEfficiency.csv")
