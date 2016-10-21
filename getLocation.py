'''

Returns the neighborhood of the submitted coordinates

'''
from osgeo import ogr 
import numpy as np

drv = ogr.GetDriverByName('ESRI Shapefile') 
ds_in = drv.Open("shapefiles/nynta.shp")    #Get the contents of the shape file
lyr_in = ds_in.GetLayer(0)    #Get the shape file's first (and only) layer

# Define the indicies to return 
neighborhood = lyr_in.GetLayerDefn().GetFieldIndex("NTAName")
borough = lyr_in.GetLayerDefn().GetFieldIndex("BoroName")

geo_ref = lyr_in.GetSpatialRef()
point_ref=ogr.osr.SpatialReference()
point_ref.ImportFromEPSG(4326)
ctran=ogr.osr.CoordinateTransformation(point_ref,geo_ref)

def check(point):
	lon = float(point["lon"])
	lat = float(point["lat"])
	
	#Transform incoming longitude/latitude to the shapefile's projection
	[lon,lat,z]=ctran.TransformPoint(lon,lat)
	
	#Create a point
	pt = ogr.Geometry(ogr.wkbPoint)
	pt.SetPoint_2D(0, lon, lat)

	#Set up a spatial filter such that the only features we see when we
	#loop through "lyr_in" are those which overlap the point defined above
	lyr_in.SetSpatialFilter(pt)

	#Loop through the overlapped features and display the field of interest
	for feat_in in lyr_in:
		return feat_in.GetFieldAsString(neighborhood), feat_in.GetFieldAsString(borough)
	
	return np.nan, np.nan # If no matches return NaN
