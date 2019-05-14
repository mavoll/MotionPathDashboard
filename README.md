# MotionPathDashboard
Dashboard to analyse and vizualize detection and tracking results

## Install
Install PostGIS (see MotionPathExtraction)

conda create --name dash python=3.6
conda activate dash
conda install ipykernel
python -m ipykernel install --user --name dash

pip install dash
pip install plotly --upgrade

pip install psycopg2
pip install shapely
pip install geopandas
conda install -c conda-forge gdal

## What we have and what we want?

### What we have

from MotionPathExtraction:
- Time-related trajectories (with pixel-coordinates within the image perspective the trajectories extracted from)
 of different classes 
 
from SimpleTPSMapping:
(- Time-related geographical trajectories (lat, long) of different classes)
because this transformation approach is not that accurate and its accuracy highly depends on manual input (target 
point marking), we first try an approach based an the pixel-coordinates tracks from MotionPathExtraction

from CountingTool:
- Number of different objects crossing former defined (within an image representing cams perspective) counting lines 
into one or another direction within an timeframe (and aggregations) 

### What we want

#### Indicators

- Def. "Frequency":
     (Entries / Leavings) - 1
     where Entries and Leavings are defined by the number of trajectories (distinguished by object classes) 
     entering ("Entries") or leaving ("Leavings") an tile (and aggs) within an time frame 

- Def. "Dwelltime":
     Lenght of the time span a objID (track) is within an tile (and aggs)

- Def. "Countings":
     Number of different objects crossing former defined (within an image representing cams perspective) counting lines 
     into one or another direction within an timeframe (and aggregations)
     
- Maybe later we include social media related indicators and wheather based indicators

#### Statistics

(see excel file as example for our catalogized records)

Basics:
--- Number detected objects/tracks (per object class) per cam and total
--- Track lenght (per object class) per cam

Indicators:
--- Frequency
--- Dwelltime
--- Countings 

Time granularities:
--- Total
--- Per day 
--- Per slice
--- Per subpart
--- Per minute
--- Per second
--- Per frame

Aggregations:
--- Count
--- Min 
--- Average
--- Max

#### Linear regression (Correlation between indicators)
#### Auto regressive models (Extrapolate into the future)

- ?other ml techniques to find pattern in time series?
- ?other ml techniques to find pattern in trajectories?

#### Dashboard 
-- Plotting (Indicators and statistics)
-- Maps (trajectories)
--- Animations (LineStringM and Point data)
-- Vizualizations
--- ?Counting lines?
--- ?

### What we need

to do:

- Raster image into tiles (or other type of unit) - implement python tool

- Data model, database and import from csv (SparkPipeline, later for geo-referenced trajectories PostGIS, GeoSpark, Django, ?)
- Dashboard (bokeh, dash, Zeppelin, ?)
- Calc indicators in regards to the tiles (its aggregations)
- Calc statistics
- Plot basic statistics on Dashboard
- more coming 
