import requests
import argparse

#command line parser
parser = argparse.ArgumentParser(description = 'Backfills zip code to single file')
parser.add_argument('input', help = 'OpenAddresses file with backfilled zip to check')
parser.add_argument('key', help = 'a file containing a valid google api key')
args = parser.parse_args()

key = open(args.key, 'r').read()

url_pre = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
url_post = '&key=' + key

good = 0
fail = 0
not_found = 0

with open(args.input, 'r') as source:
	for row in source:
		parts = row.split(',')
		check = requests.get(url_pre + parts[1] + ',' + parts[0] + url_post)
		result = check.json()
		if result['status'] == 'OK':
			for piece in result['results'][0]['address_components']:
				if piece['types'][0] == 'postal_code':
					if piece['long_name'] == parts[7]:
						print 'pass'
						good += 1
					else:
						print 'fail'
						fail += 1
					break
			else:
				print 'not_found'
				not_found += 1
		else:
			print 'not found'
			not_found += 1

print 'pass: ' + str(good)
print 'fail: ' + str(fail)
print 'not_found: ' + str(not_found)