import dash_html_components as html

def Footer():
    return html.Div(
            [
                    html.P('Developed by Marc-André Vollstedt - ', style = {'display': 'inline'}),
                    html.A('marc.vollstedt@gmail.com', href = 'mailto:marc.vollstedt@gmail.com')
            ], className = "twelve columns",
            style = {'fontSize': 18, 'padding-top': 20}
            )
