from dash import Dash, html, dash_table, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

from src.utils.get_data import fetch_records, fetch_multiple_records

# fetch_multiple_records(300) -> Toutes les stations
# initial_df['ville'] -> Colonne "ville" du DataFrame
# .dropna() -> Supprime les valeurs vides (stations sans ville)
# .unique() -> Ne garde que les villes uniques (pas de doublons)
# sorted() -> Trie alphabétiquement

initial_df = fetch_multiple_records(300)
cities = sorted(initial_df['ville'].dropna().unique()) # Récupère les villes (pour le filtre)

app = Dash(__name__)
app.layout = html.Div([
	html.H1("Prix des carburants par ville"),
	html.Div([
		html.Label("Sélectionner une ville:"),
		# Menu déroulant avec les villes
		dcc.Dropdown(
			id='city-dropdown',
			options=[{'label': 'Toutes les villes', 'value': 'ALL'}] + 
			        [{'label': city, 'value': city} for city in cities],
			value='ALL',
			clearable=False
		),
	], style={'margin': '20px 0'}),
	
	# Carte interactive
	html.Div([
		html.H3("Localisation des stations"),
		dcc.Graph(id='stations-map', style={'height': '500px'})
	], style={'margin': '20px 0'}),
	
	# Tableau des données
	html.Div([
		html.H3("Détails des stations"),
		dash_table.DataTable(
			id='data-table',
			columns=[{"name": c, "id": c} for c in initial_df.columns],
			page_size=20,
			style_table={"overflowX": "auto"},
		),
	]),
])

# Filtre les données selon la ville sélectionnée
@callback(
	[Output('data-table', 'data'), Output('stations-map', 'figure')],
	Input('city-dropdown', 'value')
)
def update_dashboard(selected_city):
	df = fetch_multiple_records(300)
	if selected_city and selected_city != 'ALL':
		df = df[df['ville'] == selected_city]
	
	# Créer la carte avec hover personnalisé
	# Préparer les données hover en filtrant les NaN
	hover_template = "<b>%{hovertext}</b><br>"
	hover_template += "Code postal: %{customdata[0]}<br>"
	hover_template += "Carburants: %{customdata[1]}<br>"
	
	# Créer les données customdata avec prix filtrés
	customdata = []
	for idx, row in df.iterrows():
		cp = row['cp']
		carburants = row['carburants_disponibles']
		
		# Construire la liste des prix disponibles
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
		color_discrete_sequence=['red'],
		zoom=5 if selected_city == 'ALL' else 12,
		height=500,
		title=f"Stations-service {selected_city if selected_city != 'ALL' else 'en France'}"
	)
	
	# Appliquer le hover personnalisé
	fig.update_traces(
		customdata=customdata,
		hovertemplate=hover_template
	)
	
	# Configuration de la carte
	fig.update_layout(
		mapbox_style="open-street-map",
		margin={"r":0,"t":50,"l":0,"b":0}
	)
	
	return df.to_dict("records"), fig

if __name__ == "__main__":
	app.run(debug=True)
