from dash import html, dcc

# Graphique : Prix d'un carburant vs Prix moyen de la station
def get_gazole_vs_avg_price_component():
    """Composant scatter plot: Prix d'un carburant vs Prix moyen de la station"""
    return html.Div([
        html.Div([
            html.H3("Prix du carburant vs Prix moyen de la station",
                style={
                    'color': '#2c3e50',
                    'marginBottom': '10px',
                    'fontFamily': 'Arial, sans-serif',
                    'display': 'inline-block',
                    'marginRight': '20px'
                }
            ),
            html.Div([
                html.Label("Sélectionner un carburant:", 
                    style={
                        'fontWeight': 'bold',
                        'marginRight': '10px',
                        'color': '#2c3e50',
                        'fontSize': '14px'
                    }
                ),
                dcc.Dropdown(
                    id='fuel-type-dropdown',
                    options=[
                        {'label': 'Gazole', 'value': 'gazole_prix'},
                        {'label': 'SP95', 'value': 'sp95_prix'},
                        {'label': 'SP98', 'value': 'sp98_prix'},
                        {'label': 'E10', 'value': 'e10_prix'},
                        {'label': 'E85', 'value': 'e85_prix'},
                        {'label': 'GPLc', 'value': 'gplc_prix'}
                    ],
                    value='gazole_prix',
                    clearable=False,
                    style={
                        'width': '200px',
                        'display': 'inline-block',
                        'borderRadius': '5px'
                    }
                ),
            ], style={'display': 'inline-block', 'verticalAlign': 'middle'})
        ], style={'marginBottom': '15px'}),
        
        dcc.Graph(id='gazole-vs-avg-price', style={'height': '400px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'margin': '20px 0',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })

