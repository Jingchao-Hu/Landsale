#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
from tqdm import tqdm

df_raster = pd.read_stata("C:/Users/macbook/Desktop/RA/cityshape/resultdata/matchedcountraster.dta")
df_citycenter = pd.read_stata("C:/Users/macbook/Desktop/RA/cityshape/originaldata/citydb.dta")
df_landsale = pd.read_stata("C:/Users/macbook/Desktop/RA/cityshape/originaldata/DR5_land_coord_1_5m.dta")

df_landsale = df_landsale.drop_duplicates(subset=["land_lat", "land_lon"])
df_raster.rename(columns={"population": "popcount", "_ID": "id"}, inplace=True)
df_citycenter.rename(columns={"市代码": "city_code"}, inplace=True)

df_landsale = df_landsale.merge(df_citycenter, on="city_code")

n = len(df_landsale)


unique_ids = df_landsale['id'].unique()

# Group by 'id' and count the number of rows for each id
id_counts = df_raster.groupby('id').size().reset_index(name='count')

# Sort the result in descending order based on the count
id_counts_sorted = id_counts.sort_values('count', ascending=False)

# Get the sorted list of unique 'id' values
sorted_ids = id_counts_sorted['id'].tolist()

for id_val in tqdm(sorted_ids, desc="Processing IDs"):
    df_landsale_filtered = df_landsale[df_landsale['id'] == id_val]
    df_raster_filtered = df_raster[df_raster['id'] == id_val]

    # Compute batch_size
    raster_count = len(df_raster_filtered)
    batch_size = 21000000 // raster_count

    n_filtered = len(df_landsale_filtered)
    total_batch_num = -(-n_filtered // batch_size)  # Ceiling division
    # Get the city name from the df_citycenter DataFrame
    city_name = df_citycenter[df_citycenter['id'] == id_val]['市'].values[0]

    # Print the city name
    print(f"Processing city: {city_name}")


    for i in range(1, total_batch_num + 1):
        start = (i - 1) * batch_size
        end = min(i * batch_size, n_filtered)
        batch = df_landsale_filtered.iloc[start:end]
        merge = df_raster_filtered.merge(batch, on="id")
        print(f"Shape of merge DataFrame for id {id_val} and batch {i}: {merge.shape}")


        df_quadrant1 = merge.loc[(merge.x > merge.land_lon) & (merge.y > merge.land_lat)]
        df_quadrant1_pop = df_quadrant1.groupby(["land_lon", "land_lat"]).popcount.sum().reset_index().rename(columns={"popcount": "quadrant1_pop"})

        df_quadrant2 = merge.loc[(merge.x < merge.land_lon) & (merge.y > merge.land_lat)]
        df_quadrant2_pop = df_quadrant2.groupby(["land_lon", "land_lat"]).popcount.sum().reset_index().rename(columns={"popcount": "quadrant2_pop"})

        df_quadrant3 = merge.loc[(merge.x < merge.land_lon) & (merge.y < merge.land_lat)]
        df_quadrant3_pop = df_quadrant3.groupby(["land_lon", "land_lat"]).popcount.sum().reset_index().rename(columns={"popcount": "quadrant3_pop"})

        df_quadrant4 = merge.loc[(merge.x > merge.land_lon) & (merge.y < merge.land_lat)]
        df_quadrant4_pop = df_quadrant4.groupby(["land_lon", "land_lat"]).popcount.sum().reset_index().rename(columns={"popcount": "quadrant4_pop"})

        df_fourquadrant = df_quadrant1_pop.merge(df_quadrant2_pop, on=["land_lon", "land_lat"], how="outer")             .merge(df_quadrant3_pop, on=["land_lon", "land_lat"], how="outer")             .merge(df_quadrant4_pop, on=["land_lon", "land_lat"], how="outer")

        df_fourquadrant.to_stata(f"C:/Users/macbook/Desktop/RA/cityshape/resultdata/output/land_result_{id_val}_{i}.dta", write_index=False)
        
data_dir = "C:/Users/macbook/Desktop/RA/cityshape/resultdata/output"
data_files = os.listdir(data_dir)

df_list = []
for f in data_files:
    if f.endswith(".dta"):
        df = pd.read_stata(os.path.join(data_dir, f))
        df_list.append(df)

result = pd.concat(df_list, ignore_index=True)  
result.to_stata("C:/Users/macbook/Desktop/RA/cityshape/resultdata/output_all.dta")


# In[ ]:




