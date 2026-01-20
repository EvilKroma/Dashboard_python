from dash import html, dcc

# Mise en place de l'histo dynamique des différents carburants
def get_price_histogram_component():
    """Composant histogramme des prix des carburants"""
    return html.Div([
        dcc.Graph(id='price-histogram', style={'height': '700px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'flex': '1',
        'minWidth': '0'
    })