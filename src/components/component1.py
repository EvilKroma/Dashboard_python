from dash import html, dcc

# Mise en place de la map interactive des stations-service
def get_map_component():
    """Composant carte interactive des stations-service"""
    return html.Div([
        html.H3("Localisation des stations", 
            style={
                'color': '#2c3e50',
                'marginBottom': '15px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        dcc.Graph(id='stations-map', style={'height': '500px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'margin': '20px 0',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })