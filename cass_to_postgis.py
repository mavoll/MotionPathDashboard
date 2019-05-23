from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import geopandas as gpd


class App(object):

    def __init__(self):
    
        auth_provider = PlainTextAuthProvider(
            username='ecl', password='ssmq2020!ztRR')
        self.cluster = Cluster(['194.95.79.98'], auth_provider=auth_provider)
        self.session = self.cluster.connect('master_dataset')
        
        self.connection = psycopg2.connect(database='gisdb', user='postgres', host='localhost', port='5432', password='postgres')
        self.connection.set_session(autocommit=True)
        self.cursor = self.connection.cursor()
        
    def run(self):           
           
        try:
            cql = "SELECT year, month, day, hour, createdAt, username, tweetId, geolocationlatitude, geolocationlongitude FROM tweets_hamburg_located WHERE year=2018 ALLOW FILTERING"
            df = pd.DataFrame(list(self.session.execute(cql)))
            df = df.dropna(subset=['geolocationlatitude'])        
            df = df.dropna(subset=['geolocationlongitude'])
            df = df[df['geolocationlatitude'].between(35, 60)]
            df = df[df['geolocationlongitude'].between(-20, 30)]
            print(df)
            df['createdat'] = pd.to_datetime(df['createdat'].mul(1000000))
            df['city'] = "Hamburg"
            
            geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['geolocationlongitude'], df['geolocationlatitude']))              
            geo_df.crs = {'init': 'epsg:4326'}
            geo_df.sort_values(['createdat'])
            #geo_df = geo_df.to_crs({'init': 'epsg:5555'})
            table = 'twitter_points'            
            
            data = []
            for index, row in geo_df.iterrows():       
                
                point = 'SRID=4326; POINT({0} {1})'.format(row['geometry'].x, row['geometry'].y)
                data.append( (row['city'], row['year'], row['month'], row['username'], row['tweetid'], row['createdat'].strftime('%Y-%m-%d %H:%M:%S.%f'), point) )
                
                                   
            
            execute_values(self.cursor, 
                           "INSERT INTO " + table + "(city, year, month, username, tweetid, createdat, geom) VALUES %s", 
                           data)
            
                  
        finally:            
            self.cluster.shutdown()
            self.cursor.close()
            self.connection.close()
    
if __name__ == '__main__':
    #    import sys

    app = App()
    app.run()