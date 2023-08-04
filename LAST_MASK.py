# %% New with regionmask
#IMPORTS
import regionmask
import numpy as np
import xarray as xr
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gp

#%% Read shapefile and make mask    NEW
#shape = gp.read_file('ne_50m_admin_0_countries.shp')
shape = gp.read_file('World_Countries.shp')

# %% LOAD NETCDF
data = nc.Dataset("TS_TOTAL.nc")
TS = data['TS']
lon = data['lon']
lat = data['lat']

# %%
# Reducing to yearly data
def yearmean(TT):
    TM = np.zeros((len(TT[0]),len(TT[0,1])))
    for i in range(0,12):
        TM = TM + TT[i]
        if i == 11: 
            TM = TM/12
            return TM         
list1 = []
for i in range(0,len(TS)-11,12):
        T = yearmean(TS[i:i+12])
        list1.append(T)
        
TS_y = np.array(list1) 
#%% NEW
shape['id'] = np.arange(0,len(shape))
gdf_mask_poly = regionmask.Regions(name = 'COUNTRY', numbers = shape.id, names = shape.COUNTRY[shape.id], outlines = list(shape.geometry.values[i] for i in range(0,len(shape))))

mask = gdf_mask_poly.mask(data, lat_name='lat', lon_name='lon')
shape.rename(columns = {'COUNTRY':'names'},inplace = True)


#%%
# defining masking function (mask,var,mask key)          NEW
def masking(y,x,key):
    m = np.ma.masked_where(y!=key, y)                  # filter out values larger than 5
    return np.ma.masked_where(np.ma.getmask(m), x) # applies the mask of m on x

def yearly_national_mean(df,TS):
    mean_list = []
    for i in range(0,len(df.index)):
        key = df['id'][i]
        TS_masked = masking(mask.to_numpy(),TS,key)
        mean_list.append([df['names'][i],TS_masked.mean()-273.15])
    mean_list = pd.DataFrame(mean_list)
    return mean_list.where(mean_list[1] != 0.0000000000).dropna()

#%% APPLYING NEW FUNCTION TO MILLENIUM     NEW
years = list(range(850,2007))
for i in range(0,len(TS_y)):
     if i == 0: 
        df_hist = yearly_national_mean(shape,TS_y[i,:,:])
        df_hist.rename({0:'Countries', 1 : str(years[i])},axis = 'columns',inplace=True)
     else: 
        df_hist_i = yearly_national_mean(shape,TS_y[i,:,:])
        df_hist[str(years[i])] = df_hist_i[1]

#%%
#Append world
world = pd.DataFrame(['World'])
world.rename({0:'Countries'}, axis = 'columns', inplace = True)
for i in range(0,len(TS_y)):
        world[str(years[i])] = TS_y[i,:,:].mean()-273.15

df_total = pd.concat([df_hist,world])    

#%% CORRECT GREENLAND NAME, DROP FRENCH GUIANA 
df_total['Countries']= df_total['Countries'].replace('Greenland (Denmark)','Greenland')
df_total = df_total.set_index('Countries')
df_total = df_total.drop('French Guiana (France)')
#%%  EXPORT
df_total.reset_index()
df_total.to_csv('df_total_new_countries.csv')


