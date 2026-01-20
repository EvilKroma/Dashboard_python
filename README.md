# Dashboard Python - Prix des Carburants

Dashboard interactif permettant de visualiser et analyser les prix des carburants en France en temps réel grâce aux données ouvertes du gouvernement français.

## User Guide

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de packages Python)

### Installation et déploiement

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/EvilKroma/Dashboard_python.git
   cd Dashboard_python
   ```

2. **Créer un environnement virtuel**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Sur Linux/macOS
   # ou
   .venv\Scripts\activate     # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application**
   ```bash
   python main.py
   ```

5. **Accéder au dashboard**
   Ouvrir votre navigateur et aller à l'adresse : `http://127.0.0.1:8050`

### Utilisation

#### Première utilisation
Lors de la première utilisation, les données seront automatiquement récupérées et traitées selon le workflow suivant :
1. **Récupération** des données brutes depuis l'API → `data/raw/rawdata.json`
2. **Nettoyage** et structuration → `data/cleaned/cleaneddata.json` 
3. **Affichage** dans le dashboard

#### Navigation dans l'application
- **Page d'accueil** : Visualisation interactive des stations-service avec carte et tableau de données
- **Filtrage** : Sélectionner une ville spécifique via le menu déroulant pour filtrer les résultats
- **Carte interactive** : Points cliquables affichant les détails des stations (prix, carburants disponibles)
- **Graphiques maniables** : Graphique dynamique et maniable selon les besoins de l'utilisateur
- **Histogrammes** : Histogrammes structurés mettant en avant les données des carburants
- **Page À propos** : Informations sur le projet et les données utilisées

## Data

### Source des données
- **API** : Prix des carburants (data.economie.gouv.fr)
- **Documentation** : [data.economie.gouv.fr](https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/api/)
- **Endpoint** : `/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records`

### Workflow de traitement des données

Le projet suit un pipeline structuré en 5 étapes :

1. **Récupération** : Les données brutes sont récupérées depuis l'API gouvernementale
2. **Stockage raw** : Sauvegarde au format JSON dans `data/raw/rawdata.json`
3. **Nettoyage** : Traitement et structuration des données avec `clean_data.py`
4. **Stockage clean** : Sauvegarde des données nettoyées dans `data/cleaned/cleaneddata.json`
5. **Affichage** : Utilisation des données nettoyées pour le dashboard

### Caractéristiques des données
- **Mise à jour** : Données en temps réel
- **Couverture géographique** : Toute la France (métropole + DOM-TOM)
- **Types de carburants** : Gazole, SP95, SP98, E10, E85, GPLc
- **Informations disponibles** :
  - Localisation GPS des stations-service
  - Prix par type de carburant
  - Informations sur les stations (ville, code postal)

### Structure des données

## Developer Guide

### Architecture du projet

```
Dashboard_python/
├── main.py                 # Point d'entrée de l'application
├── config.py              # Configuration de l'API
├── requirements.txt       # Dépendances Python
├── data/                  # Stockage des données
│   ├── raw/              # Données brutes de l'API
│   │   └── rawdata.json  # JSON brut depuis l'API
│   └── cleaned/          # Données nettoyées
│       └── cleaneddata.json # JSON structuré pour le dashboard
└── src/
    ├── components/        # Composants réutilisables
    │   ├── navbar.py      # Barre de navigation
    │   ├── header.py      # En-tête
    │   ├── footer.py      # Pied de page
    │   └── ...
    ├── pages/            # Pages de l'application
    │   ├── home.py       # Page d'accueil avec dashboard
    │   ├── about.py      # Page à propos
    │   └── simple_page.py # Layout principal
    └── utils/            # Utilitaires
        ├── get_data.py   # Pipeline de récupération et stockage
        ├── clean_data.py # Algorithmes de nettoyage
        └── common_functions.py # Fonctions communes
```
### Pipeline de données

Le système suit un workflow rigoureux :

1. **API → Raw JSON** (`fetch_raw_data_from_api`)
2. **Raw JSON → Cleaned JSON** (`clean_raw_data`) 
3. **Cleaned JSON → DataFrame** (`load_cleaned_data`)

```python
# Utilisation du pipeline complet
from src.utils.get_data import refresh_data_pipeline
df = refresh_data_pipeline(limit=300)

# Ou chargement des données existantes  
from src.utils.get_data import get_data_for_dashboard
df = get_data_for_dashboard(force_refresh=False)
```

### Ajouter une nouvelle page

1. **Créer le fichier de la page** dans `src/pages/`
   ```python
   # src/pages/ma_nouvelle_page.py
   from dash import html, dcc
   
   def get_layout():
       return html.Div([
           html.H1("Ma Nouvelle Page"),
           # Contenu de votre page
       ])
   ```

2. **Importer dans simple_page.py**
   ```python
   from . import ma_nouvelle_page
   ```

3. **Ajouter la route** dans le callback de `simple_page.py`
   ```python
   def display_page(pathname):
       if pathname == '/ma-nouvelle-page':
           return ma_nouvelle_page.get_layout()
       # autres conditions...
   ```

4. **Ajouter le lien** dans la navbar (`src/components/navbar.py`)

### Ajouter un nouveau graphique

1. **Créer une fonction de graphique** dans un composant
   ```python
   import plotly.express as px
   
   def create_mon_graphique(df):
       fig = px.bar(df, x='colonne_x', y='colonne_y')
       return fig
   ```

2. **Intégrer dans une page**
   ```python
   dcc.Graph(figure=create_mon_graphique(data))
   ```

3. **Ajouter des callbacks** si nécessaire pour l'interactivité

### Technologies utilisées
- **Dash** : Framework web pour applications analytiques
- **Plotly** : Bibliothèque de visualisation interactive
- **Pandas** : Manipulation et analyse des données
- **Requests** : Client HTTP pour les appels API

## Rapport d'analyse

### Principales conclusions

1. **Distribution géographique** : Les stations-service sont inégalement réparties sur le territoire, avec une concentration plus élevée en zones urbaines et le long des axes routiers principaux.

2. **Variabilité des prix** : 
   - Les prix varient significativement selon les régions
   - Les stations en zones urbaines tendent à avoir des prix légèrement plus élevés
   - Certaines enseignes pratiquent des prix systématiquement inférieurs

3. **Disponibilité des carburants** :
   - Le Gazole et SP95 sont disponibles dans pratiquement toutes les stations
   - L'E85 et le GPLc sont moins répandus, principalement dans certaines régions
   - Le SP98 est généralement disponible dans les stations des grandes enseignes

4. **Patterns temporels** : Les données en temps réel permettent d'observer des variations de prix tout au long de la journée et de la semaine.

### Insights techniques
- L'API gouvernementale est très fiable avec un taux de disponibilité élevé
- Les données GPS permettent une géolocalisation précise des stations
- Le format JSON facilite l'intégration et le traitement des données

## Copyright

Je déclare sur l'honneur que le code fourni a été produit par moi-même, à l'exception des lignes ci-dessous :

### Code emprunté et références

**Aucune ligne de code n'a été directement empruntée à des sources externes.**

### Bibliothèques et frameworks utilisés
- **Dash** (Plotly) : Framework web pour applications analytiques - [Documentation officielle](https://dash.plotly.com/)
- **Plotly** : Bibliothèque de visualisation - [Documentation officielle](https://plotly.com/python/)
- **Pandas** : Manipulation de données - [Documentation officielle](https://pandas.pydata.org/)
- **Requests** : Client HTTP - [Documentation officielle](https://requests.readthedocs.io/)

### Données
- **API Prix des carburants** : data.economie.gouv.fr - Données ouvertes du gouvernement français

---

Toute ligne non déclarée ci-dessus est réputée être produite par l'auteur du projet. L'absence ou l'omission de déclaration sera considérée comme du plagiat.

