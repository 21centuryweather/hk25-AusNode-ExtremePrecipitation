

import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd

# Create lat / lon arrays
lat = []
lon = []
ws_names_detailed = ['Suva (Manual)', 'Suva (Automatic)', 'Lautoka (Manual)', 'Lautoka (TB3)', 'Penang (TB3)', 'Savusavu (Airport)', 'Labasa (Airport)']
ws_names = ['Suva', 'Suva', 'Lautoka', 'Lautoka', 'Penang (TB3)', 'Savusavu (Airport)', 'Labasa (Airport)']

#Suva (Manual)
lat_station = -18.147571
lon_station = 178.453610
lat.append(lat_station)
lon.append(lon_station)


#Suva (AWS)
lat_station = -18.147549
lon_station = 178.453608
lat.append(lat_station)
lon.append(lon_station)

#Lautoka (Manual)
lat_station = -17.618600
lon_station = 177.438900
lat.append(lat_station)
lon.append(lon_station)

#Lautoka (TB3)
lat_station = -17.618897
lon_station = 177.438730
lat.append(lat_station)
lon.append(lon_station)

#Penang (TB3)
lat_station = -17.373833
lon_station = 178.171619
lat.append(lat_station)
lon.append(lon_station)

#Savusavu (Airport)
lat_station = -16.806141
lon_station = 179.342817
lat.append(lat_station)
lon.append(lon_station)

#Labasa (Airport)
lat_station = -16.468900
lon_station = 179.339700
lat.append(lat_station)
lon.append(lon_station)

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

# Set extent to focus on a specific region (optional)
#ax.set_extent(bounds, crs=ccrs.PlateCarree())

# Add gridlines and labels (optional)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False

ax.scatter(lon, lat, c = 'red', s = 50, marker ='o')

# Add tags for each weather station
for i in range(0, len(lon)):
    plt.text(lon[i], lat[i], ws_names[i],
            horizontalalignment='right',
            transform=ccrs.Geodetic())

plt.title('Locations of Fiji weather stations')
plt.show()





