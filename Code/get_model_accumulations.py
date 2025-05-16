# Get Daily Accumulations from hourly Model output

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import station_functions as sf
from datetime import timedelta
from scipy.stats import gaussian_kde

# %% Create daily data for each model & location (Fiji)
model_files = ["Lautoka_TB3_z10.csv", "Suva_AWS_z10.csv", "Penang_TB3_z10.csv", 
               "Labasa_Airport_z10.csv", "Savusavu_Airport_z10.csv"]
fpath_u = "../Data/uk_model_fiji_z10/"
fpath_g = "../Data/germney_model_fiji_z10/"
outpath_model_daily = "../Data/Model_Daily/Fiji/"

for fname in model_files:
    loc = fname.split("_")[0]
    
    # Germany (ICON) model
    g_data = sf.read_model_fiji(fpath_g, "germany_node_" + fname)
    g_daily = sf.get_daily_model(g_data)
    g_daily.to_csv(outpath_model_daily + "g_" + loc + "_daily.csv")
    
    # UK (UM) model
    u_data = sf.read_model_fiji(fpath_u, "uk_node_" + fname)
    u_daily = sf.get_daily_model(u_data)
    u_daily.to_csv(outpath_model_daily + "u_" + loc + "_daily.csv")
   
#%% Create daily data for each model & location in Sydney    
sydney_files = ["Badgerys_Creek_AWS_z10.csv", "Bankstown_Airport_AWS_z10.csv", "Norah_Head_AWS_z10.csv", 
                "Richmond_RAAF_z10.csv", "Sydney_Airport_AMO_z10.csv"]
fpath_u = "../Data/uk_model_sydney_z10/"
fpath_g = "../Data/germney_model_sydney_z10/"
outpath_model_daily = "../Data/Model_Daily/Sydney/"

for fname in sydney_files:
    loc = fname.split("_")[0]
    
    # Germany (ICON) model
    g_data = sf.get_daily_sydney(fpath_g, "germany_node_" + fname)
    g_data.to_csv(outpath_model_daily + "g_" + loc + "_daily.csv")
    
    # UK (UM) model
    u_data = sf.get_daily_sydney(fpath_u, "uk_node_" + fname)
    u_data.to_csv(outpath_model_daily + "u_" + loc + "_daily.csv")