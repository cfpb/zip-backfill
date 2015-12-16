'''
Takes an OpenAddresses formatted file and writes every good row without or with a zipcode into an output file, defaults to without a zip code
'''

import argparse
import os

#command line parser
parser = argparse.ArgumentParser(description = 'Code that takes all good rows without zip codes')
parser.add_argument('input', help = 'A file containing some number of state OpenAddresses files')
parser.add_argument('output', help = 'The file to store found rows')
parser.add_argument('-z', '--zips', action = 'store_true', help = 'pull rows WITH zips, instead of without')
args = parser.parse_args()

def check_validity(l_split, row):
	#checks if a row is good i.e. that it contains a valid lat, lon, number, and street. Also 
	#checks if there are quotation marks as a proxy for parsing issues and whether the number has
	#any digits as a proxy for parsing an bad data issues
	if len(l_split) >= 8 and l_split[0] and l_split[1] and l_split[2] and l_split[3] and 'plot' not in l_split[2] and 'plot' not in l_split[3] \
	and '"' not in row and l_split[0].lower() != 'lon' and any(i.isdigit() for i in l_split[2]):
		if l_split[2].isdigit() == True: #if num is a digit check that it is greater than 0
			if int(l_split[2]) > 0: return True
			else: return False
		else: return True
	else: return False

def mylistdir(directory):
	#A specialized version of os.listdir() that ignores files that start with a leading period."""
	filelist = os.listdir(directory)
	return [x for x in filelist if not (x.startswith('.'))]

output = open(args.output, 'w') 
for state in mylistdir(args.input): #loop through states folders
	print(state) #just to record progress in the terminal
	if args.input.endswith('//'): state_dir = args.input + state #make the state file path
	else: state_dir = args.input + '//' + state #make the state file path
	output.write('#' + state +  '\n')
	for region in mylistdir(state_dir): #loop through the files in state folders
		if region.endswith('.csv'):
			with open(state_dir + '//' + region, 'r') as file:
				for row in file:
					row_split = row.split(',')
					#if collecting rows with no zips
					if not args.zips and len(row_split[7]) < 5 and check_validity(row_split, row): 
						#if no state use the abbreviation from the file name						
						if not row_split[6]: row_split[6] = state
						output.write(','.join(row_split))
					#if collecting rows with zips
					if args.zips and len(row_split[7]) = 5 and check_validity(row_split, row):
						#if no state use the abbreviation from the file name
						if not row_split[6]: row_split[6] = state
						output.write(','.join(row_split))
output.close()