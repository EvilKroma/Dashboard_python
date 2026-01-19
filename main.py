from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

from src.pages import simple_page
from src.utils.get_data import get_data_for_dashboard
from src.utils.get_data import fetch_multiple_records
from config import DEFAULT_LIMIT

app = Dash(__name__, suppress_callback_exceptions=True, title="Dashboard - Prix des carburants en France")

app.layout = simple_page.get_layout()

current_df = None

# Mettre a jour les components
@callback(
    [Output('data-table', 'data'), Output('stations-map', 'figure'), Output('price-histogram', 'figure'), Output('price-distribution', 'figure')],
    [Input('city-dropdown', 'value'), Input('stations-map', 'clickData')]
)
def update_dashboard(selected_city, click_data):
    global current_df
    df = fetch_multiple_records(300)
    current_df = df.copy()
    
    if selected_city and selected_city != 'ALL':
        df = df[df['ville'] == selected_city]

    df = df.reset_index(drop=True)
    
    # On vérifie si un point a été cliqué
    selected_station = None
    if click_data and 'points' in click_data and len(click_data['points']) > 0:
        point = click_data['points'][0]
        if 'pointIndex' in point and 0 <= point['pointIndex'] < len(df):
            selected_station = df.iloc[point['pointIndex']]
    
    # Hover sur la carte
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
    
    #je créé la carte ici
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
    
    # Si je sélectionne une station, ses prix s'affichent
    if selected_station is not None:
        station_prices = []
        for fuel, col in [('Gazole', 'gazole_prix'), ('SP95', 'sp95_prix'), ('SP98', 'sp98_prix'), 
                          ('E85', 'e85_prix'), ('E10', 'e10_prix'), ('GPLc', 'gplc_prix')]:
            price = selected_station.get(col)
            if pd.notna(price) and price > 0:
                station_prices.append({'fuel': fuel, 'price': price})
        
        if station_prices:
            prices_df = pd.DataFrame(station_prices)
            fig_hist = px.bar(
                prices_df,
                x='fuel',
                y='price',
                color='fuel',
                labels={'price': 'Prix (€)', 'fuel': 'Type carburant'},
                title=f"Prix à la station: {selected_station.get('ville', 'N/A')}"
            )
        else:
            fig_hist = px.histogram(title="Aucun prix disponible pour cette station")
    else:
        # Affichage par défaut: moyenne par carburant
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

            # Calcul des moyennes
            mean_by_fuel = prices_df.groupby('fuel', as_index=False)['price'].mean()
            overall_mean = prices_df['price'].mean() if not prices_df.empty else None
            if overall_mean is not None:
                mean_by_fuel = pd.concat([mean_by_fuel, pd.DataFrame([{'fuel': 'Moyenne', 'price': overall_mean}])], ignore_index=True)

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
            yaxis=dict(range=[0, max(4, 4)])
        )

    # Vrai histogramme de distribution des prix
    if len(available_cols) > 0:
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
        
        fig_distribution = px.histogram(
            prices_df,
            x='price',
            color='fuel',
            nbins=20,
            title='Distribution des prix des carburants',
            labels={'price': 'Prix (€)', 'count': 'Nombre de stations'},
            barmode='group'
        )
        fig_distribution.update_layout(
            margin={"r":10,"t":40,"l":10,"b":10},
            xaxis_title='Prix (€)',
            yaxis_title='Nombre de stations'
        )
    else:
        fig_distribution = px.histogram(title="Aucun prix disponible")

    return df.to_dict("records"), fig, fig_hist, fig_distribution

if __name__ == "__main__":
    app.run(debug=True)