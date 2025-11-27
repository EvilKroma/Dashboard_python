from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

from src.pages import simple_page
from src.utils.get_data import get_data_for_dashboard
from config import DEFAULT_LIMIT

app = Dash(__name__, suppress_callback_exceptions=True)

# Layout principal utilisant simple_page comme conteneur
app.layout = simple_page.get_layout()

# Callback pour la mise à jour du dashboard (home component)
@callback(
    [Output('data-table', 'data'), Output('stations-map', 'figure')],
    Input('city-dropdown', 'value')
)
def update_dashboard(selected_city):
    df = get_data_for_dashboard(force_refresh=False)
    if selected_city and selected_city != 'ALL':
        df = df[df['ville'] == selected_city]
    
    # Pour le hover des pts rouges
    hover_template = "<b>%{hovertext}</b><br>"
    hover_template += "Code postal: %{customdata[0]}<br>"
    hover_template += "Carburants: %{customdata[1]}<br>"
    
    customdata = []
    for idx, row in df.iterrows():
        cp = row['cp']
        carburants = row['carburants_disponibles']
        
        # Liste des prix dispo
        prix_info = []
        price_mapping = {
            'Gazole': row['gazole_prix'],
            'SP95': row['sp95_prix'], 
            'E85': row['e85_prix'],
            'GPLc': row['gplc_prix'],
            'E10': row['e10_prix'],
            'SP98': row['sp98_prix']
        }
        
        for fuel, price in price_mapping.items():
            if pd.notna(price) and price > 0:
                prix_info.append(f"{fuel}: {price:.3f}€")
        
        prix_str = "<br>".join(prix_info) if prix_info else "Aucun prix disponible"
        customdata.append([cp, carburants, prix_str])
    
    hover_template += "Prix:<br>%{customdata[2]}<extra></extra>"
    
    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='ville',
        color_discrete_sequence=['#e74c3c'],  # Rouge plus moderne
        zoom=5 if selected_city == 'ALL' else 12,
        height=500,
        title=f"Stations-service {selected_city if selected_city != 'ALL' else 'en France'}"
    )
    
    # Applique le hover
    fig.update_traces(
        customdata=customdata,
        hovertemplate=hover_template,
        marker=dict(size=8, opacity=0.8)  # Marqueurs plus visibles
    )
    
    # Config de la carte avec style amélioré
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":10,"t":40,"l":10,"b":10},
        title_font_size=16,
        title_font_color='#2c3e50'
    )
    
    return df.to_dict("records"), fig

if __name__ == "__main__":
    app.run(debug=True)
