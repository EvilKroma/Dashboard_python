from dash import html, dcc

def get_top_stations_component():
    """Composant graphique top 5 des stations avec filtre prix et carburant"""
    return html.Div([
        html.Div([
            # Filtre cher/pas cher
            html.Div([
                html.Label("Afficher:", 
                    style={
                        'fontWeight': 'bold',
                        'marginRight': '10px',
                        'color': '#2c3e50',
                        'fontSize': '14px'
                    }
                ),
                dcc.RadioItems(
                    id='top-stations-filter',
                    options=[
                        {'label': ' Prix moyens les plus chers', 'value': 'expensive'},
                        {'label': ' Prix moyens les plus bas', 'value': 'cheap'}
                    ],
                    value='expensive',
                    inline=True,
                    style={
                        'display': 'flex',
                        'gap': '30px'
                    },
                    labelStyle={
                        'marginRight': '20px',
                        'cursor': 'pointer',
                        'fontSize': '14px'
                    }
                )
            ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
            
            # Filtre carburant
            html.Div([
                html.Label("Carburant:", 
                    style={
                        'fontWeight': 'bold',
                        'marginRight': '10px',
                        'color': '#2c3e50',
                        'fontSize': '14px'
                    }
                ),
                dcc.Dropdown(
                    id='top-stations-fuel-filter',
                    options=[
                        {'label': 'Prix moyen global', 'value': 'prix_moyen'},
                        {'label': 'Gazole', 'value': 'gazole_prix'},
                        {'label': 'SP95', 'value': 'sp95_prix'},
                        {'label': 'SP98', 'value': 'sp98_prix'},
                        {'label': 'E10', 'value': 'e10_prix'},
                        {'label': 'E85', 'value': 'e85_prix'},
                        {'label': 'GPLc', 'value': 'gplc_prix'}
                    ],
                    value='prix_moyen',
                    clearable=False,
                    style={
                        'width': '200px',
                        'fontSize': '14px'
                    }
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'})
        ], style={
            'marginBottom': '15px',
            'display': 'flex',
            'alignItems': 'center',
            'gap': '40px'
        }),
        
        dcc.Graph(id='top-stations-graph', style={'height': '600px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'margin': '20px 0',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
