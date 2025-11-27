from dash import html, dcc

def get_price_histogram_component():
    """Composant histogramme des prix des carburants"""
    return html.Div([
        html.H3("Distribution des prix des carburants",
            style={
                'color': '#2c3e50',
                'marginBottom': '10px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        dcc.Graph(id='price-histogram', style={'height': '400px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'margin': '20px 0',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })