import dash_html_components as html
import dash_core_components as dcc
from app import app

def Header():
    return html.Div([
        get_header(),
        html.Br([])
    ])

def get_header():
    logo = html.Div([        
        get_menu(),
        html.Div([
            html.Img(src=app.get_asset_url('logo.jpg'), width='141')
        ], className="one columns padded"),

    ], className="row gs-header")
    
    return logo

def get_menu():
                
    menu = html.Div([

        dcc.Link('Tracks   |', href='/', className="tab first"),

 #       dcc.Link('Twitter   |', href='/twitter', className="tab"),

        dcc.Link('Pyramics   |', href='/pyramics', className="tab"),

        dcc.Link('Weather   ', href='/weather', className="tab"),

    ], className="eleven columns padded")
    return menu