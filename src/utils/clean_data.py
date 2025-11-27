import pandas as pd
from datetime import datetime
from typing import Dict, List, Any


def clean_raw_data(raw_data: dict) -> dict:
    raw_records = raw_data['data']
    cleaned_records = []
    
    for record in raw_records:
        cleaned_record = clean_single_record(record)
        if cleaned_record is not None:
            cleaned_records.append(cleaned_record)
    
    # Structure des données nettoyées
    cleaned_data = {
        "metadata": {
            "cleaning_timestamp": datetime.now().isoformat(),
            "total_records": len(cleaned_records),
            "raw_fetch_timestamp": raw_data['metadata']['fetch_timestamp'],
            "cleaning_operations": [
                "Extraction coordonnées GPS",
                "Conversion prix en float",
                "Nettoyage carburants disponibles",
                "Validation géolocalisation",
                "Suppression enregistrements invalides"
            ]
        },
        "data": cleaned_records
    }
    
    return cleaned_data


def clean_single_record(record: dict) -> dict:
    """Nettoie un seul enregistrement"""
    try:
        cleaned = {}
        
        # Copie des champs de base
        basic_fields = ['id', 'nom', 'adresse', 'ville', 'cp', 'pop', 'marque']
        for field in basic_fields:
            cleaned[field] = record.get(field, "")
        
        # Extraction et nettoyage des coordonnées GPS
        if "geom" in record and isinstance(record["geom"], dict):
            cleaned["longitude"] = float(record["geom"].get("lon", 0))
            cleaned["latitude"] = float(record["geom"].get("lat", 0))
            
            # Validation des coordonnées (France métropolitaine + DOM-TOM)
            if not is_valid_french_coordinates(cleaned["longitude"], cleaned["latitude"]):
                return None  # Skip cet enregistrement
        else:
            return None  # Skip si pas de géolocalisation
        
        # Nettoyage des prix des carburants
        price_fields = {
            'gazole_prix': 'gazole_prix',
            'sp95_prix': 'sp95_prix', 
            'sp98_prix': 'sp98_prix',
            'e10_prix': 'e10_prix',
            'e85_prix': 'e85_prix',
            'gplc_prix': 'gplc_prix'
        }
        
        available_fuels = []
        for api_field, clean_field in price_fields.items():
            price_value = record.get(api_field)
            if price_value and price_value != "":
                try:
                    cleaned_price = float(price_value)
                    if cleaned_price > 0:  # Prix valide
                        cleaned[clean_field] = cleaned_price
                        available_fuels.append(api_field.replace('_prix', '').upper())
                    else:
                        cleaned[clean_field] = None
                except (ValueError, TypeError):
                    cleaned[clean_field] = None
            else:
                cleaned[clean_field] = None
        
        # Liste des carburants disponibles
        cleaned['carburants_disponibles'] = ', '.join(available_fuels)
        
        # Ajout de champs calculés
        cleaned['nb_carburants'] = len(available_fuels)
        cleaned['prix_moyen'] = calculate_average_price(cleaned)
        
        # Nettoyage des dates
        date_fields = ['gazole_maj', 'sp95_maj', 'sp98_maj', 'e10_maj', 'e85_maj', 'gplc_maj']
        for field in date_fields:
            cleaned[field] = record.get(field, "")
        
        return cleaned
        
    except Exception as e:
        return None


def is_valid_french_coordinates(longitude: float, latitude: float) -> bool:
    """Vérifie si les coordonnées sont valides (simplifiée)"""
    # France métropolitaine 
    if -5.0 <= longitude <= 10.0 and 42.0 <= latitude <= 52.0:
        return True
    
    # DOM-TOM
    if (-62.0 <= longitude <= -51.0 and 14.0 <= latitude <= 18.0) or \
       (55.0 <= longitude <= 56.0 and -22.0 <= latitude <= -20.0):
        return True
    
    return False


def calculate_average_price(record: dict) -> float:
    """Calcule le prix moyen des carburants disponibles"""
    price_fields = ['gazole_prix', 'sp95_prix', 'sp98_prix', 'e10_prix', 'e85_prix', 'gplc_prix']
    valid_prices = []
    
    for field in price_fields:
        price = record.get(field)
        if price is not None and price > 0:
            valid_prices.append(price)
    
    if valid_prices:
        return round(sum(valid_prices) / len(valid_prices), 3)
    return None


def get_data_statistics(cleaned_data: dict) -> dict:
    """Génère des statistiques sur les données nettoyées"""
    records = cleaned_data['data']
    
    stats = {
        'total_records': len(records),
        'stations_with_gazole': sum(1 for r in records if r.get('gazole_prix')),
        'stations_with_sp95': sum(1 for r in records if r.get('sp95_prix')),
        'stations_with_e85': sum(1 for r in records if r.get('e85_prix')),
        'unique_cities': len(set(r['ville'] for r in records if r['ville'])),
        'unique_brands': len(set(r['marque'] for r in records if r['marque']))
    }
    
    return stats