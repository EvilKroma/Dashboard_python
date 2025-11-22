from dash import Dash, html, dash_table

from src.utils.get_data import fetch_records

df = fetch_records()

app = Dash(__name__)
app.layout = html.Div([
	html.H1("Prix des carburants (échantillon)"),
	dash_table.DataTable(
		data=df.to_dict("records"),
		columns=[{"name": c, "id": c} for c in df.columns],
		page_size=20,
		style_table={"overflowX": "auto"},
	),
])

if __name__ == "__main__":
	app.run(debug=True)
