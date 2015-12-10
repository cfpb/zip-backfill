'''
This code takes an OpenAddresses file with zip codes
it then backfills each row and checks the backfill 
results against the existant zip codes and produces
a new file with the results

Pull_only_zip.py is meant to produce rows for this
'''

import fiona
import argparse
from shapely.geometry import shape
from shapely.geometry import MultiPolygon
from shapely.geometry import Point

#command line parser
parser = argparse.ArgumentParser(description = 'Backfills zip code to single file')
parser.add_argument('input', help = 'OpenAddresses file to backfill from')
parser.add_argument('output', help = 'file to to backfill to')
parser.add_argument('shape_file', help = 'a census ZCTA shape file')
args = parser.parse_args()

#a search function that checks the last ZCTA found and then ZCTAs radiating out from it
def find_zip(point, index):
	#set counters that move out from index of last found point
	before = after = index
	while before >= 0 or after < len(sorted_key):
		#first check last found index
		if before == after:
			if zips.geoms[sorted_key[index][1]].contains(point) == True: 
				#return zip and index
				return (sorted_key[index][0], index)
			#move counters
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
	#if no ZCTA found
	return('None', index)

#construct list of zip polygons
with fiona.drivers():
	#open a shape file
	with fiona.open(args.shape_file, 'r') as source:
		#creating a list of polygons from the shape file
		zips = MultiPolygon([shape(pol['geometry']) for pol in source])
		#creating a list of tuples with the zip codes from the shape file and their order in the file
		zips_key = [(pol['properties']['ZCTA5CE10'], inx) for inx, pol in enumerate(source)]
		sorted_key = sorted(zips_key)


output = open(args.output, 'w')
current_inx = 0
with open(args.input, 'r') as points:
	for point in points:
		s_point = (point.strip('\r\n')).split(',')
		if len(s_point) == 8: 
			s_point.append('')
		#run function find_zip with lon and lat of current row as a point and the index of the last found point
		result = find_zip(Point(float(s_point[0]), float(s_point[1])), current_inx)
		#set current_inx to the index of the last point found
		current_inx = result[1]
		#if zcta zip is same as on file
		if result[0] == s_point[7]: s_point[8] = 'same'
		#if no zcta zip is found
		elif result[0] == 'None': s_point[8] = 'None'
		#if zcta is not the same as on file write in found zip
		else: s_point[8] = result[0]
		output.write(",".join(s_point) + '\n')

output.close()
