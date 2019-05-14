import psycopg2
import sys


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