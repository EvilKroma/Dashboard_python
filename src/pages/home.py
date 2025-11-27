from dash import html, dash_table, dcc
import plotly.express as px
import pandas as pd

from src.utils.get_data import fetch_multiple_records
from src.components import header, footer, component1, price_histogram

# Fetch initial
initial_df = fetch_multiple_records(300)
cities = sorted(initial_df['ville'].dropna().unique())

def get_layout():
    return html.Div([
        # Header (composant)
        header.get_header(),
        
        # Section filtres
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
            component1.get_map_component(),
            # Histogramme des prix (nouveau composant)
            price_histogram.get_price_histogram_component()
        ], className="row"),
        
        # Section tableau
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
        
        # Footer (composant)
        footer.get_footer()
    ])