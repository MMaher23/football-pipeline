FROM apache/airflow:2.8.1

RUN pip install apache-airflow-providers-microsoft-azure \
    azure-storage-file-datalake \
    python-dotenv \
    requests


FROM apache/airflow:2.8.1

RUN pip install apache-airflow-providers-microsoft-azure \
    azure-storage-file-datalake \
    python-dotenv \
    requests \
    psycopg2-binary