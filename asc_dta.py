#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import gdal
import numpy as np
asc_file = 'C:/Users/macbook/Desktop/RA/cityshape/originaldata/pop_count/gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev11_2010_30_sec_1.asc'
ds = gdal.Open(asc_file)
band = ds.GetRasterBand(1)
data = band.ReadAsArray().astype(np.float32)


#get information of raster
transform = ds.GetGeoTransform()
x_origin = transform[0]
y_origin = transform[3]
pixel_width = transform[1]
pixel_height = transform[5]

#get longitude,latitude,population information of each point
df = pd.DataFrame(data=data.flatten(), columns=['population'])
df['row'] = np.repeat(np.arange(data.shape[0]), data.shape[1])
df['col'] = np.tile(np.arange(data.shape[1]), data.shape[0])
df['y'] = y_origin + df['row'] * pixel_height
df['x'] = x_origin + df['col'] * pixel_width
df['longitude'] = df['x']
df['latitude'] = df['y']
df = df[['latitude', 'longitude', 'population']]

dta_file = 'C:/Users/macbook/Desktop/RA/cityshape/resultdata/pop_count1.dta'
df.to_stata(dta_file, write_index=False)

