import dash
import psycopg2
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

app = dash.Dash(__name__)
server = app.server
app.title = 'SmartSquare MotionPathDashboard'
app.config.suppress_callback_exceptions = True

# API keys and datasets
app.mapbox_access_token = 'pk.eyJ1Ijoic25vb3B0aGVub29iIiwiYSI6ImNqdm1qdTd2cDFkdWg0YXJ1YXZwNTFtdmcifQ.7ABtAp_1NyyHFFBbfAeIwQ'

app.connection = psycopg2.connect(database="gisdb", user="postgres", host="localhost", port="5432", password="postgres")
app.connection.set_session(autocommit=True)
app.cursor = app.connection.cursor()

auth_provider = PlainTextAuthProvider(
            username='ecl', password='ssmq2020!ztRR')
app.cluster = Cluster(['194.95.79.98'], auth_provider=auth_provider)
app.session = app.cluster.connect('master_dataset')

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

