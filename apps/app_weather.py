from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import colorsys
from plotly import graph_objs as go

from components import Header, Footer
from app import app
                                    
indicators_daily = {'fx': 'wind speed max', 'fm': 'wind speed average', 'rsk': 'precipitation sum', 
              'rskf': 'precipitation type', 'sdk': 'sun sum', 'shk_tag': 'snow sum', 
              'nm': 'cloud amount average', 'vpm': 'steam pressure average', 'pm': 'air pressure', 
              'tmk': 'temp average', 'upm': 'air humidity average', 'txk': 'temp max', 
              'tnk': 'temp min', 'tgk': 'soil temp 5cm min'}

indicators_hourly = {'v_te005': 'soil temp 5cm', 'ff': 'wind speed', 'v_n': 'cloud amount', 
              'p': 'air pressure type', 'r1': 'precipitation', 'wrtr': 'precipitation type', 
              'rs_ind': 'precipitation indicator', 'sd_s0': 'sun', 'tt_tu': 'temp', 'rf_tu': 'air humidity'}

df = None
df2 = None
days = None

#  Layouts
layout_table = dict(
    autosize=True,
    height=700,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Data table'
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_lines = dict(
    
    showlegend=True,
    dragmode="select",
    autosize=True,
    height=600,
    
)

layout_lines2 = dict(
    
    showlegend=True,
    dragmode="select",
    autosize=True,
    height=600,
    
)

def layout():
    return html.Div(
        html.Div([
            html.Div(id='page-weather-content'),
            Header(),
            html.Div(
                [
                    html.H2(children='Weather',
                            style={
                                'textAlign': 'center'
                            },
                            className='twelve columns')
                    
                ], className="row"
            ),
            html.Br(),
            html.Div([
    				dcc.RangeSlider(
    					id='slider',
    					min=min(days),
    					max=max(days),
                        step=1000000000 * 3600 * 24,
                        updatemode='mouseup', #'drag' 
                        pushable=True,
    					value=[min(days) , max(days)],
    					marks={int(timestamp): datetime.fromtimestamp(timestamp/1000000000) for timestamp in days[::30]},
    				),
    			], className='twelve columns'),       
            html.Br(),
            html.Br(),
            html.Br(),
            # Map + table + Histogram
            html.Div(
                [          
                    html.Div(
                        [
                            html.H5(children='Weather daily',
                                    style={
                                        'textAlign': 'center'
                                    },
                                    className='twelve columns')
                            
                        ], className="row"
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'daily',
                                            options= [{'label': value,'value': key}
                                                    for key, value in indicators_daily.items()],
                                            value=['fm', 'rsk', 'sdk', 'nm', 'tmk'],
                                            multi=True
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),
                    html.Div([
                        dcc.Graph(
                            id="weather-daily-line-graph")]
                        , className="twelve columns"
                    ),
                    html.Div(
                        [
                            html.H5(children='Weather hourly',
                                    style={
                                        'textAlign': 'center'
                                    },
                                    className='twelve columns')
                            
                        ], className="row"
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'hourly',
                                            options= [{'label': value,'value': key}
                                                    for key, value in indicators_hourly.items()],
                                            value=['tt_tu'],
                                            multi=True
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),
                    html.Div([
                        dcc.Graph(
                            id="weather-hourly-line-graph")]
                        , className="twelve columns"
                    ),
                    Footer(),
                ], className="row"
            )
       ], className='ten columns offset-by-one'))
  
@app.callback(
Output('weather-daily-line-graph', 'figure'),
[Input('slider', 'value'),
 Input('daily', 'value')])
def update_line_graph_daily(slider, daily):
    
    aux = df.copy()      
    
    aux = aux[aux['date'].astype(int) >= slider[0]]
    aux = aux[aux['date'].astype(int) <= slider[1]]
    
    data = []    
         
    if not aux.empty:
        for type in daily:
            data.append(
                     dict(
                         type='scatter',
                         mode='lines',
                         x= aux["date"],
                         y= aux[type],
                         name= indicators_daily[type], 
                         line = dict(
                             color= create_unique_color_int(int(hash(type))),
                             width = 2,
                             dash = 'dot')
                             )
                 )        
        
    return go.Figure(data=data, layout=layout_lines)

@app.callback(
Output('weather-hourly-line-graph', 'figure'),
[Input('slider', 'value'),
 Input('hourly', 'value')])
def update_line_graph_hourly(slider, hourly):
    
    aux = df2.copy()
    
    aux = aux[aux['time'].astype(int) >= slider[0]]
    aux = aux[aux['time'].astype(int) <= slider[1]]
    
    data = []    
         
    if not aux.empty:
        for type in hourly:
            data.append(
                     dict(
                         type='scatter',
                         mode='lines',
                         x= aux["time"],
                         y= aux[type],
                         name= indicators_hourly[type], 
                         line = dict(
                             color= create_unique_color_int(int(hash(type))),
                             width = 2,
                             dash = 'dot')
                             )
                 )        
        
    return go.Figure(data=data, layout=layout_lines)

def create_unique_color_int(tag, hue_step=0.0000000001):

    h, v, = (tag * hue_step) % 1, 1. - (int(tag * hue_step) % 4) / 5.
    r, g, b = colorsys.hsv_to_rgb(h, 1., v)

    return 'rgba(' + str(int(255 * r)) + ',' + str(int(255 * g)) + ',' + str(int(255 * b))+ ',1)'