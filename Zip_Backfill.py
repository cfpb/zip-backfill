import fiona
import argparse
from shapely.geometry import shape
from shapely.geometry import MultiPolygon
from shapely.geometry import Point

#command line parser
parser = argparse.ArgumentParser(description = 'Backfills zip code to single file')
parser.add_argument('input', help = 'file to backfill from')
parser.add_argument('output', help = 'file to to backfill to')
args = parser.parse_args()

#construct list of zip polygons
with fiona.drivers():
	with fiona.open('/Users/gudelk/Downloads/cb_2014_us_zcta510_500k/cb_2014_us_zcta510_500k.shp', 'r') as source:
		zips = MultiPolygon([shape(pol['geometry']) for pol in source])
		zips_key = [(pol['properties']['ZCTA5CE10'], inx) for inx, pol in enumerate(source)]
		sorted_key = sorted(zips_key)

output = open(args.output, 'w')
with open(args.input, 'r') as points:
	for point in points:
		print point
		s_point = point.split(',')
		if s_point[7]: output.write(point)
		else:
			for inx, poly in enumerate(zips.geoms):
				if poly.contains(Point(float(s_point[0]), float(s_point[1]))) == True:
					s_point[7] = zips_key[inx][0]
					output.write(",".join(s_point))
					break
			else:
				s_point[7] = 'False'
				output.write(",".join(s_point))

output.close()




