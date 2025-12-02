import pandas as pd
import requests

from config import FULL_ENDPOINT, DEFAULT_LIMIT, TIMEOUT

# Récupère les données de l'API
def fetch_records(limit: int = DEFAULT_LIMIT) -> pd.DataFrame:
	params = {"limit": min(limit, 100)}  
	resp = requests.get(FULL_ENDPOINT, params=params, timeout=TIMEOUT)
	resp.raise_for_status()
	payload = resp.json()
	rows = payload.get("results", [])
	
	# Converti en String
	for row in rows:
		if "geom" in row and isinstance(row["geom"], dict):
			row["longitude"] = row["geom"].get("lon", "")
			row["latitude"] = row["geom"].get("lat", "")
			row["geom"] = f"({row['geom'].get('lon', '')}, {row['geom'].get('lat', '')})"
		
		for key, value in row.items():
			if isinstance(value, (list, dict)):
				row[key] = str(value)
	
	return pd.DataFrame(rows)


# Récupère plus de données en faisant plusieurs appels API
def fetch_multiple_records(total_limit: int = 300) -> pd.DataFrame:
	"""Fetch more records by making multiple API calls"""
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
			print(f"Error fetching batch at offset {offset}: {e}")
			break

	for row in all_rows:
		if "geom" in row and isinstance(row["geom"], dict):
			row["longitude"] = row["geom"].get("lon", "")
			row["latitude"] = row["geom"].get("lat", "")
			row["geom"] = f"({row['geom'].get('lon', '')}, {row['geom'].get('lat', '')})"
		
		for key, value in row.items():
			if isinstance(value, (list, dict)):
				row[key] = str(value)
	
	return pd.DataFrame(all_rows[:total_limit])


if __name__ == "__main__":
	df = fetch_records()
	print(df.head())
