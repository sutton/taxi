'''

For each trip get the drop off / pick up neighbourhood / borough classification, direction of travel, day of week 

'''
import csv
import datetime
import getLocation
import getDirection
import numpy as np

columns=["trip_distance","passenger_count",
"dropoff_datetime","dropoff_latitude",
"dropoff_longitude","pickup_datetime",
"pickup_latitude","pickup_longitude"]

newColumns = ["pickup_neighborhood",
"pickup_borough","dropoff_neighborhood",
"dropoff_borough","trip_direction","day_of_week"]

for i in np.arange(1,8):
	trips = 0
	with open('formatted/jan'+str(i)+'.csv', 'wb') as csvfile:
		colstring= ""
		for col in columns + newColumns:
			colstring = colstring + col + ","
		colstring = colstring + "\n"
		csvfile.write(colstring)
		with open('data/jan'+str(i)+'.csv', 'rb') as f:
			reader = csv.DictReader(f)
			for row in reader:
				try:
					if row["dropoff_latitude"] !="0" and row["pickup_latitude"]!="0":
						
						## Get direction of travel, neighbourhoods, boroughs
						endpoint = {"lat":row["dropoff_latitude"],"lon":row["dropoff_longitude"]}
						startpoint = {"lat":row["pickup_latitude"],"lon":row["pickup_longitude"]}
						pickup_neighborhood,pickup_borough = getLocation.check(startpoint)
						dropoff_neighborhood,dropoff_borough = getLocation.check(endpoint)
						trip_direction = getDirection.vehicleBearing(endpoint, startpoint)
						pickup_datetime = datetime.datetime.strptime(row["pickup_datetime"], '%Y-%m-%d %H:%M:%S')
						day_of_week = pickup_datetime.strftime('%A')
						string = ""
						for c in columns:
							string= string +(row[c]+",")
						string = string + str(pickup_neighborhood)+","+str(pickup_borough)+","+str(dropoff_neighborhood)+","+str(dropoff_borough)+","+str(trip_direction)+","+str(day_of_week)+"\n"
						csvfile.write(string)
				except:
					pass
				print trips
				trips +=1				
			f.close()
			csvfile.close()

			
