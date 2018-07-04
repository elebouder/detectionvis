import gdal
from gdal import osr, ogr

rasterfile = ""
csvfile = ""
csvname = (csvfile.split('/')[-1]).split('.')[0]

# use a dictionary reader so we can access by field name


# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource(csvname + ".shp")

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
layer = data_source.CreateLayer(csvname + "_Aggregations", srs, ogr.wkbPoint)

# Add the fields we're interested in
field_name = ogr.FieldDefn("Name", ogr.OFTString)
field_name.SetWidth(24)
layer.CreateField(field_name)
layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))

with open(csvfile, 'r') as csvf:
    reader = csv.DictReader(csvf)
    # Process the text file and add the attributes and features to the shapefile
    for row in reader:
        # create the feature
        feature = ogr.Feature(layer.GetLayerDefn())
        # Set the attributes using the values from the delimited text file
        feature.SetField("Name", row['geohash'])
        feature.SetField("Latitude", row['c_y'])
        feature.SetField("Longitude", row['c_x'])

  	# create the WKT for the feature using Python string formatting
  	wkt = "POINT(%f %f)" %  (float(row['Longitude']) , float(row['Latitude']))

	# Create the point from the Well Known Txt
  	point = ogr.CreateGeometryFromWkt(wkt)

  	# Set the feature geometry using the point
  	feature.SetGeometry(point)
  	# Create the feature in the layer (shapefile)
  	layer.CreateFeature(feature)
  	# Dereference the feature
	feature = None


"""
src = gdal.Open(infile)
src_b = src.GetRasterBand(1)
src_g = src.GetRasterBand(2)
src_r = src.GetRasterBand(3)
prj = src.GetProjection()

switcher = {
            'WGS 84 / UTM zone 8N': 32608,
            'WGS 84 / UTM zone 9N': 32609,
            'WGS 84 / UTM zone 10N': 32610,
            'WGS 84 / UTM zone 11N': 32611,
            'WGS 84 / UTM zone 12N': 32612
        }

srs = osr.SpatialReference(wkt=prj)
if srs.IsProjected():
	projcs = srs.GetAttrValue('projcs')
        print projcs
        epsg = switcher.get(projcs, 'nothing')

if epsg == 'nothing':
	print 'projection not in current list of projections handled by this code'
        sys.exit(1)

# epsg is 8901 for projected, 4326 for decimal lat/lon
pproj = pyproj.Proj(init='epsg:%s' % epsg)
praw = pyproj.Proj(init='epsg:4326')

"""