from dash import html

def get_header():
    """Composant header avec titre et crédit académique"""
    return html.Div([
        html.H1("Dashboard - Prix des carburants en France", 
            style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '10px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        html.P(
            "Projet scolaire ESIEE PARIS - Dorian DENEUCHATEL / Flavien NOUET - E3FI",
            style={
                'textAlign': 'center',
                'color': '#95a5a6',
                'fontSize': '14px',
                'fontStyle': 'italic',
                'marginBottom': '20px'
            }
        )
    ], style={
        'backgroundColor': '#ecf0f1',
        'padding': '20px',
        'marginBottom': '20px',
        'borderRadius': '10px'
    })