from dash import html

def get_footer():
    """Composant footer avec crédit source des données"""
    return html.Div([
        html.P(
            "Données fournies par data.economie.gouv.fr | Mis à jour en temps réel",
            style={
                'textAlign': 'center',
                'color': '#95a5a6',
                'fontSize': '12px',
                'margin': '20px 0'
            }
        )
    ])