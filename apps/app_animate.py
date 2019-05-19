#import dash_table as dt
#from dash.dependencies import Input, Output
#import dash_core_components as dcc
#import dash_html_components as html
#
#import pandas as pd
#import geopandas as gpd
#from plotly import graph_objs as go
#
#from app import app
#
#
#classes = ['', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
#            'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
#            'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
#            'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
#            'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
#            'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
#            'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
#            'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
#            'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
#            'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
#            'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
#            'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
#            'scissors', 'teddy bear', 'hair drier', 'toothbrush']
#
#sql = "SELECT cam, day, slice, part, subpart, track_id, time, track_class, geom FROM tracks_points_per_sec"
#df = gpd.GeoDataFrame.from_postgis(sql, app.db.connection, geom_col='geom' )
#df = df.to_crs('epsg:4326')
#df['lon'] = df['geom'].y
#df['lat'] = df['geom'].x
##df['time'] = df['time'].astype(str)
#del df['geom']
#df.sort_values(['time'], axis=0, ascending=True, inplace=True)
#df['index'] = df.index.astype(int)
#
##  Layouts
#layout_table = dict(
#    autosize=True,
#    height=700,
#    font=dict(color="#191A1A"),
#    titlefont=dict(color="#191A1A", size='14'),
#    margin=dict(
#        l=35,
#        r=35,
#        b=35,
#        t=45
#    ),
#    hovermode="closest",
#    plot_bgcolor='#fffcfc',
#    paper_bgcolor='#fffcfc',
#    legend=dict(font=dict(size=10), orientation='h'),
#    title='Data table'
#)
#layout_table['font-size'] = '12'
#layout_table['margin-top'] = '20'
#
#layout_map = dict(
#    autosize=True,
#    height=500,
#    font=dict(color="#191A1A"),
#    titlefont=dict(color="#191A1A", size='14'),
#    margin=dict(
#        l=0,
#        r=0,
#        b=0,
#        t=0
#    ),
#    hovermode="closest",
#    plot_bgcolor='#fffcfc',
#    paper_bgcolor='#fffcfc',
#    legend=dict(font=dict(size=10), orientation='h'),
#    mapbox=dict(
#        accesstoken=app.mapbox_access_token,
#        style="light",
#        center=dict(
#            lon=9.997399,
#            lat=53.549517
#        ),
#        zoom=16.8,
#    )
#)
#
#layout_pies = dict(
#    
#    title='Number tracks per cam / class / day / slice',
#    showlegend=True,
#    dragmode="select",
#    autosize=True,
#    height=500,
#    
#)
#
#
#layout = html.Div(
#    html.Div([
#        html.Div(id='page-1-content'),
#        dcc.Link('Go to Home', href='/'),
#        html.Br(),
#        dcc.Link('Go to Animation', href='/animation'),
#        html.Br(),
#        dcc.Link('Go to Statistics', href='/statistics'),
#        html.Br(),
#        dcc.Link('Go to Indicators', href='/indicators'),
#        html.Div(
#            [
#                html.H1(children='SmartSquare - Movement Raw Data',
#                        className='nine columns')
#                
#            ], className="row"
#        ),    
#        # Selectors
#        html.Div(
#            [
#                html.Div(
#                    [
#                        dcc.Checklist(
#                                id = 'cam',
#                                options=[
#                                    {'label': 'DesignOffices', 'value': 'designOffices'},
#                                    {'label': 'Kirchvorplatz', 'value': 'kirchvorplatz'},
#                                    {'label': 'KreuzungDomplatz', 'value': 'kreuzungDomplatz'}
#                                ],
#                                values=['designOffices', 'kirchvorplatz', 'kreuzungDomplatz'],
#                                labelStyle={'display': 'inline-block'}
#                        ),
#                    ],
#                    className='six columns'
#                ),                
#            ],
#            className='row'
#        ),
#        
#        # Selectors
#        html.Div(
#            [                
#                html.Div(
#                    [
#                        dcc.Dropdown(
#                            id='track_class',
#                            options= [{'label': classes[int(item)],'value': int(item)}
#                                        for item in set(df['track_class'].astype(int))],
#                            multi=True,
#                            value=[1,2,3,4,6,8]#list(set(df['track_class'].astype(int)))
#                        )
#                    ],
#                    className='six columns',
#                )
#            ],
#            className='row'
#        ),
#        # Selectors
#        html.Div(
#            [                
#                html.Div(
#                    [
#                        dcc.Dropdown(
#                            id='day',
#                            options= [{'label': item,'value': item}
#                                        for item in set(df['day'])],
#                            multi=True,
#                            value=list(set(df['day']))
#                        )
#                    ],
#                    className='six columns',
#                )
#            ],
#            className='row'
#        ),
#        # Selectors
#        html.Div(
#            [                
#                html.Div(
#                    [
#                        dcc.Dropdown(
#                            id='slice',
#                            options= [{'label': item,'value': item}
#                                        for item in set(df['slice'])],
#                            multi=True,
#                            value=list(set(df['slice']))
#                        )
#                    ],
#                    className='six columns',
#                )
#            ],
#            className='row'
#        ),    
#        # Map + table + Histogram
#        html.Div(
#            [
#                html.Div(
#                    [
#                        dcc.Graph(id='map-graph',
#                                  animate=True)
#                    ], className = "six columns"
#                ),
#                html.Div([
#                    dcc.Graph(
#                        id='bar-graph',
#                    )
#                ], className= 'six columns'
#                ),
#                html.Div(
#                    [
#                        dt.DataTable(
#                            id='datatable',
#                            columns=[{"name": i, "id": i} for i in df.columns],
#                            data=df.to_dict('records'), #.to_dict("rows"),
#                            selected_rows=[],#list(df['index'].astype(int)) ,#[],
#                            editable=False,
#                            filtering=True,
#                            sorting=True,
#                            sorting_type="multi",
#                            style_cell={'padding': '5px'},
#                            style_table={
#                                
#                                'maxHeight': '700px',
#                                'border': 'thin lightgrey solid',
#                                'margin-top': 0
#                            },
#                            style_header={
#                                'backgroundColor': 'white',
#                                'fontWeight': 'bold'
#                            },
#                            style_cell_conditional=[
#                                {
#                                    'if': {'column_id': c},
#                                    'textAlign': 'left'
#                                } for c in ['cam', 'time','track_id','track_class']
#                            ] + [
#                                                        {
#                                    'if': {'row_index': 'odd'},
#                                    'backgroundColor': 'rgb(248, 248, 248)'
#                                }
#                            ] + [
#                                {
#                                    'if': {'column_id': c},
#                                    'textAlign': 'left'
#                                } for c in ['Date', 'Region']
#                            ],
#                        
#                            style_as_list_view=True,
#                            pagination_mode='fe',
#                                pagination_settings={
#                                    "displayed_pages": 1,
#                                    "current_page": 0,
#                                    "page_size": 18,
#                                },
#                                navigation="page",
#                            ),
#                    ],
#                    className="twelve columns"
#                ),                
#                html.Div(
#                    [
#                        html.P('Developed by Marc-André Vollstedt - ', style = {'display': 'inline'}),
#                        html.A('marc.vollstedt@gmail.com', href = 'mailto:marc.vollstedt@gmail.com')
#                    ], className = "twelve columns",
#                       style = {'fontSize': 18, 'padding-top': 20}
#                )
#            ], className="row"
#        )
#   ], className='ten columns offset-by-one'))
#
#@app.callback(
#Output('datatable', 'data'),
#[Input('track_class', 'value'),
# Input('cam', 'values'),
# Input('day', 'value'),
# Input('slice', 'value')])
#def update_dataframe(track_class, cam, day, slice):
#    
#    data = {}
#    
#    map_aux = df.copy()
#    map_aux = map_aux[map_aux['track_class'].astype(int).isin(track_class)]     
#    map_aux = map_aux[map_aux['cam'].isin(cam)]    
#    map_aux = map_aux[map_aux['day'].isin(day)]
#    map_aux = map_aux[map_aux['slice'].isin(slice)]
#    
#    if not map_aux.empty:
#        data = map_aux.to_dict('records') #.to_dict("rows")
#    
#    return data
#
#@app.callback(
#Output('map-graph', 'figure'),
#[Input('datatable', 'data')])
#def update_map(data):
#    
#    aux = pd.DataFrame(data)
#    ret = {}
#    
#    if not aux.empty:
#        ret = {
#            "data": [{
#                    "type": "scattermapbox",
#                    "lat": list(aux['lat']),
#                    "lon": list(aux['lon']),
#                    "hoverinfo": "text",
#                    "hovertext": [["Track ID: {} <br>Track class: {} <br>Time: {}".format(i,j,k)]
#                                    for i,j,k in zip(aux['track_id'], aux['track_class'],aux['time'])],
#                    "mode": "markers",
#                    "name": list(aux['track_id']),
#                    "marker": {
#                        "size": 6,
#                        "opacity": 0.7
#                    }
#            }],
#            "layout": layout_map
#        }
#                    
#    return ret
#
#@app.callback(
#Output('bar-graph', 'figure'),
#[Input('datatable', 'data')])
#def update_figure(data):
#    dff = pd.DataFrame(data)    
#    ret = {}
#    
#    if not dff.empty:
#        data = go.Data([
#             go.Pie(
#                 labels= dff.groupby('cam', as_index = False).count()['cam'],
#                 values = dff.groupby('cam', as_index = False).count()['track_id'],
#                 domain=dict(
#                    x= [0, .48],
#                    y= [.52, 1]),
#                 
#                 ),
#             go.Pie(
#                 labels= dff.groupby('track_class', as_index = False).count()['track_class'],
#                 values = dff.groupby('track_class', as_index = False).count()['index'],
#                 domain=dict(
#                    x= [.52, 1],
#                    y= [.52, 1]),
#                 
#                 ),
#            go.Pie(
#                 labels= dff.groupby('day', as_index = False).count()['day'],
#                 values = dff.groupby('day', as_index = False).count()['index'],
#                 domain=dict(
#                    x= [0, .48],
#                    y= [0, .49]),
#                 
#                 ),
#             go.Pie(
#                 labels= dff.groupby('slice', as_index = False).count()['slice'],
#                 values = dff.groupby('slice', as_index = False).count()['index'],
#                 domain=dict(
#                    x= [.52, 1],
#                    y= [0, .49]),
#                 
#                 )    
#             ,
#         ])
#        
#        ret =  go.Figure(data=data, layout=layout_pies)
#    
#    return ret