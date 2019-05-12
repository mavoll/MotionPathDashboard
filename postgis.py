import psycopg2
import osgeo.ogr
import shapely
import shapely.wkt
import geopandas as gpd

connection = psycopg2.connect(database="gisdb",user="postgres", password="postgres")
cursor = connection.cursor()