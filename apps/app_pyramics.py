import dash_table as dt
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import colorsys
import pandas as pd
from plotly import graph_objs as go

from components import Header, Footer
from app import app
                                    
indicators_pyramics = {'id': 'id', 'measurement': 'measurement', 'sensor': 'sensor', 'name': 'name', 
              'type': 'type', 'start_time': 'start_time', 'end_time': 'end_time', 
              'age': 'age', 'dwell': 'dwell', 'gender': 'gender', 'views': 'views'}

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

layout_lines = dict(
    
    showlegend=True,
    dragmode="select",
    autosize=True,
    height=600,
    
)

def layout(): 
    return html.Div(
        html.Div([
            html.Div(id='page-pyramics-content'),
            Header(),
            html.Div(
                [
                    html.H2(children='Pyramics',
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
    					#marks={int(timestamp): datetime.fromtimestamp(timestamp/1000000000) for timestamp in days[::30]},
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
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'pyramics_name',
                                            options=[
                                                {'label': 'Backhus', 'value': 'Backhus'},
                                                {'label': 'Bürgerstiftung', 'value': 'Bürgerstiftung'}
                                            ],
                                            value=['Backhus', 'Bürgerstiftung'],
                                            multi=True
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'pyramics',
                                            options=[
                                                {'label': 'Count iteractions', 'value': 'interactions'},
                                                {'label': 'Sum views', 'value': 'views'},
                                                {'label': 'Sum dwell', 'value': 'dwell'}
                                            ],
                                            value='views',
                                            multi=False
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'intervall',
                                            options=[
                                                {'label': '1 hour intervall', 'value': 'H'},
                                                {'label': '1 day intervall', 'value': 'D'},
                                                {'label': '1 week intervall', 'value': 'W'},
                                                {'label': '1 month intervall', 'value': 'M'},
                                                {'label': 'else', 'value': 'WO'}
                                            ],
                                            value='D',
                                            multi=False
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),
                    html.Div([
                        dcc.Graph(
                            id="pyramics-line-graph")]
                        , className="twelve columns"
                    ),
                    html.Div([
                        dcc.Graph(
                            id="pyramics-line-graph2")]
                        , className="twelve columns"
                    ),
                    html.Div([
                        dcc.Graph(
                            id="pyramics-line-graph3")]
                        , className="twelve columns"
                    ),
                    html.Div(
                        [
                            html.H4(children='Pyramics data table:',
                                    style={
                                        'textAlign': 'center'
                                    },
                                    className='twelve columns')
                            
                        ], className="row"
                    ),
                    html.Div(
                        [
                            dt.DataTable(
                                id='pyramics-datatable',
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
Output('pyramics-datatable', 'data'),
[Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('pyramics-datatable', 'selected_rows')])
def update_dataframe_pyramics(slider, pyramics_name, selected_rows):
                    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]
    
    if len(selected_rows) > 0:
        tmp = tmp[tmp['index'].astype(int).isin(selected_rows)]        
    
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
        
    return tmp.to_dict(orient='records')
  
@app.callback(
Output('pyramics-line-graph', 'figure'),
[Input('pyramics', 'value'),
 Input('intervall', 'value'),
 Input('pyramics-datatable', 'data')])
def update_line_graph_pyramics(pyramics, intervall,  data):
    
    aux = pd.DataFrame(data)
    data = []
    
    
    grouped = aux.groupby(['name'], as_index = False)    
    for name, group in grouped:
       group = group.sort_values(['start_time'])    
       if not group.empty:
           group['start_time'] = pd.to_datetime(group['start_time'])
           if pyramics == 'interactions':
               group_count = group.groupby(pd.Grouper(key='start_time', freq=intervall), as_index = True).count()['id']
           elif pyramics == 'views':
               group_count = group.groupby(pd.Grouper(key='start_time', freq=intervall), as_index = True).sum()['views']
           else:
               group_count = group.groupby(pd.Grouper(key='start_time', freq=intervall), as_index = True).sum()['dwell']
        
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
Output('pyramics-line-graph2', 'figure'),
[Input('pyramics', 'value'),
 Input('intervall', 'value'),
 Input('pyramics-datatable', 'data')])
def update_line_graph_2_pyramics(pyramics, intervall,  data):
    
    aux = pd.DataFrame(data)
    data = []
    
    
    grouped = aux.groupby(['name'], as_index = False)    
    for name, group in grouped:
       group = group.sort_values(['start_time'])    
       if not group.empty:
           group['start_time'] = pd.to_datetime(group['start_time'])
           grouped2 = group.groupby(pd.Grouper(key='start_time', freq='W'), as_index = False)
           for name2, group2 in grouped2: 
               if not group2.empty:
                   cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']   
                   group_count = group2.groupby(group['start_time'].dt.weekday_name, as_index = True).count()['id'].reindex(cats) 
                   data.append(
                         dict(
                             type='scatter',
                             mode='lines',
                             x= group_count.index.tolist(),#group.copy().groupby(['time'], as_index = False).count()['time'],
                             y= group_count,#group.copy().groupby(['time'], as_index = False).count()['index'],
                             name= str(pd.to_datetime(name2).isocalendar()[1]), 
                             line = dict(
                                 color= create_unique_color_int(int(hash(str(name2)))),
                                 width = 2,
                                 dash = 'dot')
                                 )
                     )
        
    return go.Figure(data=data, layout=layout_lines)

@app.callback(
Output('pyramics-line-graph3', 'figure'),
[Input('pyramics', 'value'),
 Input('intervall', 'value'),
 Input('pyramics-datatable', 'data')])
def update_line_graph_3_pyramics(pyramics, intervall,  data):
    
    aux = pd.DataFrame(data)
    data = []
    
    grouped = aux.groupby(['name'], as_index = False)    
    for name, group in grouped:
       group = group.sort_values(['start_time'])    
       if not group.empty:
           group['start_time'] = pd.to_datetime(group['start_time'])
           grouped2 = group.groupby(pd.Grouper(key='start_time', freq='D'), as_index = False)
           for name2, group2 in grouped2: 
               if not group2.empty:
                   group_count = group2.groupby(group['start_time'].dt.hour, as_index = True).count()['id'] 
                   data.append(
                         dict(
                             type='scatter',
                             mode='lines',
                             x= group_count.index.tolist(),#group.copy().groupby(['time'], as_index = False).count()['time'],
                             y= group_count,#group.copy().groupby(['time'], as_index = False).count()['index'],
                             name= str(name2), 
                             line = dict(
                                 color= create_unique_color_int(int(hash(str(name2)))),
                                 width = 2,
                                 dash = 'dot')
                                 )
                     )
        
    return go.Figure(data=data, layout=layout_lines)

def create_unique_color_int(tag, hue_step=0.0000000001):

    h, v, = (tag * hue_step) % 1, 1. - (int(tag * hue_step) % 4) / 5.
    r, g, b = colorsys.hsv_to_rgb(h, 1., v)

    return 'rgba(' + str(int(255 * r)) + ',' + str(int(255 * g)) + ',' + str(int(255 * b))+ ',1)'