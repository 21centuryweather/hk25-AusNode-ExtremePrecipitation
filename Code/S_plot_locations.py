

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd


# Read in weather station data
ws = pd.read_excel('Syd_station_info.xlsx')

# Create lat / lon arrays
lon = ws['Longitude']
lat = ws['Latitude']
ws_names = ws['Station_name']

# Get boundary of points
#margin = 2 # optional margin for the boundary
lon_min = min(lon)
lon_max = max(lat)
lat_min = min(lat)
lat_max = max(lat)
bounds = [lon_min, lon_max, lat_min, lat_max]
print(bounds)

# Create a basemap to plot 
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# Add coastlines, borders, and rivers
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.RIVERS)

# Add land and ocean color
ax.add_feature(cfeature.LAND, color='lightgray')
ax.add_feature(cfeature.OCEAN, color='lightblue')

# Add gridlines and labels (optional)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                      linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False

ax.scatter(lon, lat, c = 'red', s = 50, marker ='o')

# Add tags for each weather station
for i in range(0, len(lon)):
    plt.text(lon[i], lat[i], ws_names[i],
            horizontalalignment='right',
            transform=ccrs.Geodetic())

plt.title('Locations of Sydney weather stations')
plt.show()
