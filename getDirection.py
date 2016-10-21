import math

def vehicleBearing(endpoint, startpoint):
	x1 = float(endpoint['lat'])
	y1 = float(endpoint['lon'])
	x2 = float(startpoint['lat'])
	y2 = float(startpoint['lon'])

	def getAtan2(y, x):
		return math.atan2(y, x)
		
	radians = getAtan2((y1 - y2), (x1 - x2))

	compassReading = radians * (180 / math.pi)

	coordNames = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
	coordIndex = int(round((compassReading / 45),0))

	if (coordIndex < 0):
		coordIndex = coordIndex + 8

	return coordNames[coordIndex]; # returns the coordinate value
