import fiona
from shapely.geometry import shape
from shapely.geometry import MultiPolygon
from shapely.geometry import Point

#a search function that checks the last ZCTA found and then ZCTAs radiating out from it
def find_zip(point, index, sorted_key, zips):
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

def import_zip(shape_file):
	#construct list of zip polygons
	with fiona.drivers():
		#open a shape file
		with fiona.open(shape_file, 'r') as source:
			#creating a list of polygons from the shape file
			zips = MultiPolygon([shape(pol['geometry']) for pol in source])
			#creating a list of tuples with the zip codes from the shape file and their order in the file
			zips_key = [(pol['properties']['ZCTA5CE10'], inx) for inx, pol in enumerate(source)]
			return (sorted(zips_key), zips)


def write_zip(outputF, inputF, sorted_key, zips):
	output = open(outputF, 'w')
	current_inx = 0
	with open(inputF, 'r') as points:
		for point in points:
			s_point = point.split(',')
			if len(s_point) == 8: s_point.append('\r\n')
			#check for zip
			if len(s_point[7]) > 4 : output.write(point)
			else:
				#run function find_zip with lon and lat of current row as a point and the index of the last found point
				result = find_zip(Point(float(s_point[0]), float(s_point[1])), current_inx, sorted_key, zips)
				#set current_inx to the index of the last point found
				current_inx = result[1]
				#zip of point is the zip of the found ZCTA
				s_point[7] = result[0]
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

	zips_load = import_zip(args.shape_file)
	write_zip(args.output, args.input, zips_load[0], zips_load[1])
