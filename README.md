# Model intercomparison for extremes precipitation  <img src='https://21centuryweather.org.au/wp-content/uploads/Hackathon-Image-WCRP-Positive-1536x736.jpg' align="right" height="139" />

How well do convection-permitting models represent extreme precipitation events?


**Project leads:** Ashneel Chandra (PhotonPi), Leena Khadke (khadkeleenasanjay)

**Project members:** Skye Williams-Kelly (SkyeEllen), 
Greta Paget (gpaget98),
Joel Treutlein (Jatreutlein),
Xueying Wang (SylviaWang87),
Kathiana Aznaran Luk (kath18),
Huyen Luong (huyenluong),
Phuong Loan Nguyen (ploan)

**Collaborators:** list here other collaborators to the project.

**Data:**
* Name, link
* Name, link

## Contributing Guidelines

> The group will decide how to work as a team. This is only an example. 

This section outlines the guidelines to ensure everyone can work and collaborate. All project members have write access to this repository, to avoid overlapping and merge issues make sure you discuss the plan and any changes to existing code or analysis.

### Project organisation

All tasks and activities will be managed through GitHub Issues. While most discussions will take place face-to-face, it is important to document the main ideas and decisions on an issue. Issues will be assigned to one or more people and classified using labels. If you want to work on an issue, comment and make sure is assigned to you to avoid overlapping. If you find a problem in the code or a new task, you can open an issue. 

### How to collaborate

* **Main branch:** We want to keep things simple, if you are working on a notebook alone you can push changes to the main branch. Make sure to 1) only add and ccommit that file and nothing else, 2) pull from the remote repo and 3) push.

*  **File naming conventions:** use the prefix `_f__` in the filename for analysis of Fijian data and use the prefix `_s__` for Sydney region.

*  **Timezones:** Station data is provided in local standard time (i.e. without Daylight Savings where applicable). Model output should be shifted by the appropirate amount (Sydney = UTC + 10, Fiji = UTC + 12) before comparisons/accumulating over days.

### Repository structure

```bash
hk25-AusNode-ExtremePrecipitation/
├── LICENCE
├── README.md
├── Code
│   ├── analysis.py
│   ├── __init__.py
│   └── read.py
├── Data
│   ├── Processed/
│   ├── Stations/
├── Plots
│   ├── F_weather_station_locations.png
│   ├── S_weather_station_locations.png
└── tests
    ├── test_analysis.py
    └── test_read.py
```
* `Code/` this folder will include the code to analyse the data.
* `Data/` this folder contains the original Fijian station data and processed station data for both Sydney and Fiji
* `Plots/` this folder contains plotted output/image files

