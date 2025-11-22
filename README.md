# Dashboard_python

API utilisée :

Prix des carburants (data.economie.gouv.fr)
L'API du gouvernement français est excellente, gratuite et très riche en données chiffrées.

Données GPS : Localisation de toutes les stations-service de France.

Données histogramme : Distribution des prix (ex: Histogramme des prix du Gazole entre 1.60€ et 2.00€).

Le petit plus : Permet de faire des filtres intéressants (par département, par marque).

Documentation : [data.economie.gouv.fr](https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/api/)

Endpoint : /api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records?limit=20 

## Démarrage rapide

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```