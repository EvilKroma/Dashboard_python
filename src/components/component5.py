from dash import html, dcc

def get_top_stations_component():
    """Composant graphique top 5 des stations avec filtre prix et carburant"""
    return html.Div([
        html.Div([
            # Filtre cher/pas cher + dropdown carburant sur la même ligne
            html.Div([
                html.Label("Afficher:", 
                    style={
                        'fontWeight': 'bold',
                        'marginRight': '15px',
                        'color': '#2c3e50',
                        'fontSize': '15px'
                    }
                ),
                dcc.RadioItems(
                    id='top-stations-filter',
                    options=[
                        {'label': ' Prix les plus chers', 'value': 'expensive'},
                        {'label': ' Prix les plus bas', 'value': 'cheap'}
                    ],
                    value='expensive',
                    inline=True,
                    style={
                        'display': 'flex',
                        'gap': '30px'
                    },
                    labelStyle={
                        'display': 'inline-block',
                        'cursor': 'pointer',
                        'fontSize': '14px',
                        'padding': '8px 15px',
                        'borderRadius': '6px',
                        'backgroundColor': '#f0f0f0',
                        'transition': 'all 0.3s',
                        'marginRight': '0px'
                    }
                ),
                
                # Dropdown carburant à côté
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
                        'display': 'inline-block',
                        'borderRadius': '5px',
                        'marginLeft': '30px'
                    }
                )
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'backgroundColor': '#f8f9fa',
                'padding': '15px 20px',
                'borderRadius': '8px',
                'marginBottom': '15px'
            })
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '10px'
        }),
        
        dcc.Graph(id='top-stations-graph', style={'height': '600px', 'borderRadius': '10px'})
    ], style={
        'backgroundColor': 'white',
        'margin': '20px 0',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
