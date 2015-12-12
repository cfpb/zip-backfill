'''
Runs through an OpenAddresses formatted file and checks the zip codes present against google or mapbox and output the rows to another file with the web API results
'''

import requests

#check address against google api
def check_address_reverse(parts, session, key):
	url_pre = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
	url_post = '&key=' + key
	#construct url with lat and lon and send request
	result = (session.get(url_pre + parts[1] + ',' + parts[0] + url_post)).json()
	return parse_google_response(result, parts)

def check_address(parts, session, key):
	url_pre = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	url_post = '&key=' + key
	#construct url with address and send request
	result = (session.get(url_pre + (parts[2] + ' ' + parts[3] + ', ' + parts[4] + ', ' + parts[6]).replace(' ', '+') + url_post)).json()
	return parse_google_response(result, parts)

def check_address_zip(parts, session, key):
	url_pre = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	url_post = '&key=' + key
	#construct url with address and send request
	result = (session.get(url_pre + (parts[2] + ' ' + parts[3] + ', ' + parts[4] + ', ' + parts[6] + ' ' + parts[7]).replace(' ', '+') + url_post)).json()
	return parse_google_response(result, parts)

def check_address_mapbox(parts, session, key):
	url_pre = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
	url_post = '.json?types=postcode&access_token=' + key
	result = (session.get(url_pre + parts[0] + ',' + parts[1] + url_post)).json()
	if result['features']:
		if result['features'][0]['text'] == parts[7]:
			return 'Same'
		else:
			return result['features'][0]['text']
	else: return 'Not Found'
	
def parse_google_response(result, parts):
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

def write_test(inputF, outputF, keyF, reverse, zips, mapbox):
	key = open(keyF, 'r').read()
	with requests.Session() as google:
		output = open(outputF, 'a')
		with open(inputF, 'r') as source:
			for row in source:
				parts = (row.strip('\r\n')).split(',')
				if parts[7] == 'None': output.write(','.join(parts + ['None']) + '\n')
				elif mapbox: output.write(','.join(parts + [check_address_mapbox(parts, google, key)]) + '\n')
				elif reverse: output.write(','.join(parts + [check_address_reverse(parts, google, key)]) + '\n')
				elif zips: output.write(','.join(parts + [check_address_zip(parts, google, key)]) + '\n')
				else: output.write(','.join(parts + [check_address(parts, google, key)]) + '\n')
	output.close()	

if __name__ == '__main__':
	
	import argparse

	#command line parser
	parser = argparse.ArgumentParser(description = 'Checks an OpenAddresses formatted file against a web API')
	parser.add_argument('input', help = 'OpenAddresses file with backfilled zip to check')
	parser.add_argument('output', help = 'file to output accuracy data')
	parser.add_argument('key', help = 'a file containing a valid api key')
	parser.add_argument('-r', '--reverse', help = 'use a reverse geocode search', action = 'store_true')
	parser.add_argument('-z', '--zip', help = 'search with zip code', action = 'store_true')
	parser.add_argument('-m', '--mapbox', help = 'geocode from the mapbox API', action = 'store_true')
	args = parser.parse_args()

	write_test(args.input, args.output, args.key, args.reverse, args.zip, args.mapbox)