import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app_raw_data
from apps import app_twitter


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([    
    dcc.Link('Go to Animation', href='/animation'),
    html.Br(),
    dcc.Link('Go to Statistics', href='/statistics'),
    html.Br(),
    dcc.Link('Go to Indicators', href='/indicators')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return app_raw_data.layout
    if pathname == '/statistics':
        return app_raw_data.layout
    if pathname == '/indicators':
        return app_raw_data.layout
    if pathname == '/twitter':
        return app_twitter.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)