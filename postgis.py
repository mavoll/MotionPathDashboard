import psycopg2
import sys
import geopandas as gpd


class Postgis(object):
    
    def __init__(self, user, password, database, host="localhost", port="5432"):
        
        try:
            self.connection = psycopg2.connect(database=database, user=user, host=host, port=port, password=password)
            self.connection.set_session(autocommit=True)
            self.cursor = self.connection.cursor()
        
        except Exception:            
            print("ERROR - connecting PostGIS")
            print(sys.exc_info()[0] + sys.exc_info()[1])                
    
    def execute_sql(self, sql, data=None):
        
        try:
            self.cursor.execute(sql, data)            
                
        except Exception:            
            print("ERROR - executing sql on postgis")
            print(str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            
    def close(self):
        
        try:
           if(self.connection):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")         
                
        except Exception:            
            print("ERROR - closing connection")
            print(str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
    
  
if __name__ == '__main__':
    
    app = Postgis("postgres", "postgres", "gisdb")
    
    sql = "SELECT track_id, time, track_class, geom FROM tracks_points_per_sec WHERE slice='Testdatensatz' AND cam='kirchvorplatz' AND day='Testdatensatz' AND  part=1 AND subpart=1"
    df = gpd.GeoDataFrame.from_postgis(sql, app.connection, geom_col='geom' )
    df.plot()    
    
    app.close()