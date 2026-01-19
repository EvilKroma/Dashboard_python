from dash import html, dcc

# Graphique : Prix moyen vs Nombre de carburants disponibles
def get_price_vs_fuel_count_component():
    """Composant scatter plot: Prix moyen vs Nombre de carburants"""
    return html.Div([
        html.H3("Prix moyen selon le nombre de carburants disponibles",
            style={
                'color': '#2c3e50',
                'marginBottom': '10px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        dcc.Graph(id='price-vs-fuel-count', style={'height': '400px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'margin': '20px 0',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
