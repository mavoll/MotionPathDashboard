import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import geopandas as gpd
import datetime

from app import app
from apps import app_raw_data
from apps import app_twitter
from apps import app_weather 
from apps import app_pyramics


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='dummy'),
    dcc.Interval(
        id='interval-component',
        interval=60*60*1000, # in milliseconds
        n_intervals=0
    ),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
#               Input('interval-component', 'n_intervals')])
def display_page(pathname):
    if pathname == '/':
        if app_raw_data.df is None: 
            fetch_and_prepare_tracks_data()           
            
        return app_raw_data.layout()
    
    if pathname == '/twitter':        
        if app_twitter.df is None:
            fetch_and_prepare_twitter_data()
            
        return app_twitter.layout()
    
    if pathname == '/weather':
        if app_weather.df is None:       
            fetch_and_prepare_weather_data()
            
        return app_weather.layout()
    
    if pathname == '/pyramics':        
        if app_pyramics.df is None:
            fetch_and_prepare_pyramics_data()
            
        return app_pyramics.layout()
    
    else:
        return '404'

@app.callback(Output('dummy', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_dataframes(n):
    
    now = datetime.datetime.now()
    if n > 0 and now - app.last_update_time >= datetime.timedelta(hours=1):
        fetch_and_prepare_tracks_data()
        fetch_and_prepare_twitter_data()
        fetch_and_prepare_weather_data()        
        fetch_and_prepare_pyramics_data()
        app.last_update_time = now
        print("Updated at: " + now.strftime("%m/%d/%Y, %H:%M:%S"))        

def fetch_and_prepare_pyramics_data():
    
    sql = "SELECT id, measurement, sensor, name, type, start_time, end_time, age, dwell, gender, views FROM pyramics"
    app_pyramics.df = pd.read_sql_query(sql, con=app.connection) 
    app_pyramics.df.sort_values('start_time')    
        
    app_pyramics.days = list(set(app_pyramics.df['start_time'].astype(int)))        
    app_pyramics.days.sort()
    
def fetch_and_prepare_weather_data():
    
    sql = "SELECT stations_id, date, fx, fm, qn_4, rsk, rskf, sdk, shk_tag, nm, vpm, pm, tmk, upm, txk, tnk, tgk FROM weather_hamburg_daily"
    app_weather.df = pd.read_sql_query(sql, con=app.connection)
    app_weather.df.sort_values('date')
    
    sql2 = "SELECT stations_id, time, v_te005, ff, v_n, p, r1, wrtr, rs_ind, sd_s0, tt_tu, rf_tu FROM weather_hamburg_hourly"
    app_weather.df2 = pd.read_sql_query(sql2, con=app.connection)
    app_weather.df2.sort_values('time')
    
    app_weather.days = list(set(app_weather.df['date'].astype(int)))
    app_weather.days.sort()

def fetch_and_prepare_twitter_data():
    
    cql = "SELECT year, month, day, hour, createdAt, username, tweetId, text, geolocationlatitude, geolocationlongitude FROM tweets_hamburg_located WHERE geolocationlatitude >= 53.548292 AND geolocationlatitude <= 53.550744 AND geolocationlongitude >= 9.991699 AND geolocationlongitude <= 10.001452 ALLOW FILTERING"
    app_twitter.df = pd.DataFrame(list(app.session.execute(cql)))    
    app_twitter.df = app_twitter.df.dropna(subset=['geolocationlatitude'])        
    app_twitter.df = app_twitter.df.dropna(subset=['geolocationlongitude'])
    #app_twitter.df = app_twitter.df[app_twitter.df['geolocationlatitude'].between(53.549900, 53.551627)]
    #app_twitter.df = app_twitter.df[app_twitter.df['geolocationlongitude'].between(9.991399, 10.995798)]
    app_twitter.df['createdat'] = pd.to_datetime(app_twitter.df['createdat'].mul(1000000))
    #app_twitter.df = app_twitter.df.set_index(['createdat', 'tweetid'], drop=False)
    app_twitter.df.drop_duplicates(['text'],inplace=True)
    app_twitter.df['city'] = "Hamburg"
    #app_twitter.df.sort_index(inplace=True)
        
    #index = app_twitter.df.index.get_level_values(0).drop_duplicates()
    #data = pd.DataFrame(index=index)
    #series = data.sort_index().asfreq(freq='D')
    
    #app_twitter.days = list(set(series.index.astype(int)))
    app_twitter.days = list(set(app_twitter.df['createdat'].astype(int)))
    app_twitter.days.sort()
    
def fetch_and_prepare_tracks_data():
    
    sql = "SELECT cam, day, slice, part, subpart, track_id, time, track_class, geom FROM tracks_points_sec"
    app_raw_data.df = gpd.GeoDataFrame.from_postgis(sql, app.connection, geom_col='geom' )
    #df.crs = {'init': 'epsg:4326'}
    app_raw_data.df = app_raw_data.df.to_crs('epsg:4326')
    app_raw_data.df['lon'] = app_raw_data.df['geom'].y
    app_raw_data.df['lat'] = app_raw_data.df['geom'].x
    app_raw_data.df['track_class_name'] = [app_raw_data.classes[classs] for classs in app_raw_data.df['track_class'].astype(int)]
    del app_raw_data.df['geom']
    #df['time'] = pd.to_datetime(df['time'])
    app_raw_data.df['index'] = app_raw_data.df.index
    app_raw_data.df['minute'] = app_raw_data.df['time'].dt.strftime('%Y-%m-%d %H:%M:00')
    app_raw_data.df.sort_values(['time','index'])
    #df.set_index(['time', 'index'], inplace=True)
    #df.sort_index(inplace=True)
    
    app_raw_data.seconds = list(set(app_raw_data.df['time'].astype(int)))
    app_raw_data.seconds.sort()

if __name__ == '__main__':
    app.run_server(debug=True,
                   threaded=True,
                   port=8050)