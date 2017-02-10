import pandas as pd

def getFIPS(filter = {}):
	fips = pd.read_csv('state_county_fips.txt', dtype = 'object')
	if filter:
		if 'state_fips' in filter:
			fips = fips.loc[fips['state_fips'].isin(set(filter['state_fips'])),]
		if 'state_abbreviation' in filter:
			fips = fips.loc[fips['state_abbreviation'].isin(filter['state_abbreviation']),]
		if 'county_fips' in filter:
			fips = fips.loc[fips['county_fips'].isin(filter['county_fips']),]
		if 'county_name' in filter:
			fips = fips.loc[fips['county_name'].isin(filter['county_name']),]
			
	return fips
