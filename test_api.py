import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

def fetch_fixtures(league_id, season):
    """Fetch all fixtures for a given league and season"""
    
    endpoint = f"{BASE_URL}/fixtures"
    
    params = {
        "league": league_id,
        "season": season
    }
    
    print(f"Fetching fixtures for league {league_id}, season {season}...")
    
    response = requests.get(endpoint, headers=HEADERS, params=params)
    
    data = response.json()
    
    return data

def save_raw(data, filename):
    """Save raw JSON response to local file"""
    
    os.makedirs("raw_data", exist_ok=True)
    
    filepath = f"raw_data/{filename}"
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved raw data to {filepath}")

if __name__ == "__main__":
    
    # Premier League = 39, Season 2023
    data = fetch_fixtures(league_id=39, season=2023)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_raw(data, f"fixtures_PL_2023_{timestamp}.json")