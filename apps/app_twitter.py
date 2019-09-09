import dash_table as dt
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import colorsys
import geopandas as gpd
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
        zoom=10,
    )
)

layout_pies = dict(
    
    title='Num tweets per city and year',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=700,
    
)

layout_pies2 = dict(
    
    title='Num tweets per month and day',
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=700,
    
)

layout_lines = dict(
    
    title='Number tracks per city and hours over time',
    showlegend=False,
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
                    html.H2(children='Twitter',
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
    					marks={day: datetime.fromtimestamp(day/1000000000) for day in days},
    				),
    			], className='twelve columns'),
            html.Br(),
            html.Br(),
            html.Div([
    				dcc.Slider(
    					id='a-slider2',
    					min=days[0],
    					max=days[-1],
    					value=days[0],
    					marks={hour: str(i) + 'days' for i, hour in enumerate(days)},
                        step= 60 * 60 * 1000000000,
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
                            id='a-bar-graph',
                        )
                    ], className= 'three columns'
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='t-map-graph',
                                      animate=True)
                        ], className = "six columns"
                    ),
                    html.Div([
                        dcc.Graph(
                            id='a-bar-graph2',
                        )
                    ], className= 'three columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            id="a-line-graph")]
                        , className="twelve columns"
                    ), 
                    html.Div(
                        [
                            dt.DataTable(
                                id='a-datatable',
                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict(orient='records'),
                                selected_rows=[],#list(df['index'].astype(int)) ,#[],
                                editable=False,
                                filtering=False,
                                sorting=True,
                                row_selectable="multi",
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
                    Footer(),
                ], className="row"
            )
       ], className='ten columns offset-by-one'))
                
@app.callback(
Output('a-datatable', 'data'),
[Input('a-year', 'value'),
 Input('a-month', 'value'),
 Input('a-day', 'value'),
 Input('a-hour', 'value'),
 Input('a-city', 'value'),
 Input('a-slider', 'value'),
 Input('a-slider2', 'value'),
 Input('a-datatable', 'selected_rows')])
def update_a_dataframe(year, month, day, hour, city, slider, slider2, selected_rows):
                    
    tmp = df.copy()
    
#    if len(selected_rows) > 0:
#        tmp = tmp[tmp['index'].astype(int).isin(selected_rows)]

#    if min(tmp['createdat'].astype(int)) < int(slider2 / 1000000000):
#        tmp = tmp[tmp['createdat'].astype(int) == int(slider2 / 1000000000)]
#    
#    tmp = tmp[tmp['createdat'].astype(int) >= slider[0]]
#    tmp = tmp[tmp['createdat'].astype(int) <= slider[1]]                
    print(tmp)
    return tmp.to_dict(orient='records')

    
@app.callback(
Output('a-map-graph', 'figure'),
[Input('a-datatable', 'data')])
def update_a_map(data):
    
    aux = gpd.GeoDataFrame(data)
    data = []
    print(aux)
    
    if not aux.empty:
        
        for city in list(set(aux['city'])):
            tmp = aux[aux['city'] == city]
            data.append(
                        dict(
                                type= 'scattermapbox',
                                lat= list(tmp['geolocationlatitude']),
                                lon= list(tmp['geolocationlongitude']),
                                hoverinfo= tmp['username'],
                                hovertext= [["username: {} <br>createdat: {} <br>tweetid: {}".format(i,j,k)]
                                                for i,j,k in zip(tmp['username'], tmp['createdat'],tmp['tweetid'])],
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
Output('a-bar-graph', 'figure'),
[Input('a-datatable', 'data')])
def update_a_bar_graph(data):
    
    dff = gpd.GeoDataFrame(data)    
    data = []
    
    if not dff.empty:
        grouped = dff.groupby('city', as_index = False).count()
        grouped2 = dff.groupby('year', as_index = False).count()
        
        data = [
             dict(
                 type='pie',
                 labels= grouped['city'],
                 values = grouped['tweetid'],
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0, 1],
                    y= [.52, 1]),
                 
                 ),
             dict(
                 type='pie',
                 labels= grouped2['year'],
                 values = grouped2['tweetid'],
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0, 1],
                    y= [0, .49]),
                 
                 ),
         ]
        
    return go.Figure(data=data, layout=layout_pies)
    
@app.callback(
Output('a-bar-graph2', 'figure'),
[Input('a-datatable', 'data')])
def update_a_bar_graph2(data):
    
    dff = gpd.GeoDataFrame(data)    
    data=[]
    
    if not dff.empty:
        
        grouped = dff.groupby('month', as_index = False).count()
        grouped2 = dff.groupby('day', as_index = False).count()
        data = [             
             dict(
                 type='pie',
                 labels= grouped['month'],
                 values = grouped['tweetid'],
                 textinfo = 'label+value+percent',
                 marker=dict(
                         colors= [create_unique_color_int(int(hash(name))) for name in grouped['month']], #create_unique_color_int(int(hash(grouped['track_class_name']))),
                 ),
                 domain=dict(
                    x= [0, 1],
                    y= [.52, 1]),
                 
                 ),
            dict(
                 type='pie',
                 labels= grouped2['day'],
                 values = grouped2['tweetid'],
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0, 1],
                    y= [0, .49]),
                 
                 ), 
         ]
        
    return go.Figure(data=data, layout=layout_pies2)
    
@app.callback(
Output('a-line-graph', 'figure'),
[Input('a-datatable', 'data')])
def update_a_line_graph(data):
    
    dff = gpd.GeoDataFrame(data)  
    data=[]
    
    
    if not dff.empty:
        grouped = dff.groupby(['city'], as_index = False)
        for name, group in grouped:
           group = group.sort_values(['createdat'])    
           if not group.empty:
               group_count = group.groupby(['createdat'], as_index = False).count()['tweetid']
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

def create_unique_color_int(tag, hue_step=0.0000000001):

    h, v, = (tag * hue_step) % 1, 1. - (int(tag * hue_step) % 4) / 5.
    r, g, b = colorsys.hsv_to_rgb(h, 1., v)

    return 'rgba(' + str(int(255 * r)) + ',' + str(int(255 * g)) + ',' + str(int(255 * b))+ ',1)'