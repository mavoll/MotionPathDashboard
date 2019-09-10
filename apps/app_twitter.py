import dash_table as dt
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import colorsys
import pandas as pd
from plotly import graph_objs as go

from components import Header, Footer
from app import app

df = None
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

layout_map = dict(
    autosize=True,
    height=700,
    animate=True,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    mapbox=dict(
        accesstoken=app.mapbox_access_token,
        style="light",
        center=dict(
            lon=9.996806,
            lat=53.549535
        ),
        zoom=17,
    )
)

layout_pies = dict(
    
    title='Num tweets per user and name',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=700,
    
)

layout_lines = dict(
    
    showlegend=True,
    dragmode="select",
    autosize=True,
    height=300,
    
)

def layout():
    return html.Div(
        html.Div([
            html.Div(id='page-twitter-content'),
            Header(),
            html.Div(
                [
                    html.H2(children='Twitter (hourly updated)',
                            style={
                                'textAlign': 'center'
                            },
                            className='twelve columns')
                    
                ], className="row"
            ),    
            # Selectors        
            html.Div([
    				dcc.RangeSlider(
    					id='a-slider',
    					min=days[0],
    					max=days[-1],
                        step= 24 * 60 * 60 * 1000000000,
                        updatemode='mouseup', #'drag' 
                        pushable=True,
    					value=[days[0], days[-1]],# int(max(timestamps) - min(timestamps))
    					marks={int(datetime.timestamp(date)) * 1000000000: date.strftime("%Y-%m-%d") for date in pd.date_range(min(days), max(days)).tolist()[::30]},
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
                            dcc.Graph(id='a-map-graph',
                                      animate=True)
                        ], className = "twelve columns"
                    ),
                    html.H5(children='Number users tweeting',
                        style={
                            'textAlign': 'center'
                        },
                        className='twelve columns'),
                    html.Div([
                        dcc.Graph(
                            id="line-graph-twitteruser")]
                        , className="twelve columns"
                    ),
                    html.H5(children='Number tweets',
                        style={
                            'textAlign': 'center'
                        },
                        className='twelve columns'),
                    html.Div([
                        dcc.Graph(
                            id="line-graph-twitteruser2")]
                        , className="twelve columns"
                    ),
                    Footer(),
                ], className="row"
            )
       ], className='ten columns offset-by-one'))
    
@app.callback(
Output('a-map-graph', 'figure'),
[Input('a-slider', 'value')])
def update_a_map(a_slider):
    
    aux = df.copy()
    aux = aux[aux['createdat'].astype(int) >= a_slider[0]]
    aux = aux[aux['createdat'].astype(int) <= a_slider[1]]
    data = []
    
    if not aux.empty:
        
        for city in list(set(aux['city'])):
            #tmp = aux[aux['city'] == city]
            data.append(
                        dict(
                                type= 'scattermapbox',                                
                                lat= aux['geolocationlatitude'].tolist(),
                                lon= aux['geolocationlongitude'].tolist(),
                                #hoverinfo= aux['text'].tolist(),
                                hovertext= [["{} <br> username: {} <br>createdat: {} <br>tweetid: {}".format(t,i,j,k)]
                                                for t,i,j,k in zip(aux['text'], aux['username'], aux['createdat'],aux['tweetid'])],
                                mode= "markers",
                                name= city,
                                marker= dict(
                                    color= create_unique_color_int(int(hash(city))),
                                    size= 6,
                                    opacity= 0.7,
                                )
                            )
                        )
        
    return dict(data= data, layout= layout_map)

@app.callback(
Output('line-graph-twitteruser', 'figure'),
[Input('a-slider', 'value')])
def update_line_graph(slider):
    
    tmp = df.copy()
                
    tmp = tmp[tmp['createdat'].astype(int) >= slider[0]]
    tmp = tmp[tmp['createdat'].astype(int) <= slider[1]]
    
    data = []    
    
    
    tmp['createdat'] = pd.to_datetime(tmp['createdat'])
    grouped = tmp.groupby(pd.Grouper(key='createdat', freq='D'), as_index = True).count()['username']    
    
    if not grouped.empty:        
                
           data.append(
                 dict(
                     type='scatter',
                     mode='lines',
                     x= grouped.index.tolist(),#group.copy().groupby(['time'], as_index = False).count()['time'],
                     y= grouped,#group.copy().groupby(['time'], as_index = False).count()['index'],
                     name= 'number users tweeting',
                     line = dict(
                         width = 2,
                         dash = 'solid')
                         )
             )
        
    return go.Figure(data=data, layout=layout_lines)

@app.callback(
Output('line-graph-twitteruser2', 'figure'),
[Input('a-slider', 'value')])
def update_line_graph2(slider):
    
    tmp = df.copy()
                
    tmp = tmp[tmp['createdat'].astype(int) >= slider[0]]
    tmp = tmp[tmp['createdat'].astype(int) <= slider[1]]
    
    data = []    
    
    
    tmp['createdat'] = pd.to_datetime(tmp['createdat'])
    grouped = tmp.groupby(pd.Grouper(key='createdat', freq='D'), as_index = True).count()['tweetid']    
    
    if not grouped.empty:        
                
           data.append(
                 dict(
                     type='scatter',
                     mode='lines',
                     x= grouped.index.tolist(),#group.copy().groupby(['time'], as_index = False).count()['time'],
                     y= grouped,#group.copy().groupby(['time'], as_index = False).count()['index'],
                     name= 'number tweets',
                     line = dict(
                         width = 2,
                         dash = 'solid')
                         )
             )
        
    return go.Figure(data=data, layout=layout_lines)        

def create_unique_color_int(tag, hue_step=0.0000000001):

    h, v, = (tag * hue_step) % 1, 1. - (int(tag * hue_step) % 4) / 5.
    r, g, b = colorsys.hsv_to_rgb(h, 1., v)

    return 'rgba(' + str(int(255 * r)) + ',' + str(int(255 * g)) + ',' + str(int(255 * b))+ ',1)'