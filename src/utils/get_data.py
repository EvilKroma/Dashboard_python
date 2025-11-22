import pandas as pd
import requests

from config import FULL_ENDPOINT, DEFAULT_LIMIT, TIMEOUT


def fetch_records(limit: int = DEFAULT_LIMIT) -> pd.DataFrame:
	params = {"limit": limit}
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


if __name__ == "__main__":
	df = fetch_records()
	print(df.head())
