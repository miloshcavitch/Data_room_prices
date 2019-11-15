import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import Polygon
from shapely.geometry import Point

df = pd.read_csv('map_data.csv', index_col=0)
hoods = gpd.read_file('nyc-neighborhoods.geo.json')
df['price'] = df['price'].str.replace('[^0-9]', '').astype(int)

fig = plt.figure()
ax = fig.gca()

zipper = zip(df['price'], df['longitude'], df['latitude'])

rooms_hood = []
for p, lon, lat in zipper:
    position = Point(lon, lat)
    found_room = False
    for i, geo in enumerate(hoods['geometry']):
        if geo.contains(position) and found_room == False:
            rooms_hood.append(hoods['id'].iloc[i])
            found_room = True
    if found_room == False:
        rooms_hood.append('None')

df['neighborhood'] = rooms_hood

df.to_csv('map_data.csv')
