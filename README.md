# Web App for Global Warming evolution in the last millenium

This web app was made using data from the [Last Millenium Ensemble Project](https://www.cesm.ucar.edu/community-projects/lme) from the Community Earth System Model (CESM).

# General Steps for the project 

* Since original data was in netcdf format, preprocessing was necessary to extract mean temperature in each country across more than 1000 years. This was performed using python libraries such as netCDF4, regionmask, xarray, geopandas and pandas. The result was a dataframe with the mean temperature for each country in each year.
* The Web App was built using dash, dash_bootstrap, along with plotly for responsive visualizations. The Web App allows user to visualize the changes in mean temperature for more than 100 countries across 1000 years, and also compare a previous year scenario to a new year scenario, observing temperature differences for each country, along with other interesting data for each chosen year.

For any question: christian.alvarez813@gmail.com


-----------------------------------------
**Google Cloud Deployment**
gcloud builds submit --tag gcr.io/globalwarming-392019/GlobalWarming  --project=globalwarming-392019

gcloud run deploy --image gcr.io/globalwarming-392019/GlobalWarming --platform managed  --project=globalwarming-392019 --allow-unauthenticated
