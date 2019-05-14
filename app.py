import dash
import postgis


app = dash.Dash(__name__)
server = app.server
app.title = 'SmartSquare MotionPathDashboard'
app.config.suppress_callback_exceptions = True

# API keys and datasets
app.mapbox_access_token = 'pk.eyJ1Ijoic25vb3B0aGVub29iIiwiYSI6ImNqdm1qdTd2cDFkdWg0YXJ1YXZwNTFtdmcifQ.7ABtAp_1NyyHFFBbfAeIwQ'
app.db = postgis.Postgis("postgres", "postgres", "gisdb")    

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

