# MotionPathDashboard
Dashboard to analyse and vizualize detection and tracking results (using Dash by Plotly)

## Install

Install PostGIS (see MotionPathExtraction){https://github.com/mavoll/MotionPathsExtraction} and create table.
```
conda create --name dash python=3.6
conda activate dash
conda install ipykernel
python -m ipykernel install --user --name dash

pip install dash
pip install plotly --upgrade

pip install psycopg2
pip install geopandas

python index.py
```

## Apps (created with Dash by Plotly)

### Raw data

<p align="center">
  <img src="/images/dashboard_1.png" width="800" align="middle">
</p>

PostGIS data table:
```
CREATE TABLE postgis.tracks_points_per_sec
(
  slice text NOT NULL,
  cam text NOT NULL,
  day text NOT NULL,
  part integer NOT NULL,
  subpart integer NOT NULL,
  track_id integer NOT NULL,
  time timestamp NOT NULL,
  track_class text NOT NULL,
  geom geometry(Point, 5555) NOT NULL,
  PRIMARY KEY (slice, cam, day, part, subpart, track_id)
);

```
Here the sample csv file and the import script from [MotionPathExtraction](https://github.com/mavoll/MotionPathsExtraction/tree/master/scripts) is used for demo. Accessed through `psycopg2` and fetched into GeoDataFrame using `geopandas.GeoDataFrame.from_postgis()` function.

Fetching data from [SparkPipeline](https://github.com/mavoll/SparkPipeline) through `pyspark` is coming later for bigger data sets.

Components:
- Dropdown (multi select)
- Time RangeSlider
- Time Slider
- Scattermapbox
- DataTable
- Pie
- Scatter (mode='lines')

### Twitter data

<p align="center">
  <img src="/images/dashboard_twitter.png" width="800" align="middle">
</p>

PostGIS data table:
```
CREATE TABLE twitter_points
(
  city text NOT NULL,
  year integer NOT NULL,
  month integer NOT NULL,
  username text NOT NULL,
  tweetid bigint NOT NULL,
  createdat timestamp NOT NULL,
  geom geometry(Point, 4326) NOT NULL,
  PRIMARY KEY (createdat, tweetid)
);
```

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

## Further development and research opportunities

## Authors

* **Marc-André Vollstedt** - marc.vollstedt@gmail.com

## Acknowledgments
