import pandas as pd
import numpy as np
import pickle

from datetime import timedelta
from datetime import datetime
from scipy import stats
from Util.GetSatelliteData import getSatelliteData
import streamlit as st

# Function to get the satellite data need for making a coral vs algae prediction
def getPredictionInterval(lat, lon, dates, model, ci=.8):
	spec_idxs = ['AWEInsh', 'AWEIsh', 'LSWI', 'MBWI', 'MLSWI26', 'MLSWI27','MNDWI', 'MuWIR', 'NDVIMNDWI', 'NDWI', 'NDWIns', 'NWI', 'SWM', 'WI1', 'WI2', 'WRI']
	bands_landsat = ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7', 'QA_PIXEL']
	bands_modis = ['sur_refl_b08', 'sur_refl_b09', 'sur_refl_b10', 'sur_refl_b11', 'sur_refl_b12', 'sur_refl_b13', 'sur_refl_b14', 'sur_refl_b15', 'sur_refl_b16']

	# Get Satellite Data	
	df_landsat = dates.apply(getSatelliteData, args = ('LANDSAT', lat, lon, bands_landsat, spec_idxs, 100), axis = 1)
	df_landsat.rename({'SR_B2' : 'Blue',
                        'SR_B3' : 'Green',
                        'SR_B4' : 'Red',
                        'SR_B5' : 'Near Infrared',
                        'SR_B6' : 'Shortwave Infrared 1',
                        'SR_B7' : 'Shortwave Infrared 2'}, axis = 1, inplace = True)
	df_modis = dates.apply(getSatelliteData, args = ('MODIS', lat, lon, bands_modis, None, 1000), axis=1)

	# Merge Dataframes
	data =  pd.merge(df_landsat, df_modis, left_on = ['lat', 'long', 'date'], right_on = ['lat', 'long', 'date'])

	# Features for predicting coral vs algae
	features = ['Blue', 'Green', 'Red',
		'Near Infrared', 'Shortwave Infrared 1', 'Shortwave Infrared 2',
		'QA_PIXEL', 'sur_refl_b08', 'sur_refl_b09', 'sur_refl_b10',
		'sur_refl_b11', 'sur_refl_b12', 'sur_refl_b13', 'sur_refl_b14',
		'sur_refl_b15', 'sur_refl_b16', 'AWEInsh', 'AWEIsh', 'LSWI', 'MBWI', 'MLSWI26', 'MLSWI27',
            'MNDWI', 'MuWIR', 'NDVIMNDWI', 'NDWI', 'NDWIns', 'NWI', 'SWM', 'WI1', 'WI2', 'WRI']
	
	X = data[features]
	preds = model.predict_proba(X)[:, 0]
	zipped = list(zip(preds, data['date']))
	if lat > 0:
		summer_start = datetime.strptime('2021-06-21', '%Y-%m-%d')
		summer_end = summer_start + timedelta(days=91)
	elif lat <0:
		summer_start = datetime.strptime('2021-12-01', '%Y-%m-%d')
		summer_end = summer_start + timedelta(days=91)
	weights = []
	for z in zipped:
		if z[1] > summer_start and z[1] < summer_end:
			weights.append(.5)
		else:
			weights.append(1)

	predicted_prob = np.average(preds, weights=weights)

	n = preds.shape[0]
	std = preds.std()
	interval = stats.t.interval(ci, n-1, loc=predicted_prob, scale=std)

	return predicted_prob, data