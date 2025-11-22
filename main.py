from dash import Dash, html, dash_table, dcc, Input, Output, callback

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
	dash_table.DataTable(
		id='data-table',
		columns=[{"name": c, "id": c} for c in initial_df.columns],
		page_size=20,
		style_table={"overflowX": "auto"},
	),
])

# Filre les données selon la ville sélectionnée
@callback(
	Output('data-table', 'data'),
	Input('city-dropdown', 'value')
)
def update_table(selected_city):
	df = fetch_multiple_records(300)
	if selected_city and selected_city != 'ALL':
		df = df[df['ville'] == selected_city]
	return df.to_dict("records")

if __name__ == "__main__":
	app.run(debug=True)
