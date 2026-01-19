from dash import html, dcc

def get_price_distribution_component():
    """Composant vrai histogramme de distribution des prix des carburants"""
    return html.Div([
        dcc.Graph(id='price-distribution', style={'height': '400px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'margin': '20px 0',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
