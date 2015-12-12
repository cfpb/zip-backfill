'''
This code takes a file in the format of OpenAddresses.
However, this file must contain good rows with zip codes.
Pull_only_zip.py is meant to produce rows for this.
It then backfills each row and checks the backfill 
results against the existant zip codes and produces
a new file with those results
'''

from shapely.geometry import Point
import Zip_Backfill

def write_openaddresses_test(inputF, outputF, sorted_key, zips):
	output = open(outputF, 'w')
	current_inx = 0
	with open(inputF, 'r') as points:
		for point in points:
			s_point = (point.strip('\r\n')).split(',')
			if len(s_point) == 8: 
				s_point.append('')
			#run function find_zip with lon and lat of current row as a point and the index of the last found point
			result = Zip_Backfill.find_zip(Point(float(s_point[0]), float(s_point[1])), current_inx, sorted_key, zips)
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

if __name__ == '__main__':
	
	import argparse
	
	#command line parser
	parser = argparse.ArgumentParser(description = 'Backfills zip code to single file')
	parser.add_argument('input', help = 'OpenAddresses file to backfill from')
	parser.add_argument('output', help = 'file to to backfill to')
	parser.add_argument('shape_file', help = 'a census ZCTA shape file')
	args = parser.parse_args()

	zips_load = Zip_Backfill.import_zip(args.shape_file)
	write_openaddresses_test(args.input, args.output, zips_load[0], zips_load[1])
