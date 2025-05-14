# f_plot_subdaily
#%% Plots for the sub-daily fijian station data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import station_functions as sf

#%% Read in data
fpath = "../Data/Processed/Fiji/"
suva = pd.read_csv(fpath + "suva_aws_1H.csv")
lautoka = pd.read_csv(fpath + "lautoka_tb3_1H.csv")
penang = pd.read_csv(fpath + "penang_tb3_1H.csv")

#%% Extreme percentile plot
p = 95
colname = "rain_1h_mm"
t95_s = sf.get_threshold(suva, colname, p)

p95_s = sf.get_extreme_p(suva, colname, percentile = p)
p95_l = sf.get_extreme_p(lautoka, colname, percentile = p)
p95_p = sf.get_extreme_p(penang, colname, percentile = p)

plt.hist([p95_s, p95_l, p95_p])


# %%
