import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.datastax.spark:spark-cassandra-connector_2.11:2.0.5 --conf spark.cassandra.connection.host=194.95.79.98 --conf spark.cassandra.auth.username=ecl --conf spark.cassandra.auth.password=ssmq2020!ztRR pyspark-shell'

import sys

from pyspark import SparkContext
from pyspark.sql import SQLContext


class Sparkpipeline(object):
    
    def __init__(self):
        
        try:
            self.sc = SparkContext("spark://194.95.79.98:7077", "pyspark")
            self.sqlContext = SQLContext(self.sc)
            
        except Exception:            
            print("ERROR - connecting Spark")
            print(sys.exc_info()[0] + sys.exc_info()[1])
        finally:
            if(self.sc):
                self.sc.stop()
                print("Spark connection is closed")
    
    def load_df_from_cassandra(self, keys_space_name, table_name):
        
        table_df = None
        
        try:
            load_options = {"keyspace": keys_space_name, "table": table_name}
            table_df = self.sqlContext.read\
                .format("org.apache.spark.sql.cassandra")\
                .options(**load_options)\
                .load()
                
        except Exception:            
            print("ERROR - loading df from cassandra")
            print(sys.exc_info()[0] + sys.exc_info()[1])
        
        return table_df
    
    def save_df_to_cassandra(self, keys_space_name, table_name, pyspark_df):
        
        try:
            save_options = {"keyspace": keys_space_name, "table": table_name}
            self.sqlContext.write\
                .format("org.apache.spark.sql.cassandra")\
                .mode('append')\
                .options(**save_options)\
                .save()
        
        except Exception:            
            print("ERROR - saving df to cassandra")
            print(sys.exc_info()[0] + sys.exc_info()[1])
    
  
if __name__ == '__main__':
    app = Sparkpipeline()
    df = app.load_and_get_table_df("master_dataset", "tweets_counter_yearly")
    df.show()
    
    