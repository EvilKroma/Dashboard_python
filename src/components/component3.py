from dash import html, dcc

def get_price_distribution_component():
    """Composant vrai histogramme de distribution des prix des carburants"""
    return html.Div([
        html.H3("Distribution réelle des prix par carburant",
            style={
                'color': '#2c3e50',
                'marginBottom': '10px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        dcc.Graph(id='price-distribution', style={'height': '400px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'margin': '20px 0',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
