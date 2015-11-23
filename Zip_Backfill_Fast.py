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

def find_zip(point, index):
	before = after = index
	while before >= 0 or after < len(sorted_key):
		if before == after:
			if zips.geoms[sorted_key[index][1]].contains(point) == True: 
				return (sorted_key[index][0], index)
			else:
				after += 1
				before -= 1
		else:
			if after < len(sorted_key):
				if zips.geoms[sorted_key[after][1]].contains(point) == True: 
					return (sorted_key[after][0], after)
				else: after += 1
			if before >= 0:
				if zips.geoms[sorted_key[before][1]].contains(point) == True: 
					return (sorted_key[before][0], before)
				else: before -= 1
	return('None', index)

#construct list of zip polygons
with fiona.drivers():
	with fiona.open('/Users/gudelk/Downloads/cb_2014_us_zcta510_500k/cb_2014_us_zcta510_500k.shp', 'r') as source:
		zips = MultiPolygon([shape(pol['geometry']) for pol in source])
		zips_key = [(pol['properties']['ZCTA5CE10'], inx) for inx, pol in enumerate(source)]
		sorted_key = sorted(zips_key)


output = open(args.output, 'w')
current_inx = 0
with open(args.input, 'r') as points:
	for point in points:
		print point
		s_point = point.split(',')
		if s_point[7]: output.write(point)
		else:
			result = find_zip(Point(float(s_point[0]), float(s_point[1])), current_inx)
			current_inx = result[1]
			s_point[7] = result[0]
			output.write(",".join(s_point))

output.close()




