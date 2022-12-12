
![](https://github.com/patgeitner/nasa-coral-health-observation/blob/main/Images/rochester-logo.png)
# Universal Remote Observation of Coral Health (UROCH): Studying the Efficacy of Extending Existing NASA Instruments to Detect and Monitor Coral Reefs 

## Sponsor: NASA
## Co-authors: 
Lisa Pink, Matthew Johnson, Mohamad Ali Kalassina, Patrick Geitner, Thomas Durkin

## Abstract

Coral reefs, one of the most biodiverse ecosystems on the planet, are facing the threat of extinction. This is projected to cause severe environmental damage, especially on the fronts of climate change and marine life. Although multiple efforts are being made to evaluate coral reef health and revitalize those witnessing severe bleaching, these efforts remain expensive and unsustainable. In this project, we study the capability of using satellite data from NASA’s Landsat-8 and MODIS-Aqua to detect coral reef presence and evaluate coral bleaching severity. We adopt a multi-faceted approach by merging data from Allen Coral Atlas and Global Coral Bleaching Dataset with satellite data in the Caribbean and Great Barrier Reef regions. Using a gradient-boosted tree-based classification model, we achieve 96.5\% accuracy in identifying coral/algae, implement a temporal voting-based classifier to distinguish coral from algae, and achieve 96.94\% weighted precision in evaluating bleaching severity in the Great Barrier Reef. Using this machine learning pipeline and the dashboard developed from it, coral reef experts can identify regions where the reefs are at risk and act to revitalize them, all while viewing metrics showing trends in sea surface temperature in those areas. 


## Installation/Setup
A Google Earth Engine account is needed in order to access the satellite data. Proceed to https://earthengine.google.com to create an account.

## Data Collection
To collect the satellite data needed to build the models for coral presence, data from Allen Coral Atlas' bethic map is needed. See the **SetupAllenCoralData** Jupyter Notebook to create the coral dataset. To collect the satellite data need to build the bleaching model, data from the Global Coral Bleaching Database is used. Now that the two essential coral files are setup, utilizing the **CollectSatelliteData** Jupyter Notebook will collect data for each of the satellites and merge them together.


## Modeling
1). Coral Presence


2). Bleaching

## Streamlit Dashboard for the Northern Caribbean
A dashboard that can be used to make real time predictions for a single location. Utilizes our coral presence models to determine whether the location is coral or not. If the prediction is coral, our bleaching model will be used to output a level of risk to the coral's health as well as a bleaching analysis. The user may use the date input to see the change in sea surface temperature over a 90 day period.

![](https://github.com/patgeitner/nasa-coral-health-observation/blob/main/Images/Dashboard.png)

### Troubleshooting:
*Try using these package versions*
- streamlit version 1.11.0
- xgboost version 1.3.2
- sklearn version 1.1.2
### Usage: streamlit run 1_Home.py

