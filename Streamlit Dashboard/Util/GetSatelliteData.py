import ee
import eemont
import pandas as pd
import numpy as np
import streamlit as st

from ee import EEException
from datetime import datetime
from Util.SSTFeatures import extend_SST

def custom_Rounding(value):
    if(0 <= value % 1 < .5):
        return round(value) + .5
    elif(.5 <= value % 1 < 1):
        return round(value) - .5
    else:
        return round(value)

def getModisBleachingFeatures(row):
	try:
		end_date = ee.Date(row.iloc[0]['date'])
		img_col = ee.ImageCollection("NASA/OCEANDATA/MODIS-Aqua/L3SMI")\
					.select(['chlor_a', 'nflh','poc', 'sst'])\
					.filterBounds(geometry=ee.Geometry.Point(row.iloc[0]['long'], row.iloc[0]['lat']))\
					.filterDate(end_date.advance(-1080, 'day'), end_date)\
					.getRegion(geometry=ee.Geometry.Point(row.iloc[0]['long'], row.iloc[0]['lat']), scale=1000)\
					.getInfo()
		
		#convert output from GEE to pandas dataframe
		df = pd.DataFrame(img_col[1:], columns=img_col[0])
		
		df['lat_Rnd'] = custom_Rounding(row.iloc[0]['lat'])
		df['lon_Rnd'] = custom_Rounding(row.iloc[0]['long'])
		
		#Calculate statistics from 90 day history
		df = extend_SST(df)
		df_90_Limit = df.tail(90)
		
		#If output came out empty, save nans
		if df.shape[0]==0:
			row['chlor_max'] = np.nan
			row['chlor_min'] = np.nan
			row['chlor_avg'] = np.nan
			row['chlor_change'] = np.nan
			row['nflh_max'] = np.nan
			row['nflh_min'] = np.nan
			row['nflh_avg'] = np.nan
			row['nflh_change'] = np.nan
			row['poc_max'] = np.nan
			row['poc_min'] = np.nan
			row['poc_avg'] = np.nan
			row['poc_change'] = np.nan

			row['sst_day_of_study'] = np.nan
			row['sst_max'] = np.nan
			row['sst_summer_max'] = np.nan
			row['sst_cv_max'] = np.nan
			row['sst_cv_cnt'] = np.nan
			row['sst_abv_summer'] = np.nan
			row['sst_abv_summer_cumulative'] = np.nan
			row['sst_cv_cnt_SumComp'] = np.nan
			row['sst_cv_max_SumComp'] = np.nan
			row['sst_dhw'] = np.nan
			row['sst_dhw_age'] = np.nan
			
		#If output has one or more rows, compress the values to specific features
		elif df.shape[0] >= 1:
			row['chlor_max'] = np.max(df_90_Limit['chlor_a'])
			row['chlor_min'] = np.min(df_90_Limit['chlor_a'])
			row['chlor_avg'] = np.mean(df_90_Limit['chlor_a'])
			row['chlor_change'] = float(df_90_Limit['chlor_a'][-1:]) - float(df_90_Limit['chlor_a'][:1])
			row['nflh_max'] = np.max(df_90_Limit['nflh'])
			row['nflh_min'] = np.min(df_90_Limit['nflh'])
			row['nflh_avg'] = np.mean(df_90_Limit['nflh'])
			row['nflh_change'] = float(df_90_Limit['nflh'][-1:]) - float(df_90_Limit['nflh'][:1])
			row['poc_max'] = np.max(df_90_Limit['poc'])
			row['poc_min'] = np.min(df_90_Limit['poc'])
			row['poc_avg'] = np.mean(df_90_Limit['poc'])
			row['poc_change'] = float(df_90_Limit['poc'][-1:]) - float(df_90_Limit['poc'][:1])

			row['sst_day_of_study'] = df['sst'].tail(1).values[0]
			row['sst_max'] = df_90_Limit['sst'].max()
			row['sst_summer_max'] = df_90_Limit['sst_SumComp'].max()
			row['sst_cv_max'] = df_90_Limit['sst_cv'].max()
			row['sst_cv_cnt'] = df_90_Limit['sst_cv'].loc[df_90_Limit['sst_cv'] >= 1.9].count()
			row['sst_abv_summer'] = df_90_Limit['sst_SumComp'].loc[(df_90_Limit['sst_SumComp'] > 1)].count()
			row['sst_abv_summer_cumulative'] = df_90_Limit['sst_SumComp'].loc[(df_90_Limit['sst_SumComp'] > 1)].sum()
			row['sst_cv_cnt_SumComp'] = df_90_Limit['sst_cv'].loc[(df_90_Limit['sst_SumComp'] > 0) & 
										(df_90_Limit['sst'] > df_90_Limit['sst_mean'])].count()
			row['sst_cv_max_SumComp'] = df_90_Limit['sst_cv'].loc[(df_90_Limit['sst_SumComp'] > 0) & 
										(df_90_Limit['sst'] > df_90_Limit['sst_mean'])].max()
			row['sst_dhw'] = df['DHW'].max()
			row['sst_dhw_age'] = df.loc[df['DHW'] == df['DHW'].max()].index.values.astype(int)[0] - len(df)
		return row, df_90_Limit
	except EEException as e:
		st.write(e)
		row['chlor_max'] = np.nan
		row['chlor_min'] = np.nan
		row['chlor_avg'] = np.nan
		row['chlor_change'] = np.nan
		row['nflh_max'] = np.nan
		row['nflh_min'] = np.nan
		row['nflh_avg'] = np.nan
		row['nflh_change'] = np.nan
		row['poc_max'] = np.nan
		row['poc_min'] = np.nan
		row['poc_avg'] = np.nan
		row['poc_change'] = np.nan

		row['sst_day_of_study'] = np.nan
		row['sst_max'] = np.nan
		row['sst_summer_max'] = np.nan
		row['sst_cv_max'] = np.nan
		row['sst_cv_cnt'] = np.nan
		row['sst_abv_summer'] = np.nan
		row['sst_abv_summer_cumulative'] = np.nan
		row['sst_cv_cnt_SumComp'] = np.nan
		row['sst_cv_max_SumComp'] = np.nan
		row['sst_dhw'] = np.nan
		row['sst_dhw_age'] = np.nan
		return row, ""

# Function to return an empty row for given location
def noBandsFound(satellite, bands, spec_idxs, lat, lon):
	new_row = pd.DataFrame()
	new_row = new_row.reindex(columns=['lat', 'long', *bands], fill_value=np.nan)
	if(satellite == 'LANDSAT'):
		new_row = new_row.reindex(columns=[*new_row.columns.tolist(), *spec_idxs], fill_value=np.nan)
	new_row['datetime_' + satellite] = np.nan
	new_row['lat'] = lat
	new_row['long'] = lon
	return new_row.T.squeeze()

def getSatelliteData(row, satellite, lat, lon, bands, spec_idxs, scale):
	try:
		start_date = ee.Date(row['date'])
		if (satellite == 'MODIS'):
			img_col = ee.ImageCollection('MODIS/006/MYDOCGA')\
						.select(bands)
			end_date = ee.Date(start_date).advance(2, 'day')
		elif (satellite == 'LANDSAT'):
			img_col = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')\
						.select(bands)\
						.spectralIndices(spec_idxs)
			end_date = ee.Date(start_date).advance(1, 'month')

		data = img_col\
					.filterBounds(geometry=ee.Geometry.Point(lon, lat))\
					.filterDate(start_date, end_date)\
					.getRegion(geometry=ee.Geometry.Point(lon, lat), scale=scale)\
					.getInfo()
					
		df = pd.DataFrame(data[1:], columns=data[0])
		df.dropna(inplace=True)
		df['datetime_' + satellite] = df.time.apply(lambda x: datetime.utcfromtimestamp(x/1000))
		df['date'] = row['date']
		df['long'] = lon
		df['lat'] = lat
		row = row.to_frame().T

		if df.shape[0] > 1:
				# Loop through data return from Google Earth Engine query and find data point closest to the coral date. 
				# Select only the earliest Satellite data point
				time_deltas = {}
				for i in range(df.shape[0]):
					time_deltas[i] = np.abs(pd.to_datetime(df['datetime_' + satellite].values[i]) - pd.to_datetime(row.iloc[0]['date']))
				ind = min(time_deltas, key=time_deltas.get)

				data = df.iloc[ind,].to_frame().T
				return data.drop(columns=['id', 'time', 'longitude', 'latitude']).squeeze()

		# We only have one Landsat data point for the selected time interval and region
		elif df.shape[0]==1:
			data = df.iloc[0,].to_frame().T
			return data.drop(columns=['id', 'time', 'longitude', 'latitude']).squeeze()

		# No data was found for given location and date range
		elif df.shape[0]==0:
			return noBandsFound(satellite, bands, spec_idxs, lat, lon)

	# Error occured when retrieving data
	except EEException as e:
		st.write(e)
		return noBandsFound(satellite, bands, spec_idxs, lat, lon)