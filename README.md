# Zip_Backfill

**Description**: `Zip_Backfill.py` takes an OpenAddresses files and, for rows that do not have zip codes, compares the row's lat and lon to a shape file of zip codes in order to assign it a zip code. The code is designed to work with a Census ZCTA `.shp` file.

All other files are to test the efficacy of `Zip_Backfill.py`.

## Usage

- To install dependencies run `pip install -r requirements.txt`

- Download the 2015 TIGER ZCTA `zip` [here](https://www.census.gov/geo/maps-data/data/tiger-line.html)

- Retrieve the [OpenAddresses US regional zip files](http://results.openaddresses.io/)

- **To Backfill**

	- Pick an OpenAddresses file from one of their regional US zip files to backfill with zip codes

	- Run `python Backfill_Zip.py <CLI Options>`

- **To Run Tests**

	- Make a file of unedited OpenAddresses rows to test with either all or no zip codes

		- To do this run `python pull_test_rows.py <CLI Options>` to pull rows without zip codes(for a check against Google or Mapbox) 

		- OR run `python pull_test_rows.py <CLI Options> -z` to pull rows with zip codes(for a check against zip codes already in OpenAddresses)

	- Run `python test.py <CLI Options>`

## CLI Options

- **`Backfill_Zip.py`**

	- **input** OpenAddresses file to backfill from
	- **output** file to to backfill to
	- **shape_file** a census ZCTA shape file

- **`pull_test_rows`**

	- **input** A file containing some number of state OpenAddresses files
	- **output** The file to store found rows
	- **-z, --zips** Pull only rows WITH zip codes instead of rows without zip codes

- **`test.py`**

	- **input** OpenAddresses file to take rows from
	- **shape_file** a census ZCTA shape file
	- **number** the number of rows to test
	- **-g, --google** use google geocode search, argument: (output file)
	- **-r, --reverse** use a reverse google geocode search, argument: (output file)
	- **-z, --zip** search google with zip code, argument: (output file)
	- **-m, --mapbox** reverse geocode from the mapbox API, argument: (output file)
	- **-o, --openaddresses** check against zips in openaddresses, argument: (output file)
	- **-gk, --google_key** a file with a google API key, needed if running any check against google
	- **-mk, --mapbox_key** a file with a mapbox API key, needed if running a check against mapbox


## Accuracy

Rows randomly pulled from all files and using the Census Tiger ZCTA .shp file:

- 19,729/23,000 = 86%: backfilled

- 1,608/1,750 = 92%: agree with Google api

- 8,587/8,593 = 99% agree with Mapbox api

- 8,236/8,581 = 96% agree with OpenAddresses



