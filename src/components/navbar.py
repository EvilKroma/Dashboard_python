from dash import html, dcc

def get_navbar():
    """Composant barre de navigation avec liens"""
    return html.Div([
        html.Div([
            dcc.Link('Accueil', href='/', 
                    style={'color': 'white', 'textDecoration': 'none', 'marginRight': '20px', 'fontWeight': 'bold'}),
            dcc.Link('À propos', href='/about', 
                    style={'color': 'white', 'textDecoration': 'none', 'fontWeight': 'bold'})
        ], style={'textAlign': 'center', 'padding': '15px'})
    ], style={
        'backgroundColor': '#2c3e50',
        'marginBottom': '0px'
    })