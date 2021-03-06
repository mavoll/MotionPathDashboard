#import dash_table as dt
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import colorsys
import pandas as pd
from plotly import graph_objs as go

from components import Header, Footer
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

df = None
seconds = None

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
        zoom=17.2,
    )
)

layout_pies = dict(
    
    title='Num points per cam and slice',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=700,
    
)

layout_pies2 = dict(
    
    title='Num points per class and day',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=700,
    
)

layout_lines = dict(
    
    title='Number tracks per class and second over time',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=300,
    
)

layout_lines2 = dict(
    
    title='Average number tracks per class and minute over time',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=300,
    
)

def layout(): 
    return html.Div(
        html.Div([
            html.Div(id='page-motion-content'),
            Header(),
            html.Div(
                [
                    html.H2(children='Tracks',
                            style={
                                'textAlign': 'center'
                            },
                            className='twelve columns')
                    
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
                                        {'label': 'KreuzungDomplatz', 'value': 'kreuzungDomplatz'},
                                        {'label': 'Backhus', 'value': 'backhus'}
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
                        step=1000000000 * 60,
                        updatemode='mouseup', #'drag' 
                        pushable=True,
    					value=[min(seconds) , max(seconds)],
    					marks={min(seconds): datetime.fromtimestamp(min(seconds)/1000000000).strftime("%Y-%m-%d %H:%M") , max(seconds): datetime.fromtimestamp(max(seconds)/1000000000).strftime("%Y-%m-%d %H:%M")},
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
                    html.Div([
                        dcc.Graph(
                            id="line-graph2")]
                        , className="twelve columns"
                    ),
#                    html.Div(
#                        [
#                            dt.DataTable(
#                                id='datatable',
#                                columns=[{"name": i, "id": i} for i in df.columns],
#                                data=df.to_dict(orient='records'),
#                                selected_rows=[],#list(df['index'].astype(int)) ,#[],
#                                editable=False,
#                                filtering=False,
#                                sorting=True,
#                                row_selectable="multi",
#                                sorting_type="multi",
#                                style_cell={'padding': '5px'},
#                                style_table={
#                                    
#                                    'maxHeight': '700px',
#                                    'border': 'thin lightgrey solid',
#                                    'margin-top': 0
#                                },
#                                style_header={
#                                    'backgroundColor': 'white',
#                                    'fontWeight': 'bold'
#                                },
#                                style_cell_conditional=[
#                                    {
#                                        'if': {'column_id': c},
#                                        'textAlign': 'left'
#                                    } for c in ['cam', 'time','track_id','track_class']
#                                ] + [
#                                                            {
#                                        'if': {'row_index': 'odd'},
#                                        'backgroundColor': 'rgb(248, 248, 248)'
#                                    }
#                                ] + [
#                                    {
#                                        'if': {'column_id': c},
#                                        'textAlign': 'left'
#                                    } for c in ['Date', 'Region']
#                                ],
#                            
#                                style_as_list_view=True,
#                                pagination_mode='fe',
#                                    pagination_settings={
#                                        "displayed_pages": 1,
#                                        "current_page": 0,
#                                        "page_size": 18,
#                                    },
#                                    navigation="page",
#                                ),
#                        ],
#                        className="twelve columns"
#                    ),                
                    Footer(),
                ], className="row"
            )
       ], className='ten columns offset-by-one'))

#@app.callback(
#Output('datatable', 'data'),
#[Input('track_class', 'value'),
# Input('cam', 'value'),
# Input('day', 'value'),
# Input('slice', 'value'),
# Input('slider', 'value'),
# Input('datatable', 'selected_rows')])
#def update_dataframe(track_class, cam, day, slice, slider, selected_rows):
#                    
#    tmp = df.copy()
#    
#    if len(selected_rows) > 0:
#        tmp = tmp[tmp['index'].astype(int).isin(selected_rows)]
#            
#    tmp = tmp[tmp['time'].astype(int) >= slider[0]]
#    tmp = tmp[tmp['time'].astype(int) <= slider[1]]
#                
#    tmp = tmp[tmp['day'].isin(day)]    
#    tmp = tmp[tmp['cam'].isin(cam)] 
#    tmp = tmp[tmp['slice'].isin(slice)]
#    tmp = tmp[tmp['track_class'].astype(int).isin(track_class)] 
#    
#    return tmp.to_dict(orient='records')

    
@app.callback(
Output('map-graph', 'figure'),
[Input('track_class', 'value'),
 Input('cam', 'value'),
 Input('day', 'value'),
 Input('slice', 'value'),
 Input('slider', 'value'),
 Input('slider2', 'value')])
def update_map(track_class, cam, day, slice, slider, slider2):
    
    tmp = df.copy()
        
    if min(tmp['time'].astype(int)) < int(slider2 / 1000000000) * 1000000000:
        tmp = tmp[tmp['time'].astype(int) == int(slider2 / 1000000000) * 1000000000]
    
    tmp = tmp[tmp['time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['time'].astype(int) <= slider[1]]
                
    tmp = tmp[tmp['day'].isin(day)]    
    tmp = tmp[tmp['cam'].isin(cam)] 
    tmp = tmp[tmp['slice'].isin(slice)]
    tmp = tmp[tmp['track_class'].astype(int).isin(track_class)] 
    
    data = []
    
    if not tmp.empty:
        
        for class_s in list(set(tmp['track_class_name'])):
            tmp2 = tmp[tmp['track_class_name'] == class_s]
            data.append(
                        dict(
                                type= 'scattermapbox',
                                lat= list(tmp2['lat']),
                                lon= list(tmp2['lon']),
                                hoverinfo= "text",
                                hovertext= [["Track ID: {} <br>Track class: {} <br>Time: {}".format(i,j,k)]
                                                for i,j,k in zip(tmp2['track_id'], tmp2['track_class_name'],tmp2['time'])],
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
[Input('track_class', 'value'),
 Input('cam', 'value'),
 Input('day', 'value'),
 Input('slice', 'value'),
 Input('slider', 'value')])
def update_bar_graph(track_class, cam, day, slice, slider):
    
    tmp = df.copy()
    
            
    tmp = tmp[tmp['time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['time'].astype(int) <= slider[1]]
                
    tmp = tmp[tmp['day'].isin(day)]    
    tmp = tmp[tmp['cam'].isin(cam)] 
    tmp = tmp[tmp['slice'].isin(slice)]
    tmp = tmp[tmp['track_class'].astype(int).isin(track_class)] 
    
    data = []
    
    if not tmp.empty:
        grouped = tmp.groupby('cam', as_index = False).count()
        grouped2 = tmp.groupby('slice', as_index = False).count()
        
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
[Input('track_class', 'value'),
 Input('cam', 'value'),
 Input('day', 'value'),
 Input('slice', 'value'),
 Input('slider', 'value')])
def update_bar_graph2(track_class, cam, day, slice, slider):
    
    tmp = df.copy()
                
    tmp = tmp[tmp['time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['time'].astype(int) <= slider[1]]
                
    tmp = tmp[tmp['day'].isin(day)]    
    tmp = tmp[tmp['cam'].isin(cam)] 
    tmp = tmp[tmp['slice'].isin(slice)]
    tmp = tmp[tmp['track_class'].astype(int).isin(track_class)] 
    
    data = []
    
    if not tmp.empty:
        
        grouped = tmp.groupby('track_class_name', as_index = False).count()
        grouped2 = tmp.groupby('day', as_index = False).count()
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
[Input('track_class', 'value'),
 Input('cam', 'value'),
 Input('day', 'value'),
 Input('slice', 'value'),
 Input('slider', 'value')])
def update_line_graph(track_class, cam, day, slice, slider):
    
    tmp = df.copy()
                
    tmp = tmp[tmp['time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['time'].astype(int) <= slider[1]]
                
    tmp = tmp[tmp['day'].isin(day)]    
    tmp = tmp[tmp['cam'].isin(cam)] 
    tmp = tmp[tmp['slice'].isin(slice)]
    tmp = tmp[tmp['track_class'].astype(int).isin(track_class)] 
    
    data = []    
    
    if not tmp.empty:
        grouped = tmp.groupby(['track_class_name'], as_index = False)
        for name, group in grouped:
           group = group.sort_values(['time'])    
           if not group.empty:
               group_count = group.groupby(['time'], as_index = True).count()['index']
               data.append(
                     dict(
                         type='scatter',
                         mode='lines',
                         x= group_count.index.tolist(),#group.copy().groupby(['time'], as_index = False).count()['time'],
                         y= group_count,#group.copy().groupby(['time'], as_index = False).count()['index'],
                         name= name, 
                         line = dict(
                             color= create_unique_color_int(int(hash(name))),
                             width = 2,
                             dash = 'dot')
                             )
                 )
        
    return go.Figure(data=data, layout=layout_lines)

@app.callback(
Output('line-graph2', 'figure'),
[Input('track_class', 'value'),
 Input('cam', 'value'),
 Input('day', 'value'),
 Input('slice', 'value'),
 Input('slider', 'value')])
def update_line_graph2(track_class, cam, day, slice, slider):
    
    tmp = df.copy()
                    
    tmp = tmp[tmp['time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['time'].astype(int) <= slider[1]]
                
    tmp = tmp[tmp['day'].isin(day)]    
    tmp = tmp[tmp['cam'].isin(cam)] 
    tmp = tmp[tmp['slice'].isin(slice)]
    tmp = tmp[tmp['track_class'].astype(int).isin(track_class)] 
    
    data = []    
    
    if not tmp.empty:
        grouped = tmp.groupby(['track_class_name'], as_index = False)
        for name, group in grouped:
           group = group.sort_values(['minute'])    
           group
           if not group.empty:
               group_count = group.groupby(['minute'], as_index = True).count()['index']
               
               data.append(
                     dict(
                         type='scatter',
                         mode='lines',
                         x= [pd.to_datetime(i) + pd.Timedelta(minutes=1) for i in group_count.index.tolist()],#group_count.index.tolist(),#group.copy().groupby(['time'], as_index = False).count()['time'],
                         y= group_count.div(60),#group.copy().groupby(['time'], as_index = False).count()['index'],
                         name= name, 
                         line = dict(
                             color= create_unique_color_int(int(hash(name))),
                             width = 2,
                             dash = 'dot')
                             )
                 )
        
    return go.Figure(data=data, layout=layout_lines2)

def create_unique_color_int(tag, hue_step=0.0000000001):

    h, v, = (tag * hue_step) % 1, 1. - (int(tag * hue_step) % 4) / 5.
    r, g, b = colorsys.hsv_to_rgb(h, 1., v)

    return 'rgba(' + str(int(255 * r)) + ',' + str(int(255 * g)) + ',' + str(int(255 * b))+ ',1)'