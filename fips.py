import pandas as pd

def getFIPS(fips_filter = {}):
	"""
		start at widest filter and move down
	"""
	fips = pd.read_csv('state_county_fips.txt', dtype = 'object')
	if fips_filter:
		if 'state_fips' in fips_filter and len(fips_filter['state_fips']) > 0:
			fips = fips.loc[fips['state_fips'].isin(set(fips_filter['state_fips'])),]
		if 'state_abbreviation' in fips_filter and len(fips_filter['state_abbreviation']) > 0:
			fips = fips.loc[fips['state_abbreviation'].isin(fips_filter['state_abbreviation']),]
		if 'county_fips' in fips_filter and len(fips_filter['county_fips']) > 0:
			fips = fips.loc[fips['county_fips'].isin(fips_filter['county_fips']),]
		if 'county_name' in fips_filter and len(fips_filter['county_name']) > 0:
			fips = fips.loc[fips['county_name'].isin(fips_filter['county_name']),]

	return fips
