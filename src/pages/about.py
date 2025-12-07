from dash import html

#Texte brut de la page "A prppos"
def get_layout():
    return html.Div([
        html.Div([
            html.H1("À propos du projet", 
                style={
                    'textAlign': 'center',
                    'color': '#2c3e50',
                    'marginBottom': '20px',
                    'fontFamily': 'Arial, sans-serif'
                }
            ),
            
            html.Div([
                html.H3("Contexte pédagogique", style={'color': '#3498db', 'marginBottom': '15px'}),
                html.P([
                    "Ce projet s'inscrit dans le cadre du mini-projet de visualisation de données à ",
                    html.Strong("ESIEE PARIS"),
                    " réalisé par ",
                    html.Strong("Dorian DENEUCHATEL / Flavien NOUET"),
                    " de la promotion ",
                    html.Strong("E3FI"),
                    "."
                ], style={'fontSize': '16px', 'lineHeight': '1.6', 'marginBottom': '20px'}),
                
                html.H3("Objectif du projet", style={'color': '#3498db', 'marginBottom': '15px'}),
                html.P(
                    "L'objectif de ce mini-projet est d'éclairer un sujet d'intérêt public en utilisant des données publiques Open Data. "
                    "Le sujet choisi porte sur les prix des carburants en France, thématique économique et environnementale d'actualité "
                    "qui impacte directement le quotidien des citoyens français.",
                    style={'fontSize': '14px', 'lineHeight': '1.8', 'marginBottom': '20px', 'fontStyle': 'italic', 'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '5px'}
                ),
                
                html.H3("Définition Open Data", style={'color': '#3498db', 'marginBottom': '15px'}),
                html.P([
                    "L'Open Data (ou donnée ouverte) est une donnée numérique d'origine publique ou privée. "
                    "Elle peut être notamment produite par une collectivité, un service public ou une entreprise. "
                    "Elle est diffusée de manière structurée selon une méthode et une licence ouverte garantissant "
                    "son libre accès et sa réutilisation par tous, sans restriction technique, juridique ou financière."
                ], style={'fontSize': '13px', 'lineHeight': '1.6', 'marginBottom': '20px', 'color': '#7f8c8d', 'borderLeft': '4px solid #3498db', 'paddingLeft': '15px'}),
                html.P([
                    html.Em("Source : "),
                    html.A("Wikipedia", href="https://fr.wikipedia.org/wiki/Donn%C3%A9es_ouvertes", target="_blank", 
                           style={'color': '#3498db', 'textDecoration': 'underline'})
                ], style={'fontSize': '12px', 'color': '#95a5a6', 'textAlign': 'right'}),
                
                html.H3("Enjeux du sujet choisi", style={'color': '#3498db', 'marginBottom': '15px'}),
                html.Ul([
                    html.Li("Impact économique : coût des déplacements pour les ménages français"),
                    html.Li("Enjeu environnemental : choix entre carburants traditionnels et alternatifs (E85, électrique)"),
                    html.Li("Transparence publique : accès libre aux prix pratiqués par les stations-service"),
                    html.Li("Aide à la décision : comparaison géographique pour optimiser ses achats"),
                    html.Li("Politique énergétique : suivi de l'évolution des prix dans le contexte de transition énergétique")
                ], style={'fontSize': '14px', 'lineHeight': '1.8', 'marginBottom': '20px'}),
                
                html.H3("Technologies utilisées", style={'color': '#3498db', 'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.H4("Backend", style={'color': '#2c3e50'}),
                        html.Ul([
                            html.Li("Python 3.12"),
                            html.Li("Pandas (manipulation de données)"),
                            html.Li("Requests (API calls)")
                        ])
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                    
                    html.Div([
                        html.H4("Frontend", style={'color': '#2c3e50'}),
                        html.Ul([
                            html.Li("Dash (interface web)"),
                            html.Li("Plotly (graphiques interactifs)"),
                            html.Li("CSS custom (styling)")
                        ])
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
                ], style={'marginBottom': '20px'}),
                
                html.H3("Source des données", style={'color': '#3498db', 'marginBottom': '15px'}),
                html.P([
                    "Les données proviennent de l'API publique ",
                    html.A("data.economie.gouv.fr", 
                          href="https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/api/",
                          target="_blank",
                          style={'color': '#3498db', 'textDecoration': 'underline'}),
                    " qui fournit les prix des carburants en France en temps réel. Cette API gouvernementale garantit "
                    "la fiabilité, l'actualité et la gratuité des données utilisées."
                ], style={'fontSize': '14px', 'lineHeight': '1.6', 'marginBottom': '20px'}),
                
                html.H3("Fonctionnalités développées", style={'color': '#3498db', 'marginBottom': '15px'}),
                html.Ul([
                    html.Li("Récupération automatisée des données via API REST"),
                    html.Li("Interface de filtrage par ville (300+ villes disponibles)"),
                    html.Li("Cartographie interactive avec géolocalisation des stations"),
                    html.Li("Affichage détaillé des prix par type de carburant"),
                    html.Li("Tableau de données paginé avec informations complètes"),
                    html.Li("Design responsive et professionnel"),
                    html.Li("Histogramme dynamique des prix des carburants avec une moyenne par type de carburant")
                ], style={'fontSize': '14px', 'lineHeight': '1.8'})
                
            ], style={
                'backgroundColor': 'white',
                'padding': '30px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'maxWidth': '800px',
                'margin': '0 auto'
            })
        ], style={
            'backgroundColor': '#f8f9fa',
            'minHeight': '100vh',
            'padding': '40px 20px',
            'fontFamily': 'Arial, sans-serif'
        })
    ])