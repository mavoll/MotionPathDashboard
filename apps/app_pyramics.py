from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import colorsys
import pandas as pd
import numpy as np
from datetime import datetime
from plotly import graph_objs as go

from components import Header, Footer
from app import app
                                    
indicators_pyramics = {'id': 'id', 'measurement': 'measurement', 'sensor': 'sensor', 'name': 'name', 
              'type': 'type', 'start_time': 'start_time', 'end_time': 'end_time', 
              'age': 'age', 'dwell': 'dwell', 'gender': 'gender', 'views': 'views'}

df = None
days = None

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

layout_bar = dict(
    
    showlegend=True,
    dragmode="select",
    autosize=True,
    height=600,    
    hovermode= 'closest',
    title= ""
    
)

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

layout_pies = dict(    
    
    showlegend=False,
    dragmode="select",
    autosize=True,
    height=400,
    
)

def layout(): 
    return html.Div([
            html.Div(id='page-pyramics-content'),            
            html.Div(
                [
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
        					marks={int(datetime.timestamp(date)) * 1000000000: date.strftime("%Y-%m-%d") for date in pd.date_range(min(days), max(days)).tolist()[::7]},
        				),
        			], className='twelve columns'),
                html.Br(),
                html.Br(),
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
                html.Br(),
                html.Br(),
                html.Br(),
                dcc.Tabs(id="tabs-pyramics", value='tab-3-pyramics', children=[
                    dcc.Tab(label='Totals and gender', value='tab-3-pyramics', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Interactions and views', value='tab-1-pyramics', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Dwell and age grouping', value='tab-2-pyramics', style=tab_style, selected_style=tab_selected_style)           
                ]),
            html.Div(id='tabs-content-pyramics'),
            Footer()
            
           ], className='ten columns offset-by-one'),
    ])

@app.callback(Output('tabs-content-pyramics', 'children'),
              [Input('tabs-pyramics', 'value')])
def render_content(tab):
    if tab == 'tab-1-pyramics':
        return html.Div([            
            
            # Map + table + Histogram
            html.Div(
                [ 
                     html.Div(
                        [
                            html.Br(),
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'gender3',
                                            options=[
                                                {'label': 'Male, Female and N/A', 'value': 'all'},
                                                {'label': 'Male and Female', 'value': 'malefemale'},
                                                {'label': 'Female', 'value': 'female'},
                                                {'label': 'Male', 'value': 'male'}
                                            ],
                                            value='all',
                                            multi=False
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),
                    html.Div(
                        [
                            html.Br(),
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
                    html.Div(
                        [
                            html.H5(children='Time series',
                                    style={
                                        'textAlign': 'center'
                                    },
                                    className='twelve columns')
                            
                        ], className="row"
                    ),
                    html.Div([
                        dcc.Graph(
                            id="pyramics-line-graph")]
                        , className="twelve columns"
                    ),
                    html.Div(
                        [
                            html.H5(children='Week days per calender week',
                                    style={
                                        'textAlign': 'center'
                                    },
                                    className='twelve columns')
                            
                        ], className="row"
                    ),
                    html.Div([
                        dcc.Graph(
                            id="pyramics-line-graph2")]
                        , className="twelve columns"
                    ),
                    html.Div(
                        [
                            html.H5(children='Hours of day per days',
                                    style={
                                        'textAlign': 'center'
                                    },
                                    className='twelve columns')
                            
                        ], className="row"
                    ),
                    html.Div([
                        dcc.Graph(
                            id="pyramics-line-graph3")]
                        , className="twelve columns"
                    ),
                ], className="row"
            )
       ], className='ten columns offset-by-one')
                        
    elif tab == 'tab-2-pyramics':
        return html.Div([            
            
            # Map + table + Histogram
            html.Div(
                [ 
                     html.Div(
                        [
                            html.Br(),
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'gender2',
                                            options=[
                                                {'label': 'Male', 'value': 'male'},
                                                {'label': 'Female', 'value': 'female'}
                                            ],
                                            value=['male','female'],
                                            multi=True
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),
                    html.Div(
                        [
                            html.Br(),                            
                            html.Div(
                                [
                                    html.H5(children='Age',
                                            style={
                                                'textAlign': 'center'
                                            },
                                            className='twelve columns')
                                    
                                ], className="row"
                            ),
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'age-intervall',
                                            options=[
                                                {'label': '1 year intervals', 'value': '1'},
                                                {'label': '5 years intervals', 'value': '5'},
                                                {'label': '10 years intervals', 'value': '10'},
                                                {'label': '15 years intervals', 'value': '15'},
                                                {'label': '20 years intervals', 'value': '20'},
                                                {'label': '25 years intervals', 'value': '25'}
                                            ],
                                            value='1',
                                            multi=False
                                    ),
                                ],
                                className='twelve columns'
                            ),
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'rel',
                                            options=[
                                                {'label': 'Absolute', 'value': 'abs'},
                                                {'label': 'Relative', 'value': 'rel'}
                                            ],
                                            value='abs',
                                            multi=False
                                    ),
                                ],
                                className='twelve columns'
                            ),
                            html.Div([
                                dcc.Graph(
                                    id="pyramics-bar-graph-age")]
                                , className="twelve columns"
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(children='Dwell',
                                            style={
                                                'textAlign': 'center'
                                            },
                                            className='twelve columns')
                                    
                                ], className="row"
                            ),
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'dwell-intervals',
                                            options=[
                                                {'label': '50 ms intervals', 'value': '50'},
                                                {'label': '100 ms intervals', 'value': '100'},
                                                {'label': '150 ms intervals', 'value': '150'},
                                                {'label': '200 ms intervals', 'value': '200'},
                                                {'label': '250 ms intervals', 'value': '250'},
                                                {'label': '300 ms intervals', 'value': '300'},
                                                {'label': '350 ms intervals', 'value': '350'},
                                                {'label': '400 ms intervals', 'value': '400'},
                                                {'label': '450 ms intervals', 'value': '450'},
                                                {'label': '500 ms intervals', 'value': '500'},
                                                {'label': '550 ms intervals', 'value': '550'},
                                                {'label': '600 ms intervals', 'value': '600'},
                                                {'label': '650 ms intervals', 'value': '650'},
                                                {'label': '700 ms intervals', 'value': '700'},
                                                {'label': '750 ms intervals', 'value': '750'},
                                                {'label': '800 ms intervals', 'value': '800'},
                                                {'label': '850 ms intervals', 'value': '850'},
                                                {'label': '900 ms intervals', 'value': '900'},
                                                {'label': '950 ms intervals', 'value': '950'},
                                                {'label': '1000 ms intervals', 'value': '1000'}
                                            ],
                                            value='100',
                                            multi=False
                                    ),
                                ],
                                className='twelve columns'
                            ),
                            html.Div(
                                [
                                    dcc.Input(
                                            id = 'min-value-dwell',
                                            type='number',
                                            placeholder='min value',
                                            value=1  
                                    ),
                                ],
                                className='six columns'
                            ),
                            html.Div(
                                [
                                    dcc.Input(
                                            id = 'max-value-dwell',
                                            type='number',
                                            placeholder='max value',
                                            value=5000  
                                    ),
                                ],
                                className='six columns'
                            ),
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'rel-dwell',
                                            options=[
                                                {'label': 'Absolute', 'value': 'abs'},
                                                {'label': 'Relative', 'value': 'rel'}
                                            ],
                                            value='abs',
                                            multi=False
                                    ),
                                ],
                                className='twelve columns'
                            ),
                                    
                            html.Div([
                                dcc.Graph(
                                    id="pyramics-bar-graph-dwell-1")]
                                , className="twelve columns"
                            ),
                        ],
                    )                   
                ], className="row"
            )
       ], className='ten columns offset-by-one')
    
    elif tab == 'tab-3-pyramics':
        return html.Div([            
            
            # Map + table + Histogram           
            html.Div(
                        [
                            html.H5(children='Total interactions, views and dwell',
                                    style={
                                        'textAlign': 'center'
                                    },
                                    className='twelve columns')
                            
                        ], className="row"
                    ),
             html.Div(
                        [
                            html.Br(),
                            html.Div(
                                [
                                    dcc.Dropdown(
                                            id = 'gender',
                                            options=[
                                                {'label': 'Male', 'value': 'male'},
                                                {'label': 'Female', 'value': 'female'}
                                            ],
                                            value=['male','female'],
                                            multi=True
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),
            html.Div(
                [                                   
                    
                    html.Div([
                        dcc.Graph(
                            id="pyramics-pie-graph")]
                        , className="twelve columns"
                    ),
                ], className="row"
            ),
            html.Div(
                        [
                            html.H5(children='Total interactions by gender',
                                    style={
                                        'textAlign': 'center'
                                    },
                                    className='twelve columns')
                            
                        ], className="row"
                    ),
            html.Div(
                        [
                            dcc.Dropdown(
                                    id = 'rel-gen',
                                    options=[
                                        {'label': 'Absolute', 'value': 'abs'},
                                        {'label': 'Relative', 'value': 'rel'}
                                    ],
                                    value='abs',
                                    multi=False
                            ),
                        ],
                        className='twelve columns'
                    ),
            html.Div(
                [                                   
                    
                    html.Div([
                        dcc.Graph(
                            id="pyramics-bar-graph")]
                        , className="twelve columns"
                    ),
                ], className="row"
            ),
            html.Div(
                        [
                            html.H5(children='Interactions by gender over time',
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
                                            id = 'intervall-gender',
                                            options=[
                                                {'label': '1 hour intervall', 'value': 'H'},
                                                {'label': '1 day intervall', 'value': 'D'},
                                                {'label': '1 week intervall', 'value': 'W'},
                                                {'label': '1 month intervall', 'value': 'M'}
                                            ],
                                            value='W',
                                            multi=False
                                    ),
                                ],
                                className='twelve columns'
                            ),                
                        ],
                    ),     
            html.Div(
                [                                   
                    
                    html.Div([
                        dcc.Graph(
                            id="pyramics-line-gender-graph")]
                        , className="twelve columns"
                    ),
                ], className="row"
            )
                
       ], className='ten columns offset-by-one')
       
@app.callback(
Output('pyramics-bar-graph-age', 'figure'),
[Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('gender2', 'value'),
 Input('age-intervall', 'value'),
 Input('rel', 'value')])
def update_bar_graph_age(slider, pyramics_name, gender, age_intervall, rel):
    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]  
    tmp = tmp[tmp['gender'].notnull()]
    tmp = tmp[tmp['gender'].str.match("|".join(gender))] 
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
    
    data = []
    f = 1    
    
    if not tmp.empty:
                
        grouped = tmp.groupby(['name'], as_index = True)
        
        for name, group in grouped:
           
           if not group.empty:
               
                if rel == 'rel':
                    f =  group.count()['id']
                group_count = group.groupby(pd.cut(group["age"], np.arange(min(group["age"]), max(group["age"]), float(age_intervall))), as_index = True).count()['id']
            
                data.append(
                             dict(
                                 type='bar',
                                 x= group_count.index.astype(str).values.tolist(),
                                 y= group_count.div(f),
                                 name=name
                                 )
                             )
                                               
        return go.Figure(data=data, layout=layout_bar)
    
@app.callback(
Output('pyramics-bar-graph-dwell-1', 'figure'),
[Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('gender2', 'value'),
 Input('dwell-intervals', 'value'),
 Input('min-value-dwell', 'value'),
 Input('max-value-dwell', 'value'),
 Input('rel-dwell', 'value')])
def update_bar_graph_dwell1(slider, pyramics_name, gender, dwell_intervall, min_value, max_value, rel):
    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]  
    tmp = tmp[tmp['gender'].notnull()]
    tmp = tmp[tmp['gender'].str.match("|".join(gender))] 
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
    
    data = []
    f = 1    
    
    if not tmp.empty:
                
        grouped = tmp.groupby(['name'], as_index = True)
        
        for name, group in grouped:
           
           if not group.empty:
               
                if rel == 'rel':
                    f =  group.count()['id']
                group_count = group.groupby(pd.cut(group["dwell"], np.arange(int(min_value), int(max_value), float(dwell_intervall))), as_index = True).count()['id']
            
                data.append(
                             dict(
                                 type='bar',
                                 x= group_count.index.astype(str).values.tolist(),
                                 y= group_count.div(f),
                                 name=name
                                 )
                             )
                                               
        return go.Figure(data=data, layout=layout_bar)
          
@app.callback(
Output('pyramics-pie-graph', 'figure'),
[Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('gender', 'value')])
def update_pie_graph_pyramics(slider, pyramics_name, gender):
    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]
    tmp = tmp[tmp['gender'].notnull()]
    tmp = tmp[tmp['gender'].str.match("|".join(gender))] 
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
    
    data = []
    
    
    
    if not tmp.empty:
                
        grouped = tmp.groupby('name', as_index = True).count()['id']
        grouped2 = tmp.groupby('name', as_index = True).sum()['views']
        grouped3 = tmp.groupby('name', as_index = True).sum()['dwell']
        
        data = [
             dict(
                 type='pie',
                 labels= grouped.index.to_list(),
                 values = grouped,
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0, 0.32],
                    y= [0, 1]),
                 
                 ),
             dict(
                 type='pie',
                 labels= grouped2.index.to_list(),
                 values = grouped2,
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0.33, 0.65],
                    y= [0, 1]),
                 
                 ),
            dict(
                 type='pie',
                 labels= grouped3.index.to_list(),
                 values = grouped3,
                 textinfo = 'label+value+percent',
                 domain=dict(
                    x= [0.66, 1],
                    y= [0, 1]),
                 
                 ),
         ]
                            
    return go.Figure(data=data, layout=layout_pies)

@app.callback(
Output('pyramics-bar-graph', 'figure'),
[Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('gender', 'value'),
 Input('rel-gen', 'value')])
def update_bar_graph_pyramics(slider, pyramics_name, gender, rel_gen):
    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]  
    tmp = tmp[tmp['gender'].notnull()]
    tmp = tmp[tmp['gender'].str.match("|".join(gender))] 
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
    
    data = []
    f = 1
        
    if not tmp.empty:
                
        grouped = tmp.groupby(['name'], as_index = True)
        
        
        for name, group in grouped:
           
           if not group.empty:
                if rel_gen == 'rel':
                    f =  group.count()['id']
                group_count = group.groupby(['gender'], as_index = True).count()['id']
            
                data.append(
                             dict(
                                 type='bar',
                                 x= group_count.index.to_list(),
                                 y= group_count.div(f),
                                 name=name
                                 )
                             )
                                               
        return go.Figure(data=data, layout=layout_bar)

@app.callback(
Output('pyramics-line-gender-graph', 'figure'),
[Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('gender', 'value'),
 Input('intervall-gender', 'value')])
def update_line_gender_graph_pyramics(slider, pyramics_name, gender, intervall):
    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]    
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
    
    data = []
    
    
    
    grouped = tmp.groupby(['name'], as_index = False)    
    for name, group in grouped:        
       group = group.sort_values(['start_time']) 
       if not group.empty:           
           group['start_time'] = pd.to_datetime(group['start_time'])
           grouped2 = group.groupby(['gender'], as_index = False) 
           for name2, group2 in grouped2:   
               if not group2.empty:         
                   group_count = group2.groupby(pd.Grouper(key='start_time', freq=intervall), as_index = True).count()['id']
                
                   data.append(
                         dict(
                             type='scatter',
                             mode='lines',
                             x= group_count.index.tolist(),#group.copy().groupby(['time'], as_index = False).count()['time'],
                             y= group_count,#group.copy().groupby(['time'], as_index = False).count()['index'],
                             name= name + ' ' + name2, 
                             line = dict(
                                 color= create_unique_color_int(int(hash(name+name2))),
                                 width = 2,
                                 dash = 'solid')
                                 )
                     )
        
    return go.Figure(data=data, layout=layout_lines)

@app.callback(
Output('pyramics-line-graph', 'figure'),
[Input('pyramics', 'value'),
 Input('intervall', 'value'),
 Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('gender3', 'value')])
def update_line_graph_pyramics(pyramics, intervall,  slider, pyramics_name, gender):
    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]
    
    if gender == 'male' or gender == 'female':         
        tmp = tmp[tmp['gender'].notnull()]
        tmp = tmp[tmp['gender'].str.match(gender)]
    elif gender == 'malefemale':         
        tmp = tmp[tmp['gender'].notnull()]
        tmp = tmp[tmp['gender'].str.match("|".join(['male', 'female']))]
        
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
    
    data = []
    
    
    grouped = tmp.groupby(['name'], as_index = False)    
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
                         dash = 'solid')
                         )
             )
        
    return go.Figure(data=data, layout=layout_lines)

@app.callback(
Output('pyramics-line-graph2', 'figure'),
[Input('pyramics', 'value'),
 Input('intervall', 'value'),
 Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('gender3', 'value')])
def update_line_graph_2_pyramics(pyramics, intervall,  slider, pyramics_name, gender):
    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]    
    if gender == 'male' or gender == 'female':         
        tmp = tmp[tmp['gender'].notnull()]
        tmp = tmp[tmp['gender'].str.match(gender)]
    elif gender == 'malefemale':         
        tmp = tmp[tmp['gender'].notnull()]
        tmp = tmp[tmp['gender'].str.match("|".join(['male', 'female']))]
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
    
    data = []    
    
    grouped = tmp.groupby(['name'], as_index = False)    
    for name, group in grouped:
       group = group.sort_values(['start_time'])    
       if not group.empty:
           group['start_time'] = pd.to_datetime(group['start_time'])
           grouped2 = group.groupby(pd.Grouper(key='start_time', freq='W'), as_index = False)
           for name2, group2 in grouped2: 
               if not group2.empty:
                   cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                   
                   if pyramics == 'interactions':
                       group_count = group2.groupby(group['start_time'].dt.weekday_name, as_index = True).count()['id'].reindex(cats)
                   elif pyramics == 'views':
                       group_count = group2.groupby(group['start_time'].dt.weekday_name, as_index = True).sum()['views'].reindex(cats)
                   else:
                       group_count = group2.groupby(group['start_time'].dt.weekday_name, as_index = True).sum()['dwell'].reindex(cats)
                       
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
 Input('slider', 'value'),
 Input('pyramics_name', 'value'),
 Input('gender3', 'value')])
def update_line_graph_3_pyramics(pyramics, intervall,  slider, pyramics_name, gender):
    
    tmp = df.copy()
    
    tmp = tmp[tmp['name'].str.match("|".join(pyramics_name))]    
    if gender == 'male' or gender == 'female':         
        tmp = tmp[tmp['gender'].notnull()]
        tmp = tmp[tmp['gender'].str.match(gender)]
    elif gender == 'malefemale':         
        tmp = tmp[tmp['gender'].notnull()]
        tmp = tmp[tmp['gender'].str.match("|".join(['male', 'female']))]
    tmp = tmp[tmp['start_time'].astype(int) >= slider[0]]
    tmp = tmp[tmp['start_time'].astype(int) <= slider[1]]
    
    data = []    
    
    grouped = tmp.groupby(['name'], as_index = False)    
    for name, group in grouped:
       group = group.sort_values(['start_time'])    
       if not group.empty:
           group['start_time'] = pd.to_datetime(group['start_time'])
           grouped2 = group.groupby(pd.Grouper(key='start_time', freq='D'), as_index = False)
           for name2, group2 in grouped2: 
               if not group2.empty:
                   if pyramics == 'interactions':
                       group_count = group2.groupby(group['start_time'].dt.hour, as_index = True).count()['id']
                   elif pyramics == 'views':
                       group_count = group2.groupby(group['start_time'].dt.hour, as_index = True).sum()['views'] 
                   else:
                       group_count = group2.groupby(group['start_time'].dt.hour, as_index = True).sum()['dwell'] 
                    
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