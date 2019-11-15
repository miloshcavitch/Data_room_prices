import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from descartes import PolygonPatch
from color_func import autoRGB, valueLERP
fig = plt.figure()
ax = fig.gca()
hoods = gpd.read_file('nyc-neighborhoods.geo.json')
df = pd.read_csv('map_data.csv')
zipper = zip(hoods['id'], hoods['geometry'])
for id, geo in zipper:
    geodf = df[ df['neighborhood'] == id]
    color = ''
    if geodf.shape[0] > 5:
        median_price = geodf['price'].median()
        if median_price != np.nan:
            #print(id, median_price)
            lerped = valueLERP(median_price, 500, 2300)
            color = autoRGB(255 - lerped, 255 - lerped, 255)
            #ax.text(geo.centroid.x, geo.centroid.y, s=str(median_price), withdash=True)
            if median_price == 500:
                color = '#ff0000'
        else:
            color = '#666666'
    else:
        color = '#666666'
    ax.add_patch(PolygonPatch(geo, fc=color, ec=color, alpha=1 ))
#add legend
patches = []
patches.append(mpatches.Patch(color='#666666', label='Insufficient Data'))
patches.append(mpatches.Patch(color='#ff0000', label='$500'))
price_colors = [700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300]
for price in price_colors:
    lerped = valueLERP(price, 500, 2300)
    color = autoRGB(255 - lerped, 255 - lerped, 255)
    label = '$'
    patches.append(mpatches.Patch(color=color, label='${}'.format(price)))
patches.reverse()
ax.legend(handles=patches, title='Median Room Price')
ax.axis('scaled')
plt.show()
