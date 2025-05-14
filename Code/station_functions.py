# Station functions
# Re-useable across both Sydney and Fiji

import numpy as np
from datetime import timedelta
import pandas as pd

# Get the threshold for nth percentile for a given dataset
def get_threshold(stat_data, precip_colname, percentile):
    precip_data = stat_data[precip_colname].dropna()
    precip_data = precip_data[precip_data > 0.2]

    # Step 4: Calculate the percentile
    threshold = np.percentile(precip_data, percentile)
    return threshold

# Get data above a given threshold or percentile
def get_extreme_p(stat_data, precip_colname, threshold = None, percentile = 0.95):
    if(threshold == None):
        threshold = get_threshold(stat_data, precip_colname, percentile)
    
    precip_data = stat_data[precip_colname].dropna()
    precip_data = precip_data[precip_data > 0.2]
    
    # Filter precip data for threshold
    extreme_data = precip_data[precip_data > threshold]

    # Return 
    return extreme_data

# Shift 
def utc2local(data, time_shift):
    data["datetime"] = data["datetime"] + timedelta(hours=time_shift)
    return data

# Calculate the daily accumulations from hourly model data
# Assumes the data has already been shifted to local time
# If it hasn't, set shifted = True

# Assumes the rainfall is in a column named "rain_1h_mm"
def get_daily_model(data, shifted = False, shift = 0):
    if shifted == False:
        data = utc2local(data, shift)

    # Resample to daily between 9am - 9am
    data = data.set_index("datetime")
    # + 9 hours to start at 9am
    data = data.rain_1h_mm.resample('24h', offset = timedelta(hours = 9)).sum().to_frame()
    data.reset_index(inplace = True)
    
    # Shift so that the accumulation is shown at the end of the period
    data["datetime"] = data["datetime"] + timedelta(days = 1)
    
    return data


# Read in model data and 
def read_model_fiji(fpath, fname):
    data = pd.read_csv(fpath + fname)
        
    # Reformat datetime column
    data["datetime"] = pd.to_datetime(data["time"])
    
    # Shift to local time
    data = utc2local(data, 12)

    # Add other columns
    data["year"] = data.datetime.dt.year
    data["hour"] = data.datetime.dt.hour
    data["time"] = data.datetime.dt.time
    
    # Rename/reorder for consistency for daily
    data = data[["datetime", "year", "hour", "value"]]
    data.rename(columns = {"value": "rain_1h_mm"}, inplace=True)

    return data

