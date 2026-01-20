from dash import html, dash_table, dcc
import plotly.express as px
import pandas as pd

from src.utils.get_data import fetch_multiple_records
from src.components import header, footer, component1, component2, component3, component4, component5

# Search bar selon chaque ville
initial_df = fetch_multiple_records(300)
cities = sorted(initial_df['ville'].dropna().unique())

def get_layout():
    return html.Div([
        header.get_header(),
        
        html.Div([
            html.Div([
                html.Label("Sélectionner une ville:", 
                    style={
                        'fontWeight': 'bold',
                        'marginBottom': '10px',
                        'color': '#2c3e50',
                        'fontSize': '14px'
                    }
                ),
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[{'label': 'Toutes les villes', 'value': 'ALL'}] + 
                            [{'label': city, 'value': city} for city in cities],
                    value='ALL',
                    clearable=False,
                    style={
                        'borderRadius': '5px'
                    }
                ),
            ], className="six columns", style={'padding': '10px'})
        ], className="row", style={
            'backgroundColor': 'white',
            'margin': '20px 0',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }),
        
        # Section principale avec carte et histogramme
        html.Div([
            # Carte (component1)
            html.Div([
                component1.get_map_component()
            ], className="six columns"),
            
            # Colonne droite avec histogramme
            html.Div([
                component2.get_price_histogram_component()
            ], className="six columns")
        ], className="row"),
        
        # Top 5 des stations les plus chères
        component5.get_top_stations_component(),
        
        # Distribution des prix (component3)
        component3.get_price_distribution_component(),
        
        # Graphique Prix du Gazole vs Prix moyen (component4)
        component4.get_gazole_vs_avg_price_component(),
        
        # Tableau qui envoie les détails du JSON
        html.Div([
            html.H3("Détails des stations", 
                style={
                    'color': '#2c3e50',
                    'marginBottom': '15px',
                    'fontFamily': 'Arial, sans-serif'
                }
            ),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": c, "id": c} for c in initial_df.columns],
                page_size=15,
                style_table={
                    "overflowX": "auto",
                    'borderRadius': '10px'
                },
                style_header={
                    'backgroundColor': '#3498db',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '12px'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f8f9fa'
                    }
                ]
            ),
        ], style={
            'backgroundColor': 'white',
            'margin': '20px 0',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }),
        
        footer.get_footer()
    ])