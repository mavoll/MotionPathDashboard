import argparse
import csv
import datetime
import psycopg2
import pandas as pd

# python test_data/insert_weather_into_postgis_daily.py -e 'gisdb' -u 'postgres' -w 'postgres' -f 'test_data/weather_data_hh/daily/produkt_klima_tag_20180304_20190904_01975.txt' -t 'weather_hamburg_daily' -i 'localhost' -x 5432

def insert_weather_day(self, track):       
        
    table = self.args['postgretable']
    
    # create table
    sql = "INSERT INTO " + table + "(stations_id, date, qn_3, fx, fm, qn_4, rsk, rskf, sdk, shk_tag, nm, vpm, pm, tmk, upm, txk, tnk, tgk) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
          
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
        ap.add_argument(
            "-f", "--file_path",
            default = None)

        self.args = vars(ap.parse_args())
        
        self._conn = None
        self._cur = None

        if self.args['postgrepassword'] is not None and self.args['postgretable'] is not None and self.args['file_path'] is not None:
            
            self._conn = psycopg2.connect(host=self.args['postgreip'],database=self.args['postgredb'], user=self.args['postgreuser'], password=self.args['postgrepassword'], port=self.args['postgreport'])
            self._conn.set_session(autocommit=True)
            self._cur = self._conn.cursor() 
        
        else:
            exit()


    def run(self):
        
        try:
        
            with open(self.args['file_path'], 'r') as csv_file:
    
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    next(csv_reader, None)
    
                    for row in csv_reader:                    
                        
                        date = row[1]
                        timestamp = datetime.datetime.strptime(date, '%Y%m%d')
                        col2 = None if (float(row[2]) < -998 or pd.isna(row[2])) else str(row[2])
                        col3 = None if (float(row[3]) < -998 or pd.isna(row[3])) else str(row[3])
                        col4 = None if (float(row[4]) < -998 or pd.isna(row[4])) else str(row[4])
                        col5 = None if (float(row[5]) < -998 or pd.isna(row[5])) else str(row[5])
                        col6 = None if (float(row[6]) < -998 or pd.isna(row[6])) else str(row[6])
                        col7 = None if (float(row[7]) < -998 or pd.isna(row[7])) else str(row[7])
                        col8 = None if (float(row[8]) < -998 or pd.isna(row[8])) else str(row[8])
                        col9 = None if (float(row[9]) < -998 or pd.isna(row[9])) else str(row[9])
                        col10 = None if (float(row[10]) < -998 or pd.isna(row[10])) else str(row[10])
                        col11 = None if (float(row[11]) < -998 or pd.isna(row[11])) else str(row[11])
                        col12 = None if (float(row[12]) < -998 or pd.isna(row[12])) else str(row[12])
                        col13 = None if (float(row[13]) < -998 or pd.isna(row[13])) else str(row[13])
                        col14 = None if (float(row[14]) < -998 or pd.isna(row[14])) else str(row[14])
                        col15 = None if (float(row[15]) < -998 or pd.isna(row[15])) else str(row[15])
                        col16 = None if (float(row[16]) < -998 or pd.isna(row[16])) else str(row[16])
                        col17 = None if (float(row[17]) < -998 or pd.isna(row[17])) else str(row[17])
                        insert_weather_day(self, (row[0], timestamp.strftime('%Y-%m-%d 00:00:00'), 
                                                  col2, col3, col4, col5, col6, col7, 
                                                  col8, col9, col10, col11, col12, col13, 
                                                  col14, col15, col16, col17))
                                                                  
        finally:
            
            if self._cur is not None: self._cur.close()
            if self._cur is not None: self._conn.close()

if __name__ == '__main__':
    #    import sys

    App().run()
