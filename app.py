import dash
import geopandas as gpd
import postgis 

app = dash.Dash(__name__)
server = app.server
app.title = 'SmartSquare MotionPathDashboard'
app.config.suppress_callback_exceptions = True

# API keys and datasets
app.mapbox_access_token = 'pk.eyJ1Ijoic25vb3B0aGVub29iIiwiYSI6ImNqdm1qdTd2cDFkdWg0YXJ1YXZwNTFtdmcifQ.7ABtAp_1NyyHFFBbfAeIwQ'

db = postgis.Postgis("postgres", "postgres", "gisdb")    
sql = "SELECT cam, day, slice, part, subpart, track_id, time, track_class, geom FROM tracks_points_per_sec"
app.df = gpd.GeoDataFrame.from_postgis(sql, db.connection, geom_col='geom' )
app.df = app.df.to_crs('epsg:4326')
app.df['lon'] = app.df['geom'].y
app.df['lat'] = app.df['geom'].x
#df['time'] = df['time'].astype(str)
del app.df['geom']
app.df.sort_values(['time','track_id'], axis=0, ascending=True, inplace=True)
app.df['index'] = app.df.index


# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})