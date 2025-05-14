# Python file to read in & clean the sub-daily station data from Fiji
# Provided in excel format with separate tabs for each stations

#%%
# Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Options
# To remove errors from subsetting then performing df manipulations
pd.options.mode.chained_assignment = None  # default='warn'

#%% Read station data
# List of tab names
stations = ["Suva Manual", "Suva AWS", "Lautoka Manual", "Lautoka TB3", "Penang TB3"]
sub_daily_fpath = "../Data/Stations/Fiji_Meteorological_Service/Sub Daily Rainfall Data.xlsx"
col_names = ["date", "time", "rain_1h_mm", "accumulation_hours"]
outpath = "../Data/Processed/Fiji/"

# Read in data
suva_aws_full = pd.read_excel(sub_daily_fpath, 
                       sheet_name=stations[1], skiprows=2, header = None)
suva_m_full = pd.read_excel(sub_daily_fpath, sheet_name=stations[0], skiprows=2, header = None)
lautoka_m_full = pd.read_excel(sub_daily_fpath, sheet_name=stations[2], skiprows=2, header = None)
lautoka_tb3_full = pd.read_excel(sub_daily_fpath, sheet_name=stations[3], skiprows=2, header = None)
penang_tb3_full = pd.read_excel(sub_daily_fpath, sheet_name=stations[4], skiprows=2, header = None)

# Set column names
df_list = [suva_aws_full, suva_m_full, lautoka_m_full, lautoka_tb3_full, penang_tb3_full]
for df in df_list:
    df.columns = col_names

# %% Specify model runtime dates (March 1st 2020 - Feb 28th 2021)
start_date = "20200301"
end_date = "20210228"

# %%
# Accumulation hours
suva_aws_full.groupby("accumulation_hours").count()
suva_m_full.groupby("accumulation_hours").count()

#%% All dfs
for df in df_list:
    df.groupby("accumulation_hours").count()

#%% Compare daily totals of automatic and manual
# Remove >1h accumulations
suva_aws = suva_aws_full.loc[suva_aws_full.accumulation_hours == 1]
suva_m = suva_m_full.loc[suva_m_full.accumulation_hours == 1]

# Get daily total
aws_daily = suva_aws.groupby(suva_aws.date).rain_1h_mm.sum().to_frame()
m_daily = suva_m[suva_m.accumulation_hours == 1].groupby(suva_m.date).rain_1h_mm.sum().to_frame()

# Inner join for common days
aws_daily = aws_daily.reset_index(drop = False)
aws_daily.columns = ["date", "rain_aws"]
m_daily = m_daily.reset_index(drop = False)
m_daily.columns = ["date", "rain_manual"]
suva_joint = pd.merge(aws_daily, m_daily)

# Plot
plt.scatter(suva_joint.rain_aws, suva_joint.rain_manual)
plt.xlabel("AWS")
plt.ylabel("Manual")
# Automatic and manual don't match?

# %% Plot daily totals to identify outliers
aws_daily.rain_aws.plot()
daily_outliers = aws_daily[aws_daily.rain_aws > 250]

#%% Filter out days that are outlier
suva_aws = suva_aws.loc[~suva_aws.date.isin(daily_outliers.date)]
aws_daily2 = suva_aws.groupby(suva_aws.date).rain_1h_mm.sum()
aws_daily2[aws_daily2 > 150]
# Remaining high values (> 150mm) correspond to periods of floods / heavy rain

#%% Add datetime column and check for duplicates
suva_aws["datetime"] = pd.to_datetime(suva_aws.date.astype(str) + ' ' + suva_aws.time.astype(str))
timestamp_count = suva_aws.groupby(suva_aws.datetime).count()
sum(timestamp_count.time > 1)
# No duplicate timesteps

#%% Repeat for dates
day_count = suva_aws.time.groupby(suva_aws.date).count()
print("Too many obs:", sum(day_count > 24)) # No days with too many observations
print("Too few obs:", sum(day_count != 24)) # 59 days with too few observations

print("N days total:", len(day_count.index.unique()))
# 1920 days total

# Check if including accumulations helps 
full_day_count = suva_aws_full.accumulation_hours.groupby(suva_aws_full.date).sum()
print("Too many obs:", sum(full_day_count > 24)) # No days with too many observations
print("With accumulations\nToo few obs:", sum(full_day_count != 24))  # 63 days with too few observations
print("N days total:", len(full_day_count.index.unique()))
# 1933 days total

#%% Outlier checks
# Time series plot
plt.figure(1)
plt.plot(suva_aws["rain_1h_mm"])

# Histogram
# plt.figure(2)
# plt.hist(suva_aws["rain_1h_mm"])
# plt.figure(3)
# plt.hist(suva_aws.rain_1h_mm[suva_aws["rain_1h_mm"] > 0])

# Boxplot
plt.figure(2)
plt.boxplot(suva_aws.rain_1h_mm)

# %% Move to UTC
# Move model output rather than stations due to daily data accumulations
# suva_aws["UTC"] = suva_aws.datetime - pd.Timedelta(hours = 12)
suva_aws.reset_index(inplace=True)

# Add missing timesteps
expected_timesteps = pd.date_range(min(suva_aws.datetime), max(suva_aws.datetime), freq="h")
missing_timesteps = expected_timesteps[~expected_timesteps.isin(suva_aws.datetime)]

# Create df for missing timesteps
missing_df = pd.DataFrame({"datetime": missing_timesteps,
                           "date": missing_timesteps.date, 
                           "time": missing_timesteps.time, 
                           "rain_1h_mm": None, 
                           "accumulation_hours": None})
missing_df.set_index("datetime")

# Add into main df
suva_aws = pd.concat([suva_aws, missing_df])
suva_aws.sort_values("datetime", inplace=True)

suva_aws.to_csv(outpath + "suva_aws_1H.csv")
#%% Resample
suva_aws.set_index("datetime", inplace=True)
suva_3H = suva_aws.rain_1h_mm.resample('3H').sum(min_count=6).to_frame()
suva_3H.reset_index()

# Check that missing values result in missing sum
sum(np.isnan(suva_3H.rain_1h_mm))

# %% Export
import os
outpath = "../Data/Processed/Fiji/"
if not os.path.exists(outpath):
    os.mkdir(outpath)
suva_3H.to_csv(outpath + "suva_aws_3H.csv")

# %% Useful functions
# Dataframe must have a 'datetime' column
def complete_df(station_data):
    # Remove accumulations
    station_data = station_data.loc[station_data.accumulation_hours == 1]
    
    # Add datetime column
    station_data["datetime"] = pd.to_datetime(station_data.date.astype(str) + ' ' + station_data.time.astype(str))
     
    # Add missing timesteps
    expected_timesteps = pd.date_range(min(station_data.datetime), max(station_data.datetime), freq="h")
    missing_timesteps = expected_timesteps[~expected_timesteps.isin(station_data.datetime)]
    missing_df = pd.DataFrame({"datetime": missing_timesteps,
                            "date": pd.to_datetime(missing_timesteps.date), 
                            "time": missing_timesteps.time, 
                            "rain_1h_mm": None, 
                            "accumulation_hours": 1})
    missing_df.set_index("datetime")
    print(f"{len(missing_timesteps)} missing timesteps added, covering {len(missing_df.date.unique())} days")

    station_data = pd.concat([station_data, missing_df], sort = True)
    # station_data.sort_values("datetime", inplace=True)
    station_data = station_data.reindex(columns=["datetime", "date", "time", "rain_1h_mm", "accumulation_hours"])
    
    station_data.set_index("datetime", inplace = True)
    return station_data

def complete_resample(station_data, out_fname):
    # Resample
    station_data.set_index("datetime")
    station_3H = station_data.rain_1h_mm.resample('3H').sum(min_count=3).to_frame()
    station_3H.reset_index()

    # Export
    import os
    outpath = "../Data/Stations/Processed/Fiji/"
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    station_3H.to_csv(outpath + out_fname)
    
    return station_3H

def get_daily(station_data):
    daily_data = station_data.rain_1h_mm.resample("D").sum().to_frame()
    daily_data.rename(columns = {"rain_1h_mm": "rain_24h_mm"}, inplace = True)
    return daily_data
#%% Suva Manual ##################
suva_m = complete_df(suva_m_full)

m_daily = get_daily(suva_m)

# Plot time series
# Some high amounts but manual lookups appears to correlate with days of high rain/flooding
plt.figure(0)
plt.plot(suva_m.rain_1h_mm)

# Plot daily accumulations
# Average rainfall appears to be low for the last period?
plt.figure(1)
plt.plot(m_daily.rain_1h_mm)

# High values correspond to known flooding/heavy rain 
suva_m_daily_outliers = m_daily.loc[m_daily.rain_1h_mm > 250]

# Remove outlier days - NA

# Save one hourly
suva_m.to_csv(outpath + "suva_man_1H.csv", index = True)
m_daily.to_csv(outpath + "suva_man_24H.csv", index = True)

# %% Lautoka ##################
lautoka_m_full.groupby("accumulation_hours").time.count()

# %%
lautoka_m = complete_df(lautoka_m_full)

# Plot full timeseries
plt.plot(lautoka_m.rain_1h_mm)

l_m_daily = get_daily(lautoka_m)
plt.plot(l_m_daily.rain_24h_mm)
# High values again correspond to known heavy rain/flooding
# e.g. 2006-01-29 maximum value from a tropical monsoon

lautoka_m.to_csv(outpath + "lautoka_man_1H.csv")
# %% Lautoka TP3 ##################
lautoka_tb3_full.groupby("accumulation_hours").time.count()
# All 1 hour accumulations

lautoka_tb3 = complete_df(lautoka_tb3_full)
# Missing 9941 timesteps over 464 days
# Date range = 2008-12-15 to 2022-12-31

plt.figure(1)
plt.plot(lautoka_tb3.rain_1h_mm)

l_tb3_daily = get_daily(lautoka_m)
plt.figure(2)
plt.plot(l_tb3_daily.rain_24h_mm)

# Check day of week averages
l_tb3_daily.reset_index(inplace=True)
l_tb3_daily.rain_24h_mm.groupby(l_tb3_daily.datetime.dt.day_of_week).mean()

# Comparison with manual
plt.figure(3)
plt.scatter(lautoka_tb3.rain_1h_mm, lautoka_tb3.rain_1h_mm)
plt.xlabel("Manual")
plt.ylabel("TP3")

# Export 1H
lautoka_tb3.to_csv(outpath + "lautoka_tb3_1H.csv")

#%% Penang TP3 ##################
penang_tb3 = complete_df(penang_tb3_full)
# 1784 missing timesteps added, covering 124 days

plt.plot(penang_tb3.rain_1h_mm)

penang_tb3_daily = get_daily(penang_tb3)
plt.figure(2)
plt.plot(penang_tb3_daily.rain_24h_mm)

penang_tb3.to_csv(outpath + "penang_tb3_1H.csv", index=True)

# %%Check day of week averages
penang_tb3_daily.reset_index(inplace=True)
plt.plot(penang_tb3_daily.rain_24h_mm.groupby(penang_tb3_daily.datetime.dt.day_name()).mean())
plt.xticks()
# %%
