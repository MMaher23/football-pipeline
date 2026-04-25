# ⚽ Football Analytics Pipeline

An end-to-end data engineering pipeline that ingests live Premier League data from a REST API, processes it through a medallion architecture, and serves analytics-ready data for dashboards.

## 🏗️ Architecture

```
Football API
     ↓
Airflow (Orchestration)
     ↓
Bronze Layer (Raw JSON → Local + Azure Data Lake)
     ↓
Silver Layer (Cleaned JSON → Local + Azure Data Lake)
     ↓
PostgreSQL (Structured Tables)
     ↓
dbt (SQL Transformations)
     ↓
Gold Layer (Analytics-Ready Tables)
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Apache Airflow | Pipeline orchestration and scheduling |
| Docker | Containerization and portability |
| Python | Data ingestion and transformation |
| Azure Data Lake Gen2 | Cloud storage (Bronze/Silver) |
| PostgreSQL | Data warehouse |
| dbt | SQL transformations (Gold layer) |
| Power BI | Dashboard and visualization |

## 📊 Medallion Architecture

- **Bronze** — Raw JSON responses from API-Football, stored locally and in Azure Data Lake
- **Silver** — Cleaned and flattened fixture data (nulls removed, nested JSON flattened)
- **Gold** — Aggregated analytics including winners, result types, and goal totals

## 🚀 Getting Started

### Prerequisites
- Docker Desktop
- Python 3.8+
- Git
- Azure account (for Data Lake)
- API-Football account (free tier)

### Installation

1. Clone the repo:
```bash
git clone https://github.com/MMaher23/football-pipeline.git
cd football-pipeline
```

2. Set up environment variables:
```bash
cp .env.example .env
```

Fill in your credentials in `.env`:
```
API_KEY=your_api_football_key
AZURE_CONNECTION_STRING=your_azure_connection_string
AZURE_CONTAINER_NAME=footballdata
POSTGRES_HOST=postgres-dbt
POSTGRES_PORT=5432
POSTGRES_DB=footballdw
POSTGRES_USER=dbtuser
POSTGRES_PASSWORD=dbtpassword
```

3. Start the pipeline:
```bash
docker-compose up airflow-init
docker-compose up airflow-webserver airflow-scheduler postgres-dbt
```

4. Access Airflow at `http://localhost:8080` (admin/admin) and trigger the DAG

5. Run dbt transformations:
```bash
cd football_dbt
dbt run
```

## 📁 Project Structure

```
football-pipeline/
├── dags/
│   └── football-pipeline.py    # Airflow DAG
├── football_dbt/
│   ├── models/
│   │   ├── silver_fixtures.sql  # Silver layer model
│   │   ├── gold_fixtures.sql    # Gold layer model
│   │   └── sources.yml          # Source definitions
│   └── dbt_project.yml
├── Dockerfile                   # Custom Airflow image
├── docker-compose.yml           # All services
├── requirements.txt
└── .env.example
```

## 📈 Sample Insights

- Manchester City and Arsenal tied on wins in PL 2023
- 82 draws across the season
- Newcastle's 8-0 win over Sheffield Utd was the biggest result

## 🔑 Key Concepts Demonstrated

- **Medallion Architecture** (Bronze/Silver/Gold)
- **Pipeline Orchestration** with Airflow DAGs
- **Containerization** with Docker
- **Cloud Storage** with Azure Data Lake Gen2
- **Data Transformation** with dbt
- **Incremental vs Full Load** patterns
- **Idempotent pipeline** design
- **Secrets management** with environment variables