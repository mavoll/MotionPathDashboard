import dash_table as dt
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import colorsys
import pandas as pd
import geopandas as gpd
from plotly import graph_objs as go

from app import app


classes = ['', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
            'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
            'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
            'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
            'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
            'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
            'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
            'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
            'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
            'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
            'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
            'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
            'scissors', 'teddy bear', 'hair drier', 'toothbrush']

sql = "SELECT cam, day, slice, part, subpart, track_id, time, track_class, geom FROM tracks_points_per_sec"
df = gpd.GeoDataFrame.from_postgis(sql, app.db.connection, geom_col='geom' )
df = df.to_crs('epsg:4326')
df['lon'] = df['geom'].y
df['lat'] = df['geom'].x
df['track_class_name'] = [classes[classs] for classs in df['track_class'].astype(int)]
del df['geom']
#df['time'] = pd.to_datetime(df['time'])
df['index'] = df.index
df.sort_values(['time','index'])
#df.set_index(['time', 'index'], inplace=True)
#df.sort_index(inplace=True)

#Slider
seconds = list(set(df['time'].astype(int)))
seconds.sort()

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
            lon=9.997399,
            lat=53.549517
        ),
        zoom=16.8,
    )
)

layout_pies = dict(
    
    title='Num tracks per cam or slice',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=700,
    
)

layout_pies2 = dict(
    
    title='Num tracks per track_class or day',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=700,
    
)

layout_lines = dict(
    
    title='Number tracks per class over time',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=300,
    
)

layout = html.Div(
    html.Div([
        html.Div(id='page-1-content'),
        dcc.Link('Raw data | ', href='/'),
        dcc.Link('Animation | ', href='/animation'),
        dcc.Link('Statistics | ', href='/statistics'),
        dcc.Link('Indicators', href='/indicators'),
        html.Div(
            [
                html.H1(children='SmartSquare - Movement Raw Data',
                        className='nine columns')
                
            ], className="row"
        ),    
        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                                id = 'cam',
                                options=[
                                    {'label': 'DesignOffices', 'value': 'designOffices'},
                                    {'label': 'Kirchvorplatz', 'value': 'kirchvorplatz'},
                                    {'label': 'KreuzungDomplatz', 'value': 'kreuzungDomplatz'}
                                ],
                                value=['designOffices', 'kirchvorplatz', 'kreuzungDomplatz'],
                                multi=True
                        ),
                    ],
                    className='six columns'
                ),                
            ],
        ),
        
        # Selectors
        html.Div(
            [                
                html.Div(
                    [
                        dcc.Dropdown(
                            id='track_class',
                            options= [{'label': classes[int(item)],'value': int(item)}
                                        for item in set(df['track_class'].astype(int))],
                            multi=True,
                            value=[1,2,3,4,6,8]#list(set(df['track_class'].astype(int)))
                        )
                    ],
                    className='six columns',
                )
            ],
            className='row'
        ),
        # Selectors
        html.Div(
            [                
                html.Div(
                    [
                        dcc.Dropdown(
                            id='day',
                            options= [{'label': item,'value': item}
                                        for item in set(df['day'])],
                            multi=True,
                            value=list(set(df['day']))
                        )
                    ],
                    className='six columns',
                )
            ],
        ),
        # Selectors
        html.Div(
            [                
                html.Div(
                    [
                        dcc.Dropdown(
                            id='slice',
                            options= [{'label': item,'value': item}
                                        for item in set(df['slice'])],
                            multi=True,
                            value=list(set(df['slice']))
                        )
                    ],
                    className='six columns',
                )
            ],
            className='row'
        ),
        html.Br(),
        html.Div([
				dcc.RangeSlider(
					id='slider',
					min=min(seconds),
					max=max(seconds),
                    step=60000000000,
                    updatemode='mouseup', #'drag' 
                    pushable=True,
					value=[min(seconds) , max(seconds)],
					marks={int(timestamp): datetime.fromtimestamp(timestamp/1000000000) for timestamp in seconds[::60]},
				),
			], className='twelve columns'),
        html.Br(),
        html.Br(),
        html.Div([
				dcc.Slider(
					id='slider2',
					min=min(seconds),
					max=max(seconds),
					value=min(seconds),
					marks={int(timestamp): str(i) + 'min' for i, timestamp in enumerate(seconds[::60])},
                    step=1,
                    disabled=False,
                    updatemode='drag', #'drag'
				),
			], className='twelve columns'),
        html.Br(),
        html.Br(),
        html.Br(),
        # Map + table + Histogram
        html.Div(
            [
                html.Div([
                    dcc.Graph(
                        id='bar-graph',
                    )
                ], className= 'three columns'
                ),
                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True)
                    ], className = "six columns"
                ),
                html.Div([
                    dcc.Graph(
                        id='bar-graph2',
                    )
                ], className= 'three columns'
                ),
                html.Div([
                    dcc.Graph(
                        id="line-graph")]
                    , className="twelve columns"
                    ),
                html.Div(
                    [
                        dt.DataTable(
                            id='datatable',
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.to_dict(orient='records'),
                            selected_rows=[],#list(df['index'].astype(int)) ,#[],
                            editable=False,
                            filtering=True,
                            sorting=True,
                            sorting_type="multi",
                            style_cell={'padding': '5px'},
                            style_table={
                                
                                'maxHeight': '700px',
                                'border': 'thin lightgrey solid',
                                'margin-top': 0
                            },
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['cam', 'time','track_id','track_class']
                            ] + [
                                                        {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                }
                            ] + [
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Date', 'Region']
                            ],
                        
                            style_as_list_view=True,
                            pagination_mode='fe',
                                pagination_settings={
                                    "displayed_pages": 1,
                                    "current_page": 0,
                                    "page_size": 18,
                                },
                                navigation="page",
                            ),
                    ],
                    className="twelve columns"
                ),                
                html.Div(
                    [
                        html.P('Developed by Marc-André Vollstedt - ', style = {'display': 'inline'}),
                        html.A('marc.vollstedt@gmail.com', href = 'mailto:marc.vollstedt@gmail.com')
                    ], className = "twelve columns",
                       style = {'fontSize': 18, 'padding-top': 20}
                )
            ], className="row"
        )
   ], className='ten columns offset-by-one'))

@app.callback(
Output('datatable', 'data'),
[Input('track_class', 'value'),
 Input('cam', 'value'),
 Input('day', 'value'),
 Input('slice', 'value'),
 Input('slider', 'value'),
 Input('slider2', 'value')])
def update_dataframe(track_class, cam, day, slice, slider, slider2):
                    
    tmp = df.copy()
    if min(tmp['time'].astype(int)) < int(slider2 / 1000000000) * 1000000000:
        tmp = tmp[tmp['time'].astype(int) == int(slider2 / 1000000000) * 1000000000]
    tmp = tmp[tmp['time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['time'].astype(int) <= slider[1]]        
    tmp = tmp[tmp['day'].isin(day)]    
    tmp = tmp[tmp['cam'].isin(cam)] 
    tmp = tmp[tmp['slice'].isin(slice)]
    tmp = tmp[tmp['track_class'].astype(int).isin(track_class)] 
    
    return tmp.to_dict(orient='records')

    
@app.callback(
Output('map-graph', 'figure'),
[Input('datatable', 'data')])
def update_map(data):
    
    aux = pd.DataFrame(data)
    data = []
    
    if not aux.empty:
        
        for class_s in list(set(aux['track_class_name'])):
            tmp = aux[aux['track_class_name'] == class_s]
            data.append(
                        dict(
                                type= 'scattermapbox',
                                lat= list(tmp['lat']),
                                lon= list(tmp['lon']),
                                hoverinfo= "text",
                                hovertext= [["Track ID: {} <br>Track class: {} <br>Time: {}".format(i,j,k)]
                                                for i,j,k in zip(tmp['track_id'], tmp['track_class_name'],tmp['time'])],
                                mode= "markers",
                                name= class_s,
                                marker= dict(
                                    color= create_unique_color_int(int(hash(class_s))),
                                    size= 6,
                                    opacity= 0.7,
                                )
                            )
                        )
        
        return dict(data= data, layout= layout_map)
            

@app.callback(
Output('bar-graph', 'figure'),
[Input('datatable', 'data')])
def update_bar_graph(data):
    dff = pd.DataFrame(data)    
    
    if not dff.empty:
        grouped = dff.groupby('cam', as_index = False).count()
        grouped2 = dff.groupby('slice', as_index = False).count()
        
        data = [
             dict(
                 type='pie',
                 labels= grouped['cam'],
                 values = grouped['index'],
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0, 1],
                    y= [.52, 1]),
                 
                 ),
             dict(
                 type='pie',
                 labels= grouped2['slice'],
                 values = grouped2['index'],
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0, 1],
                    y= [0, .49]),
                 
                 ),
         ]
        
        return go.Figure(data=data, layout=layout_pies)
    
@app.callback(
Output('bar-graph2', 'figure'),
[Input('datatable', 'data')])
def update_bar_graph2(data):
    dff = pd.DataFrame(data)    
    
    if not dff.empty:
        
        grouped = dff.groupby('track_class_name', as_index = False).count()
        grouped2 = dff.groupby('day', as_index = False).count()
        data = [             
             dict(
                 type='pie',
                 labels= grouped['track_class_name'],
                 values = grouped['index'],
                 textinfo = 'label+value+percent',
                 marker=dict(
                         colors= [create_unique_color_int(int(hash(name))) for name in grouped['track_class_name']], #create_unique_color_int(int(hash(grouped['track_class_name']))),
                 ),
                 domain=dict(
                    x= [0, 1],
                    y= [.52, 1]),
                 
                 ),
            dict(
                 type='pie',
                 labels= grouped2['day'],
                 values = grouped2['index'],
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0, 1],
                    y= [0, .49]),
                 
                 ), 
         ]
        
        return go.Figure(data=data, layout=layout_pies2)
    
@app.callback(
Output('line-graph', 'figure'),
[Input('datatable', 'data')])
def update_line_graph(data):
    dff = pd.DataFrame(data)  
    if not dff.empty:
        data = []     
        grouped = dff.groupby(['track_class_name'], as_index = False)
        for name, group in grouped:
           group = group.sort_values(['time'])    
           if not group.empty:
               data.append(
                     dict(
                         type='scatter',
                         mode='lines',
                         x= group.copy().groupby(['time'], as_index = False).count()['time'],
                         y= group.copy().groupby(['time'], as_index = False).count()['index'],
                         name= name, 
                         line = dict(
                             color= create_unique_color_int(int(hash(name))),
                             width = 2,
                             dash = 'dot')
                             )
                 )
        
        return go.Figure(data=data, layout=layout_lines)
    
def create_unique_color_int(tag, hue_step=0.0000000001):

    h, v, = (tag * hue_step) % 1, 1. - (int(tag * hue_step) % 4) / 5.
    r, g, b = colorsys.hsv_to_rgb(h, 1., v)

    return 'rgba(' + str(int(255 * r)) + ',' + str(int(255 * g)) + ',' + str(int(255 * b))+ ',1)'