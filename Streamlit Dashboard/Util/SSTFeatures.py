import pandas as pd
import numpy as np

def cumlimit(x, lim):
    x[np.isnan(x)]=0
    total = 0.
    result = np.empty_like(x)
    for i, y in enumerate(x):
        total += y
        if total < lim:
            total = 0.
        result[i]=total
    return result

# This function takes the dataframe created from the MODIS values and creates the features for coefficient of variation (cv)
# maximum temperature and the comparison to summertime averages.
def extend_SST(df):
	SummerAvgSST = pd.read_csv(r"../Sample Data/SummerAvgSST.csv")

	df['sst'] = df['sst'].interpolate()
	dfExt=pd.merge(df, SummerAvgSST,how = 'left', left_on = ['lon_Rnd','lat_Rnd'], right_on = ['Lon','Lat'])
	dfExt['sst_SumComp'] = dfExt['sst'] - dfExt['sst_Summer']
	dfExt['sst_SumComp'] = dfExt['sst_SumComp'].fillna(0)
	dfExt['sst_sd'] = dfExt['sst'].rolling(14).std()
	dfExt['sst_mean'] = dfExt['sst'].rolling(14).mean()
	dfExt['sst_cv'] = dfExt['sst_sd'] * 100 / dfExt['sst_mean']

	dfExt['sst_streak'] = dfExt['sst_SumComp'].apply(np.floor)
	dfExt['sst_streak_min'] = dfExt['sst_streak'].rolling(7).min()
	dfExt.loc[dfExt['sst_streak_min'] < 1, 'sst_streak_min'] = -1
	dfExt['sst_streak_min'] = dfExt['sst_streak_min']/7
	dfExt['DHW'] = cumlimit(dfExt['sst_streak_min'].values,0)

	dfExt['sst_streak'] = dfExt['sst_SumComp'].apply(np.ceil)
	dfExt.loc[dfExt['sst_streak'] < 1,'sst_streak'] = -1
	dfExt['sst_streak'] = dfExt['sst_streak']/7
	dfExt['DHW'] = cumlimit(dfExt['sst_streak_min'].values,0)

	return dfExt