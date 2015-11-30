# Zip_Backfill

Both of these scripts run from the command line and take as input two files: input and output. Input is a .csv file with addresses that need to be backfilled. This file should be in the format: Lon Lat, Number, Street, City, District, Region, Zip, ID. Output is a .csv file that the backfilled addresses will be written into. Addresses rows will be returned in the same format as Input.

## Difference Between Files

The difference between the two scripts lies in how they search census block polygons. Zip_Backfill.py looks through the loaded shape files to see if they contain a point from beginning to end ('for poly in zips.geom'). Zip_Backfill_Fast.py takes advantage of the fact that geographically close zip codes are numerically close and that geographically close address points are together within files. As such, it first tries the last zip code that was found and then zip codes progressively farther from it until it finds a match.

## Performance

###Speed(macbook air)

Benton Indiana, 10229 rows:

- Zip_Backfill.py ~ 1 Hour 15 Minutes
- Zip_Backfill_Fast.py ~ 30 Seconds

###Accuracy

Running the current test of 36 rows, three rows per state for three states in each of the four OpenAddresses areas, and using Census Tiger Line ZCTA shape file:

- 30/36 are found and backfilled with zip codes
- 27/30 of the backfilled zip codes agree with what the Google api returns as the zip code


