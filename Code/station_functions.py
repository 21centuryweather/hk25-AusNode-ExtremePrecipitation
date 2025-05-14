# Station functions
# Re-useable across both Sydney and Fiji

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
