import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import ee
import geemap.foliumap as emap

from datetime import datetime as dt
from datetime import timedelta
from Util.MakePrediction import getPredictionInterval
from Util.GetSatelliteData import getModisBleachingFeatures

def resetSession():
	for key in st.session_state.keys():
		del st.session_state[key]
	st.legacy_caching.caching.clear_cache()

#Caching prediction results
@st.cache
def getPrediction(longitude, latitude):
	# Get Prediction   
	dates = ['05/01/2021', '07/01/2021', '09/01/2021', '11/01/2021', '01/01/2022']
	dates_df = pd.DataFrame(columns=['date'])
	for date in dates:
		temp = pd.DataFrame({'date': [pd.to_datetime(date)]})
		dates_df = pd.concat([dates_df, temp]) 

	predicted_prob, data = getPredictionInterval(lat=latitude, 
										   lon=longitude, 
										   dates=dates_df, 
										   model=xgb_model)
	return predicted_prob

st.set_page_config(page_title = "Evaluation",
				   page_icon = "🕒")
# Load Model
xgb_model = pickle.load(open(r"../Trained Models/coral_presence_xgb_model_CAR.pkl", "rb"))

# Title
st.markdown("<h1 style='text-align: center; color: white;'> Make A Prediction </h1>", unsafe_allow_html=True)

# Map Display
longitude = float(st.text_input('Longitude', -76.2, on_change = resetSession))
latitude = float(st.text_input('Latitude', 25.01, on_change = resetSession))
point = {'lon': longitude,
		'lat': latitude}

ee.Initialize()
map = emap.Map(basemap = 'ROADMAP',
			   center = [latitude, longitude],
			   plugin_Draw = False,
			   zoom = 8)
map.add_basemap('HYBRID')
map.add_marker((latitude, longitude))
map.to_streamlit(height = 600)

# Setup session
if "button_clicked" not in st.session_state:
	st.session_state.button_clicked = False
def callback():
	st.session_state.button_clicked = True

if (st.button("Predict", on_click = callback) or st.session_state.button_clicked):
	predicted_prob = getPrediction(longitude, latitude)

	if (predicted_prob > .5):
		st.header("Selected point is Coral 🦐")

		st.markdown("""---""")
		st.write('A bleaching analysis for the provided location will be modeled for the previous 90 days.')
		date = st.date_input(label='Date: ',
                value=(dt(month=10, day=1, year=2015)))

		if st.button('Evaluate'):
			predicted_prob, data = getPredictionInterval(lat=latitude, 
										 lon=longitude, 
										 dates=pd.DataFrame({'date': [pd.to_datetime(date)]}), 
										 model=xgb_model)
			df_bleaching_feats, df_90 = getModisBleachingFeatures(data)

			features = df_bleaching_feats[['sur_refl_b08', 'sur_refl_b09', 'sur_refl_b10', 'sur_refl_b11', 'sur_refl_b12', 'sur_refl_b13', 'sur_refl_b14', 'sur_refl_b15', 'sur_refl_b16', 
											'Blue', 'Green', 'Red', 'Near Infrared', 'Shortwave Infrared 1', 'Shortwave Infrared 2', 'QA_PIXEL', 
											'AWEInsh', 'AWEIsh', 'LSWI', 'MBWI', 'MLSWI26', 'MLSWI27', 'MNDWI', 'MuWIR', 'NDVIMNDWI', 'NDWI', 'NWI', 'SWM', 'WI1', 'WI2', 'WRI', 
											'sst_day_of_study', 'sst_max', 'sst_summer_max', 'sst_cv_max', 'sst_cv_cnt', 'sst_abv_summer', 'sst_abv_summer_cumulative', 'sst_cv_cnt_SumComp', 
											'sst_cv_max_SumComp', 'sst_dhw', 'sst_dhw_age', 'chlor_avg', 'chlor_change', 'nflh_avg', 'nflh_change', 'nflh_max', 'nflh_min', 
											'poc_avg', 'poc_change', 'poc_max', 'poc_min']]

			#st.write(features)
			bleaching_model = pickle.load(open(r"../Trained Models/bleaching_2bin_model_CAR.pkl", "rb"))
			result = bleaching_model.predict(features)

			if result == 0:
				st.header('Bleaching level: low ✅')
			else:
				st.header('Bleaching level: moderate/severe' + ' 💥')

			st.write('Cumulative Degrees Over Monthly Maximum Mean (MMM):',
					 round(float(df_bleaching_feats['sst_abv_summer_cumulative'].values),2))
			st.write('Maximum Degree Heating Weeks (DHW) in past three years:',round(float(df_bleaching_feats['sst_dhw'].values),2))
			st.write('Date of DHW Max:',timedelta(int(df_bleaching_feats['sst_dhw_age'])) + date)

			# SST vs SST_Summer Plot
			fig, ax = plt.subplots()
			line1, = ax.plot(pd.to_datetime(df_90['time'], unit='ms'), df_90['sst'], label = "SST")
			line2, = ax.plot(pd.to_datetime(df_90['time'], unit='ms'), df_90['sst_Summer'], label = 'MMM')
			ax.set_xlabel('Date')
			ax.set_ylabel('Temperature (C)')
			ax.legend(handles = [line1, line2])
			ax.set_title("Comparison of Sea Surface Temperature vs Expected Summer Maximum ")
			plt.xticks(rotation=45)
			st.pyplot(fig)

	else: 
		st.write("Selected point is Non-Coral")

