import pandas as pd
import requests
import json
import os
from datetime import datetime

try:
    from config import FULL_ENDPOINT, DEFAULT_LIMIT, TIMEOUT
    from .clean_data import clean_raw_data
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from config import FULL_ENDPOINT, DEFAULT_LIMIT, TIMEOUT
    from clean_data import clean_raw_data

# Chemins des fichiers data
RAW_DATA_PATH = "data/raw/rawdata.json"
CLEANED_DATA_PATH = "data/cleaned/cleaneddata.json"


def fetch_and_save_data(total_limit: int = DEFAULT_LIMIT) -> pd.DataFrame:
    """Pipeline complet: API → Raw → Clean → DataFrame"""
    
    # Fetch de l'API
    all_rows = []
    offset = 0
    batch_size = 100
    
    while len(all_rows) < total_limit:
        params = {"limit": batch_size, "offset": offset}
        try:
            resp = requests.get(FULL_ENDPOINT, params=params, timeout=TIMEOUT)
            resp.raise_for_status()
            payload = resp.json()
            rows = payload.get("results", [])
            
            if not rows:
                break
                
            all_rows.extend(rows)
            offset += batch_size
            
        except Exception as e:
            print(f"Erreur lors de la récupération: {e}")
            break
    
    final_data = all_rows[:total_limit]
    
    # Sauvegarde raw
    raw_data = {
        "metadata": {
            "fetch_timestamp": datetime.now().isoformat(),
            "total_records": len(final_data),
            "api_endpoint": FULL_ENDPOINT
        },
        "data": final_data
    }
    
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    with open(RAW_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)
    
    # Nettoyage et sauvegarde clean
    cleaned_data = clean_raw_data(raw_data)
    
    os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)
    with open(CLEANED_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    return pd.DataFrame(cleaned_data['data'])


def get_data_for_dashboard(force_refresh: bool = False, total_limit: int = DEFAULT_LIMIT) -> pd.DataFrame:
    """Point d'entrée principal pour le dashboard"""
    
    if force_refresh or not os.path.exists(CLEANED_DATA_PATH):
        return fetch_and_save_data(total_limit)
    
    with open(CLEANED_DATA_PATH, 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)
    
    return pd.DataFrame(cleaned_data['data'])

def fetch_multiple_records(total_limit: int = DEFAULT_LIMIT) -> pd.DataFrame:
    """Fonction de compatibilité"""
    return get_data_for_dashboard(force_refresh=False, total_limit=total_limit)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test du pipeline de données")
    parser.add_argument('--refresh', action='store_true', help='Actualiser les données')
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT, help='Nombre d\'enregistrements')
    parser.add_argument('--stats', action='store_true', help='Afficher les statistiques')
    
    args = parser.parse_args()
    
    if args.refresh:
        df = fetch_and_save_data(args.limit)
    else:
        df = get_data_for_dashboard(force_refresh=False)
    
    if args.stats:
        print(f"Total: {len(df)} | Gazole: {df['gazole_prix'].notna().sum()} | SP95: {df['sp95_prix'].notna().sum()} | E85: {df['e85_prix'].notna().sum()} | Villes: {df['ville'].nunique()}")
    else:
        print(f"{len(df)} enregistrements chargés")