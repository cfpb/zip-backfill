import requests
import argparse

#command line parser
parser = argparse.ArgumentParser(description = 'Backfills zip code to single file')
parser.add_argument('input', help = 'OpenAddresses file with backfilled zip to check')
parser.add_argument('output', help = 'file to output accuracy data')
parser.add_argument('key', help = 'a file containing a valid google api key')
args = parser.parse_args()

key = open(args.key, 'r').read()
url_pre = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
url_post = '&key=' + key

#check address against google api
def check_address(row):
	parts = row.split(',')
	#construct url with lat and lon and send request
	result = (requests.get(url_pre + parts[1] + ',' + parts[0] + url_post)).json()
	#if google finds point
	if result['status'] == 'OK':
		for piece in reversed(result['results'][0]['address_components']):
			#look for post code
			if piece['types'][0] == 'postal_code':
				#check if post code is same as zip in file
				if piece['long_name'] == parts[7]:
					return 'Same'
				else:
					return piece['long_name']
		#if no postcode
		else:
			return 'Not Found'
	#if no result
	else:
		return 'Not Found'

output = open(args.output, 'w')
with open(args.input, 'r') as source:
	for row in source:
		if row[0] != '#': output.write(row.strip('\n') + ',' + check_address(row) + '\n')
		else: output.write(row)

output.close()
		