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
    [Output('data-table', 'data'), 
     Output('stations-map', 'figure'), 
     Output('price-histogram', 'figure'),
     Output('price-distribution', 'figure'),
     Output('gazole-vs-avg-price', 'figure'),
     Output('top-stations-graph', 'figure')],
    [Input('city-dropdown', 'value'), 
     Input('stations-map', 'clickData'),
     Input('fuel-type-dropdown', 'value'),
     Input('top-stations-filter', 'value'),
     Input('top-stations-fuel-filter', 'value')]
)
def update_dashboard(selected_city, click_data, selected_fuel, top_stations_filter, top_stations_fuel):
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
            fig_hist.update_layout(
                margin={"r":10,"t":40,"l":10,"b":10},
                yaxis=dict(range=[0, 3])
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
            yaxis=dict(range=[0, 3])
        )


    # Vrai histogramme de distribution des prix
    # Ce graphique utilise TOUTES les données (current_df), pas le filtre de ville
    price_cols_all = ['gazole_prix', 'sp95_prix', 'sp98_prix', 'e85_prix', 'e10_prix', 'gplc_prix']
    available_cols_all = [c for c in price_cols_all if c in current_df.columns]
    
    if len(available_cols_all) > 0:
        prices_df = current_df[available_cols_all].melt(var_name='fuel', value_name='price')
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
            title='Distribution des prix des carburants en France',
            labels={'price': 'Prix (€)', 'count': 'Nombre de stations', 'fuel': 'Type de carburant'},
            barmode='group'
        )
        fig_distribution.update_layout(
            margin={"r":10,"t":40,"l":10,"b":10},
            xaxis_title='Prix (€)',
            yaxis_title='Nombre de stations'
        )
    else:
        fig_distribution = px.histogram(title="Aucun prix disponible")


    # Graphique dynamique: Prix d'un carburant vs Prix moyen de la station
    # Ce graphique utilise TOUTES les données (current_df), pas le filtre de ville
    fuel_labels = {
        'gazole_prix': 'Gazole',
        'sp95_prix': 'SP95',
        'sp98_prix': 'SP98',
        'e10_prix': 'E10',
        'e85_prix': 'E85',
        'gplc_prix': 'GPLc'
    }
    
    selected_fuel_label = fuel_labels.get(selected_fuel, 'Carburant')
    
    # Utiliser current_df (toutes les données) au lieu de df (données filtrées par ville)
    df_fuel = current_df[(current_df[selected_fuel].notna()) & (current_df[selected_fuel] > 0) & 
                         (current_df['prix_moyen'].notna()) & (current_df['prix_moyen'] > 0)].copy()
    
    if len(df_fuel) > 0:
        fig_fuel_avg = px.scatter(
            df_fuel,
            x='prix_moyen',
            y=selected_fuel,
            color='nb_carburants',
            size='nb_carburants',
            hover_data=['ville', 'carburants_disponibles'],
            labels={'prix_moyen': 'Prix moyen de la station (€)', 
                    selected_fuel: f'Prix du {selected_fuel_label} (€)',
                    'nb_carburants': 'Nb carburants'},
            title=f'Prix du {selected_fuel_label} vs prix moyen de tous les carburants de la station',
            color_continuous_scale='RdYlGn_r'
        )
        
        # Ajouter une ligne de tendance
        import numpy as np
        if len(df_fuel) > 1:
            z = np.polyfit(df_fuel['prix_moyen'], df_fuel[selected_fuel], 1)
            p = np.poly1d(z)
            x_trend = np.linspace(df_fuel['prix_moyen'].min(), df_fuel['prix_moyen'].max(), 100)
            fig_fuel_avg.add_scatter(
                x=x_trend, 
                y=p(x_trend), 
                mode='lines', 
                name='Tendance',
                line=dict(color='red', dash='dash', width=2)
            )
        
        fig_fuel_avg.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='white')))
        fig_fuel_avg.update_layout(
            margin={"r":120,"t":40,"l":10,"b":10},
            legend=dict(
                orientation="v",
                yanchor="bottom",
                y=0.01,
                xanchor="right",
                x=0.99,
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="rgba(0, 0, 0, 0.3)",
                borderwidth=1
            ),
            coloraxis_colorbar=dict(
                title="Nb carburants",
                x=1.15
            )
        )
    else:
        fig_fuel_avg = px.scatter(title=f"Aucune donnée disponible pour {selected_fuel_label}")

    # Créer le top 5 des stations avec filtre carburant
    # Mapping des carburants avec labels
    fuel_label_map = {
        'prix_moyen': 'Prix moyen global',
        'gazole_prix': 'Gazole',
        'sp95_prix': 'SP95',
        'sp98_prix': 'SP98',
        'e10_prix': 'E10',
        'e85_prix': 'E85',
        'gplc_prix': 'GPLc'
    }
    
    selected_fuel_label_top = fuel_label_map.get(top_stations_fuel, 'Prix moyen')
    
    # Filtrer les données valides pour le carburant sélectionné
    df_fuel_filtered = current_df[(current_df[top_stations_fuel].notna()) & (current_df[top_stations_fuel] > 0)].copy()
    
    # Grouper par ville et prendre la meilleure/pire station
    if top_stations_filter == 'expensive':
        # Pour les plus chers : prendre le max par ville
        df_top5 = df_fuel_filtered.loc[df_fuel_filtered.groupby('ville')[top_stations_fuel].idxmax()].copy()
        df_top5 = df_top5.nlargest(5, top_stations_fuel)
        title_text = f'Top 5 - {selected_fuel_label_top} les plus chers'
        color_seq = ['#e74c3c']
    else:
        # Pour les plus bas : prendre le min par ville
        df_top5 = df_fuel_filtered.loc[df_fuel_filtered.groupby('ville')[top_stations_fuel].idxmin()].copy()
        df_top5 = df_top5.nsmallest(5, top_stations_fuel)
        title_text = f'Top 5 - {selected_fuel_label_top} les plus bas'
        color_seq = ['#27ae60']
    
    if len(df_top5) > 0:
        # Afficher juste la ville
        df_top5['station_label'] = df_top5['ville']
        
        # Créer le graphique
        fig_top5 = px.bar(
            df_top5,
            x='station_label',
            y=top_stations_fuel,
            color_discrete_sequence=color_seq,
            labels={top_stations_fuel: f'{selected_fuel_label_top} (€)', 'station_label': 'Ville'},
            title=title_text,
            text=top_stations_fuel
        )
        
        fig_top5.update_traces(
            textposition='outside',
            marker=dict(line=dict(width=1, color='white')),
            texttemplate='<b>%{y:.3f}€</b>'
        )
        
        # Calculer l'intervalle précis pour l'axe Y
        min_price = df_top5[top_stations_fuel].min()
        max_price = df_top5[top_stations_fuel].max()
        price_range = max_price - min_price
        margin = max(price_range * 0.25, 0.02)  # 25% de marge ou minimum 0.02€
        
        fig_top5.update_layout(
            margin={"r":10,"t":40,"l":10,"b":120},
            xaxis_title='Ville',
            yaxis_title=f'{selected_fuel_label_top} (€)',
            yaxis=dict(
                range=[min_price - margin, max_price + margin],
                dtick=(price_range / 5) if price_range > 0 else 0.1  # 5 ticks pour la précision
            ),
            showlegend=False,
            title_font_size=16,
            title_font_color='#2c3e50',
            xaxis_tickangle=-45,
            hovermode='x unified'
        )
    else:
        fig_top5 = px.bar(title="Aucune donnée disponible")

    return df.to_dict("records"), fig, fig_hist, fig_distribution, fig_fuel_avg, fig_top5

if __name__ == "__main__":
    app.run(debug=True)