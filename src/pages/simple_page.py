from dash import html, dcc, Input, Output, callback

from . import home, about
from ..components import navbar

def get_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        
        # Barre de navigation (composant)
        navbar.get_navbar(),
        
        # Contenu de la page
        html.Div(id='page-content', style={
            'backgroundColor': '#f8f9fa',
            'minHeight': '100vh',
            'padding': '20px',
            'fontFamily': 'Arial, sans-serif'
        })
    ])

# Callback pour la navigation entre composants
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/about':
        return about.get_layout()  # Appel du composant about
    else:  # Default to home
        return home.get_layout()   # Appel du composant home