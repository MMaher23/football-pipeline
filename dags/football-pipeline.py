from airflow.decorators import dag, task
from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv('/opt/airflow/.env')

@dag(
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['football']
)
def football_pipeline():

    @task
    def fetch_fixtures():
        API_KEY = os.getenv("API_KEY")
        
        response = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers={"x-apisports-key": API_KEY},
            params={"league": 39, "season": 2023}
        )
        
        data = response.json()
        
        os.makedirs('/opt/airflow/raw_data', exist_ok=True)
        
        filepath = f"/opt/airflow/raw_data/fixtures_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {data['results']} fixtures to {filepath}")
        
        return filepath

    @task
    def transform_fixtures(filepath: str):
        with open(filepath, 'r') as f:
            raw = json.load(f)
        
        fixtures = []
        
        for fixture in raw['response']:
            fixtures.append({
                'fixture_id': fixture['fixture']['id'],
                'date': fixture['fixture']['date'],
                'home_team': fixture['teams']['home']['name'],
                'away_team': fixture['teams']['away']['name'],
                'home_goals': fixture['score']['fulltime']['home'],
                'away_goals': fixture['score']['fulltime']['away'],
                'status': fixture['fixture']['status']['short']
            })
        
        silver_path = filepath.replace('raw_data', 'silver_data').replace('.json', '_clean.json')
        os.makedirs(os.path.dirname(silver_path), exist_ok=True)
        
        with open(silver_path, 'w') as f:
            json.dump(fixtures, f, indent=2)
        
        print(f"Transformed {len(fixtures)} fixtures to {silver_path}")
        
        return silver_path

    @task
    def upload_to_azure(raw_path: str, silver_path: str):
        from azure.storage.filedatalake import DataLakeServiceClient

        connection_string = os.getenv("AZURE_CONNECTION_STRING")
        container_name = os.getenv("AZURE_CONTAINER_NAME")

        service_client = DataLakeServiceClient.from_connection_string(connection_string)
        filesystem_client = service_client.get_file_system_client(container_name)

        # Upload bronze file
        bronze_filename = os.path.basename(raw_path)
        bronze_client = filesystem_client.get_file_client(f"bronze/{bronze_filename}")
        with open(raw_path, 'r') as f:
            data = f.read()
        bronze_client.create_file()
        bronze_client.append_data(data, offset=0, length=len(data))
        bronze_client.flush_data(len(data))
        print(f"Uploaded bronze file: {bronze_filename}")

        # Upload silver file
        silver_filename = os.path.basename(silver_path)
        silver_client = filesystem_client.get_file_client(f"silver/{silver_filename}")
        with open(silver_path, 'r') as f:
            data = f.read()
        silver_client.create_file()
        silver_client.append_data(data, offset=0, length=len(data))
        silver_client.flush_data(len(data))
        print(f"Uploaded silver file: {silver_filename}")

        return f"Uploaded {bronze_filename} and {silver_filename} to Azure"
    @task
    def load_to_postgres(silver_path: str):
        import psycopg2
        import json
        
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        db = os.getenv("POSTGRES_DB")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=db,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_fixtures (
                fixture_id INTEGER,
                date TEXT,
                home_team TEXT,
                away_team TEXT,
                home_goals INTEGER,
                away_goals INTEGER,
                status TEXT
            )
        """)
        
        # Clear existing data
        cursor.execute("TRUNCATE TABLE raw_fixtures")
        
        # Load silver data
        with open(silver_path, 'r') as f:
            fixtures = json.load(f)
        
        for fixture in fixtures:
            cursor.execute("""
                INSERT INTO raw_fixtures VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                fixture['fixture_id'],
                fixture['date'],
                fixture['home_team'],
                fixture['away_team'],
                fixture['home_goals'],
                fixture['away_goals'],
                fixture['status']
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Loaded {len(fixtures)} fixtures into PostgreSQL")
        return len(fixtures)

    raw_path = fetch_fixtures()
    silver_path = transform_fixtures(raw_path)
    upload_to_azure(raw_path, silver_path)
    load_to_postgres(silver_path)
football_pipeline()