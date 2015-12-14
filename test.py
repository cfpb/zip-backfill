import argparse
import os
import random

import pick_rand
import Zip_Backfill
import Self_Check
import Google_Check

#command line parser
parser = argparse.ArgumentParser(description = 'Tests zip_backfill accuraccy on a number of rows randomly selected from every file, choose one flag')
parser.add_argument('input', help = 'OpenAddresses file to take rows from')
parser.add_argument('output', help = 'a file to write results to')
parser.add_argument('shape_file', help = 'a census ZCTA shape file')
parser.add_argument('number', help = 'the number of rows to test')
parser.add_argument('-g', '--google', help = 'use google geocode search, attach a file with a google API key')
parser.add_argument('-r', '--reverse', help = 'use a reverse google geocode search, attach a file with a google API key')
parser.add_argument('-z', '--zip', help = 'search google with zip code, attach a file with a google API key')
parser.add_argument('-m', '--mapbox', help = 'reverse geocode from the mapbox API, attach a file with a mapbox API key')
parser.add_argument('-o', '--openaddresses', help = 'check against zips in openaddresses, use a file with zips as input', action = 'store_true')
args = parser.parse_args()


#check that a flag is picked

#create temp file for storing data
temp_rand = random.randint(1000000,9999999)

print 'picks rows'
#open temp file and write in random rows
pick_rand.write_rows(args.input, temp_rand, args.number)

print 'load poly'
#load shape file
zips_load = Zip_Backfill.import_zip(args.shape_file)

if args.openaddresses:

	print 'run test'
	
	Self_Check.write_openaddresses_test(temp_rand, args.output, zips_load[0], zips_load[1])

else:

	temp_backfill = random.randint(10000000,99999999)

	print 'backfill'

	Zip_Backfill.write_zip(temp_rand, temp_backfill, zips_load[0], zips_load[1])

	print 'run test'

	if args.google: write_test(temp_backfill, args.output, args.google, False, False, False)

	if args.reverse: write_test(temp_backfill, args.output, args.reverse, True, False, False)

	if args.zip: write_test(temp_backfill, args.output, args.zip, False, True, False)

	if args.mapbox: write_test(temp_backfill, args.output, args.mapbox, False, False, True)

	os.remove(temp_backfill)

os.remove(temp_rand)