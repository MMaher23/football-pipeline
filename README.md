# Football Analytics Pipeline 🏆

An end-to-end data pipeline that ingests Premier League fixture data from a REST API, processes it through a medallion architecture, and stores it in a data warehouse for analytics.

## Architecture

## Tech Stack

- **Orchestration**: Apache Airflow
- **Containerization**: Docker
- **Cloud Storage**: Azure Data Lake Gen2
- **Data Warehouse**: PostgreSQL
- **Transformation**: dbt
- **Data Source**: API-Football (Premier League 2023)

## Setup

### Prerequisites
- Docker Desktop
- Python 3.x
- Azure account

### Installation

1. Clone the repo:
\```
git clone https://github.com/MMaher23/football-pipeline.git
cd football-pipeline
\```

2. Create virtual environment:
\```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\```

3. Set up environment variables:
\```
cp .env.example .env
\```
Fill in your API key and Azure credentials in `.env`

4. Start the pipeline:
\```
docker-compose up airflow-init
docker-compose up airflow-webserver airflow-scheduler postgres-dbt
\```

5. Access Airflow UI at `http://localhost:8080` (admin/admin)

6. Run dbt transformations:
\```
cd football_dbt
dbt run
\```

## Pipeline Stages

- **Bronze**: Raw JSON from API-Football stored locally and in Azure Data Lake
- **Silver**: Cleaned and flattened fixture data
- **Gold**: Aggregated analytics including winner, result type, and goal totals

## Key Features

- Fully orchestrated with Airflow DAGs
- Dockerized for portability
- Medallion architecture (Bronze/Silver/Gold)
- Cloud storage on Azure Data Lake Gen2
- SQL transformations with dbt