import dash_table as dt
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
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
    height=500,
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
    
    title='Number tracks per cam / class / day / slice',
    showlegend=True,
    dragmode="select",
    autosize=True,
    height=500, 
    
)
        
# functions
def gen_map(map_data):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    if not map_data.empty:
        return {
            "data": [{
                    "type": "scattermapbox",
                    "lat": list(map_data['lat']),
                    "lon": list(map_data['lon']),
                    "hoverinfo": "text",
                    "hovertext": [["Track ID: {} <br>Track class: {} <br>Time: {}".format(i,j,k)]
                                    for i,j,k in zip(map_data['track_id'], map_data['track_class'],map_data['time'])],
                    "mode": "markers",
                    "name": list(map_data['track_id']),
                    "marker": {
                        "size": 6,
                        "opacity": 0.7
                    }
            }],
            "layout": layout_map
        }

layout = html.Div(
    html.Div([
        html.Div(id='page-1-content'),
        html.Br(),
        dcc.Link('Go to indicators', href='/indicators'),
        html.Br(),
        dcc.Link('Go to statistics', href='/'),
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
                        dcc.Checklist(
                                id = 'cam',
                                options=[
                                    {'label': 'DesignOffices', 'value': 'designOffices'},
                                    {'label': 'Kirchvorplatz', 'value': 'kirchvorplatz'},
                                    {'label': 'KreuzungDomplatz', 'value': 'kreuzungDomplatz'}
                                ],
                                values=['designOffices', 'kirchvorplatz', 'kreuzungDomplatz'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns'
                ),                
            ],
            className='row'
        ),
        
        # Selectors
        html.Div(
            [                
                html.Div(
                    [
                        dcc.Dropdown(
                            id='track_class',
                            options= [{'label': classes[int(item)],'value': int(item)}
                                        for item in set(app.df['track_class'].astype(int))],
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
                                        for item in set(app.df['day'])],
                            multi=True,
                            value=list(set(app.df['day']))
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
                            id='slice',
                            options= [{'label': item,'value': item}
                                        for item in set(app.df['slice'])],
                            multi=True,
                            value=list(set(app.df['slice']))
                        )
                    ],
                    className='six columns',
                )
            ],
            className='row'
        ),    
        # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True)
                    ], className = "six columns"
                ),
                html.Div([
                    dcc.Graph(
                        id='bar-graph',
                    )
                ], className= 'six columns'
                ),
                html.Div(
                    [
                        dt.DataTable(
                            id='datatable',
                            columns=[{"name": i, "id": i} for i in app.df.columns],
                            data=app.df.to_dict("rows"),
                            selected_rows=list(app.df.index.values) ,#[],
                            editable=False,
                            filtering=True,
                            sorting=True,
                            sorting_type="multi",
                            row_selectable='multi',
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
Output('map-graph', 'figure'),
[Input('datatable', 'data'),
 Input('datatable', 'selected_rows')])
def cam_selection(data, selected_rows):
    
    aux = pd.DataFrame(data)
    return gen_map(aux)

@app.callback(
Output('datatable', 'data'),
[Input('track_class', 'value'),
 Input('cam', 'values'),
 Input('datatable', 'selected_rows'),
 Input('day', 'value'),
 Input('slice', 'value')])
def update_selected_row(track_class, cam, selected_rows, day, slice):
    
    map_aux = app.df.copy()    
    map_aux = map_aux[map_aux['track_class'].astype(int).isin(track_class)]
    map_aux = map_aux[map_aux['cam'].isin(cam)]    
    map_aux = map_aux[map_aux['index'].isin(selected_rows)]
    map_aux = map_aux[map_aux['day'].isin(day)]
    map_aux = map_aux[map_aux['slice'].isin(slice)]
    
    data = map_aux.to_dict("rows")
    return data

@app.callback(
Output('bar-graph', 'figure'),
[Input('datatable', 'data'),
 Input('datatable', 'selected_rows')])
def update_figure(data, selected_rows):
    dff = pd.DataFrame(data)    
    
    if not dff.empty:
        data = go.Data([
             go.Pie(
                 labels= dff.groupby('cam', as_index = False).count()['cam'],
                 values = dff.groupby('cam', as_index = False).count()['track_id'],
                 domain=dict(
                    x= [0, .48],
                    y= [.52, 1]),
                 
                 ),
             go.Pie(
                 labels= dff.groupby('track_class', as_index = False).count()['track_class'],
                 values = dff.groupby('track_class', as_index = False).count()['index'],
                 domain=dict(
                    x= [.52, 1],
                    y= [.52, 1]),
                 
                 ),
            go.Pie(
                 labels= dff.groupby('day', as_index = False).count()['day'],
                 values = dff.groupby('day', as_index = False).count()['index'],
                 domain=dict(
                    x= [0, .48],
                    y= [0, .49]),
                 
                 ),
             go.Pie(
                 labels= dff.groupby('slice', as_index = False).count()['slice'],
                 values = dff.groupby('slice', as_index = False).count()['index'],
                 domain=dict(
                    x= [.52, 1],
                    y= [0, .49]),
                 
                 )    
             ,
         ])
        
        return go.Figure(data=data, layout=layout_pies)