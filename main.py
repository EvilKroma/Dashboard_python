from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

from src.pages import simple_page
from src.utils.get_data import fetch_multiple_records

app = Dash(__name__, suppress_callback_exceptions=True)

# Layout principal utilisant simple_page comme conteneur
app.layout = simple_page.get_layout()

# Callback pour la mise à jour du dashboard (home component)
@callback(
    [Output('data-table', 'data'), Output('stations-map', 'figure'), Output('price-histogram', 'figure')],
    Input('city-dropdown', 'value')
)
def update_dashboard(selected_city):
    df = fetch_multiple_records(300)
    if selected_city and selected_city != 'ALL':
        df = df[df['ville'] == selected_city]
    
    # Pour le hover des pts rouges
    hover_template = "<b>%{hovertext}</b><br>"
    hover_template += "Code postal: %{customdata[0]}<br>"
    hover_template += "Carburants: %{customdata[1]}<br>"
    
    customdata = []
    for idx, row in df.iterrows():
        cp = row.get('cp', '')
        carburants = row.get('carburants_disponibles', '')
        
        # Liste des prix dispo
        prix_info = []
        price_mapping = {
            'Gazole': row.get('gazole_prix'),
            'SP95': row.get('sp95_prix'), 
            'E85': row.get('e85_prix'),
            'GPLc': row.get('gplc_prix'),
            'E10': row.get('e10_prix'),
            'SP98': row.get('sp98_prix')
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
        color_discrete_sequence=['#e74c3c'],
        zoom=5 if selected_city == 'ALL' else 12,
        height=500,
        title=f"Stations-service {selected_city if selected_city != 'ALL' else 'en France'}"
    )
    
    # Applique le hover
    fig.update_traces(
        customdata=customdata,
        hovertemplate=hover_template,
        marker=dict(size=8, opacity=0.8)
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":10,"t":40,"l":10,"b":10},
        title_font_size=16,
        title_font_color='#2c3e50'
    )

    # Histogramme des prix
    price_cols = ['gazole_prix', 'sp95_prix', 'sp98_prix', 'e85_prix', 'e10_prix', 'gplc_prix']
    available_cols = [c for c in price_cols if c in df.columns]
    if len(available_cols) == 0:
        fig_hist = px.histogram(title="Aucun prix disponible")
    else:
        prices_df = df[available_cols].melt(var_name='fuel', value_name='price')
        prices_df = prices_df.dropna(subset=['price'])
        prices_df = prices_df[prices_df['price'] > 0]
        mapping = {
            'gazole_prix': 'Gazole',
            'sp95_prix': 'SP95',
            'sp98_prix': 'SP98',
            'e85_prix': 'E85',
            'e10_prix': 'E10',
            'gplc_prix': 'GPLc'
        }
        prices_df['fuel'] = prices_df['fuel'].map(mapping).fillna(prices_df['fuel'])

        # Calcul des moyennes par carburant et moyenne globale
        mean_by_fuel = prices_df.groupby('fuel', as_index=False)['price'].mean()
        overall_mean = prices_df['price'].mean() if not prices_df.empty else None
        if overall_mean is not None:
            mean_by_fuel = pd.concat([mean_by_fuel, pd.DataFrame([{'fuel': 'Moyenne', 'price': overall_mean}])], ignore_index=True)

        # Bar chart montrant la moyenne par carburant + colonne "Moyenne"
        fig_hist = px.bar(
            mean_by_fuel,
            x='fuel',
            y='price',
            color='fuel',
            labels={'price': 'Prix moyen (€)', 'fuel': 'Type carburant'},
            title='Prix moyen par type de carburant (et moyenne totale)'
        )
        fig_hist.update_traces(showlegend=False, opacity=0.85)
        fig_hist.update_layout(
            margin={"r":10,"t":40,"l":10,"b":10},
            yaxis=dict(range=[0, max(4, (overall_mean or 0) * 1.1)])  # ajuste l'échelle si besoin
        )

    return df.to_dict("records"), fig, fig_hist

if __name__ == "__main__":
    app.run(debug=True)
