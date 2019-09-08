import argparse
import csv
import datetime
import psycopg2
import pandas as pd

# python test_data/insert_weather_into_postgis_hourly.py -e 'gisdb' -u 'postgres' -w 'postgres' -t 'weather_hamburg_hourly' -i 'localhost' -x 5432

def insert_weather_hour(self, track):       
        
    table = self.args['postgretable']
    
    # create table
    sql = "INSERT INTO " + table + "(stations_id, time, v_te005, ff, v_n, p, r1, wrtr, rs_ind, sd_s0, tt_tu, rf_tu) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
          
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
            
            files = ["test_data/weather_data_hh/hourly/produkt_eb_stunde_20180304_20190904_01975.txt",
                     "test_data/weather_data_hh/hourly/produkt_f_stunde_20180304_20190409_01975.txt",
                     "test_data/weather_data_hh/hourly/produkt_n_stunde_20180304_20190904_01975.txt",
                     "test_data/weather_data_hh/hourly/produkt_p0_stunde_20180304_20190904_01975.txt",
                     "test_data/weather_data_hh/hourly/produkt_rr_stunde_20180304_20190904_01975.txt",
                     "test_data/weather_data_hh/hourly/produkt_sd_stunde_20180304_20190904_01975.txt",
                     "test_data/weather_data_hh/hourly/produkt_tu_stunde_20180304_20190904_01975.txt"]
            
            for i, file_path in enumerate(files):
                if i == 0:
                    dfs = pd.read_csv(file_path, delimiter=';', index_col=[0, 1])
                else:
                    dfs = pd.concat([dfs, pd.read_csv(file_path, delimiter=';', index_col=[0, 1])], axis=1)
                
            dfs.to_csv("test_data/weather_data_hh/hourly/concat_20180304_20190904_01975.txt")
            for index, row in dfs.iterrows():
                date = str(index[1])
                v_te005 = None if (float(row[2]) < -998 or pd.isna(row[2])) else str(row[2])
                ff = None if (float(row[9]) < -998 or pd.isna(row[9])) else str(row[9]) 
                v_n = None if (row[14] == -999 or pd.isna(row[14])) else str(int(row[14])) 
                p = None if (float(row[17]) < -998 or pd.isna(row[17])) else str(row[17]) 
                r1 = None if (float(row[21]) < -998 or pd.isna(row[21])) else str(row[21]) 
                wrtr = None if (row[23] == -999 or pd.isna(row[23])) else str(int(row[23])) 
                rs_ind = None if (row[22] == -999 or pd.isna(row[22])) else str(int(row[22])) 
                sd_s0 = None if (row[26] == -999 or pd.isna(row[26])) else str(int(row[26]))
                tt_tu = None if (float(row[29]) < -998 or pd.isna(row[29])) else str(row[29])
                rf_tu = None if (float(row[30]) < -998 or pd.isna(row[30])) else str(row[30])
                timestamp = datetime.datetime.strptime(date, '%Y%m%d%H')  
                insert_weather_hour(self, (index[0], timestamp.strftime('%Y-%m-%d %H:00:00'), 
                                          v_te005, ff, v_n, p, r1, wrtr, 
                                          rs_ind, sd_s0, tt_tu, rf_tu))
                                                                  
        finally:
            
            if self._cur is not None: self._cur.close()
            if self._cur is not None: self._conn.close()

if __name__ == '__main__':
    #    import sys

    App().run()
