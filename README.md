# Universal Remote Observation of Coral Health (UROCH): Studying the Efficacy of Extending Existing NASA Instruments to Detect and Monitor Coral Reefs 

<p align="center">
  <img alt="Light" src="https://github.com/patgeitner/nasa-coral-health-observation/blob/main/Images/rochester-logo.png" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Light" src="https://github.com/patgeitner/nasa-coral-health-observation/blob/main/Images/NASA_logo.svg.webp" width="30%">
</p>

### Sponsor: NASA
### Co-authors: 
Lisa Pink, Matthew Johnson, Mohamad Ali Kalassina, Patrick Geitner, Thomas Durkin

## Abstract
Coral reefs, one of the most biodiverse ecosystems on the planet, are facing the threat of extinction. This is projected to cause severe environmental damage, especially on the fronts of climate change and marine life. Although multiple efforts are being made to evaluate coral reef health and revitalize those witnessing severe bleaching, these efforts remain expensive and unsustainable. In this project, we study the capability of using satellite data from NASA’s Landsat-8 and MODIS-Aqua to detect coral reef presence and evaluate coral bleaching severity. We adopt a multi-faceted approach by merging data from Allen Coral Atlas and Global Coral Bleaching Dataset with satellite data in the Caribbean and Great Barrier Reef regions. Using a gradient-boosted tree-based classification model, we achieve 96.5\% accuracy in identifying coral/algae, implement a temporal voting-based classifier to distinguish coral from algae, and achieve 96.94\% weighted precision in evaluating bleaching severity in the Great Barrier Reef. Using this machine learning pipeline and the dashboard developed from it, coral reef experts can identify regions where the reefs are at risk and act to revitalize them, all while viewing metrics showing trends in sea surface temperature in those areas. 


## Installation/Setup
A Google Earth Engine account is needed in order to access the satellite data. Proceed to https://earthengine.google.com to create an account.

## Data Collection
The following notebooks are used to process and merge the coral datasets and add the satellite data:

1). After downloading the benthic map data from a given region, the **SetupAllenCoralData** is used to process the data into a format that can easily be merged with the satellite data. The notebook returns a subset from the given Allen Coral Data with an even number of Coral/Algae and non-Coral/Algae observations.

2). With the coral data sampled and processed into a pickle files, we can then add the necessary satellite data using Google Earth Engine. The **CollectSatelliteData** notebook reads in the resulting pickle file and adds surface reflectance features from the Modis-Aqua satellite and surface reflectance values and spectral indices from the Landsat-8 satellite. The resulting dataset is a spatially and temporally fused combination of the satellite features and coral labels that can be used to train our modeling approaches.

## Feature Engineering
The feature engineering folder contains an exploratory analysis of adding different features related to sea surface temperatures, particulate organic carbon, and chlorophyll A concentration to potentially add to our coral bleaching models.

1). The **Sea Surface Temperature Feature Extraction** notebook explores extracting features related to sea surface temperatures, a factor known to contribute to coral bleaching 

2). The **chlorophyllA_feature_analysis** notebook explores the correlation between various features relating to cholorphyll A concentration and particulate organic carbon with the percentage of bleaching that a coral colony has experienced.

## Modeling
With the datasets generated and features added, we can train machine learning models to predict coral presence and assess coral health.

1). The **CoralPresenceModeling** notebook walks through the training and evaluation of a gradient-boosted tree-based (XGBoost) model for predicting coral/algae presence at a given location using satellite data.

2). The **AlgaeIdentification** notebook walks through our temporal, voting-based method to determine if a given point contains coral or algae.

3). The **CoralBleachingModeling** notebook walks through the training and evaluation of models to predict the percentage bleaching a given coral has experienced. We explore regression, ranking, and classification methods.

## Sample Data
This folder contains small samples of the final coral/algae presence and coral bleaching datasets that we used to train our machine learning models. Full datasets could not be uploaded as they were too large.

## Streamlit Dashboard for the Northern Caribbean
This is a dashboard that can be used to make real time predictions for a single location on both coral presence and coral bleaching. It utilizes our coral presence models to determine whether the location is coral or not. If the prediction is coral, our bleaching model will be used to output a level of risk to the coral's health as well as a bleaching analysis. The user may use the date input to see the change in sea surface temperature over a 90 day period.

![](https://github.com/patgeitner/nasa-coral-health-observation/blob/main/Images/Dashboard.png)

### Troubleshooting:
*Try using these package versions*
- streamlit version 1.11.0
- xgboost version 1.3.2
- sklearn version 1.1.2
### Usage: streamlit run 1_Home.py

