from dash import html, dcc

# Mise en place de la map interactive des stations-service
def get_map_component():
    """Composant carte interactive des stations-service"""
    return html.Div([
        dcc.Graph(id='stations-map', style={'height': '500px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'flex': '1',
        'minWidth': '0'
    })