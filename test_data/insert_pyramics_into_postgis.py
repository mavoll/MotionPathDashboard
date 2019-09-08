import argparse
import csv
import datetime
import psycopg2
import pandas as pd

# python test_data/insert_pyramics_into_postgis.py -e 'gisdb' -u 'postgres' -w 'postgres' -t 'pyramics' -i 'localhost' -x 5432

def insert_pyramics(self, track):       
        
    table = self.args['postgretable']
    
    # create table
    sql = "INSERT INTO " + table + "(measurement, sensor, name, type, start_time, end_time, age, dwell, gender, views) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
          
    try:
        self._cur.execute(sql,track)
           
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    


class App(object):

    def __init__(self):

        ap = argparse.ArgumentParser()
        ap.add_argument(
            "-u", "--postgreuser", 
            default= "hcuadmin")
        ap.add_argument(
            "-w", "--postgrepassword",
            default = None)
        ap.add_argument(
            "-i", "--postgreip",
            default = "localhost")
        ap.add_argument(
            "-x", "--postgreport",
            default = 5432)
        ap.add_argument(
            "-e", "--postgredb",
            default = "gisdata")
        ap.add_argument(
            "-t", "--postgretable",
            default = "weather_daily")

        self.args = vars(ap.parse_args())
        
        self._conn = None
        self._cur = None

        if self.args['postgrepassword'] is not None and self.args['postgretable'] is not None:
            
            self._conn = psycopg2.connect(host=self.args['postgreip'],database=self.args['postgredb'], user=self.args['postgreuser'], password=self.args['postgrepassword'], port=self.args['postgreport'])
            self._conn.set_session(autocommit=True)
            self._cur = self._conn.cursor() 
        
        else:
            exit()


    def run(self):
        
        try:
            
            dfs = []
            
            files = ["test_data/pyramics_data_hh/Backhus_interaction_2018-01-01_2019-10-01.csv",
                     "test_data/pyramics_data_hh/Buergerstiftung_interaction_2018-01-01_2019-10-01.csv"]
            
            for i, file_path in enumerate(files):
                if i == 0:
                    dfs = pd.read_csv(file_path, delimiter=',')
                else:
                    dfs = pd.concat([dfs, pd.read_csv(file_path, delimiter=',')], ignore_index=True)
              
            dfs.to_csv("test_data/pyramics_data_hh/concat_2018-01-01_2019-10-01.csv")
            
            for index, row in dfs.iterrows():
                measurement = None if (row[0] == -1 or pd.isna(row[0])) else str(row[0])
                sensor = None if (row[1] == -1 or pd.isna(row[1])) else str(row[1])
                name = None if (row[2] == -1 or pd.isna(row[2])) else str(row[2]) 
                mtype = None if (row[3] == -1 or pd.isna(row[3])) else str(row[3]) 
                start_time = None if (row[4] == -1 or pd.isna(row[4])) else str(row[4]) 
                end_time = None if (row[5] == -1 or pd.isna(row[5])) else str(row[5]) 
                age = None if (row[6] == -1 or pd.isna(row[6])) else str(int(row[6])) 
                dwell = None if (row[7] == -1 or pd.isna(row[7])) else str(int(row[7])) 
                gender = None if (row[8] == -1 or pd.isna(row[8])) else str(row[8])
                views = None if (row[9] == -1 or pd.isna(row[9])) else str(int(row[9]))
                
                
                insert_pyramics(self, (measurement, sensor, name, mtype,
                                           start_time, end_time,
                                           age, dwell, gender, views))
                                                                  
        finally:
            
            if self._cur is not None: self._cur.close()
            if self._cur is not None: self._conn.close()

if __name__ == '__main__':
    #    import sys

    App().run()
