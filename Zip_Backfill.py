import fiona
import argparse
from shapely.geometry import shape
from shapely.geometry import MultiPolygon
from shapely.geometry import Point

#command line parser
parser = argparse.ArgumentParser(description = 'Backfills zip code to single file')
parser.add_argument('input', help = 'file to backfill from')
parser.add_argument('output', help = 'file to to backfill to')
parser.add_argument('shape_file', help = 'a census ZCTA shape file')
args = parser.parse_args()

#construct list of zip polygons
with fiona.drivers():
	#open a shape file
	with fiona.open(args.shape_file, 'r') as source:
		#creating a list of polygons from the shape file
		zips = MultiPolygon([shape(pol['geometry']) for pol in source])
		#creating a list of tuples with the zip codes from the shape file and their order in the file
		zips_key = [(pol['properties']['ZCTA5CE10'], inx) for inx, pol in enumerate(source)]

output = open(args.output, 'w')
with open(args.input, 'r') as points:
	for point in points:
		s_point = point.split(',')
		#check for zip
		if s_point[7]: output.write(point)
		else:
			for inx, poly in enumerate(zips.geoms):
				#check is lon, lat of current row as a point is contained in each poly
				if poly.contains(Point(float(s_point[0]), float(s_point[1]))) == True:
					#zip of point is the zip of the found ZCTA
					s_point[7] = zips_key[inx][0]
					output.write(",".join(s_point))
					#stop searching
					break
			#if no ZCTA found
			else:
				s_point[7] = 'False'
				output.write(",".join(s_point))

output.close()




