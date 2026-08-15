from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator # Di Airflow 3.x path operator standar diperbarui
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests

def fetch_and_store_posts():
    current_offset = int(Variable.get("post_offset", default_var=0))
    limit = 10
    
    url = f"https://jsonplaceholder.typicode.com/posts?_start={current_offset}&_limit={limit}"
    response = requests.get(url)
    posts = response.json()
    
    if not posts:
        print("Data sudah habis ditarik semua.")
        return

    # Menghubungkan ke PostgreSQL menggunakan koneksi ID default
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Membuat tabel otomatis dengan kolom waktu penarikan
    create_table_query = """
        CREATE TABLE IF NOT EXISTS api_posts (
            id INT PRIMARY KEY,
            user_id INT,
            title VARCHAR(255),
            body TEXT,
            waktu_penarikan TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    pg_hook.run(create_table_query)
    
    insert_query = """
        INSERT INTO api_posts (id, user_id, title, body)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """
    
    for post in posts:
        pg_hook.run(insert_query, parameters=(post['id'], post['userId'], post['title'], post['body']))
        
    Variable.set("post_offset", current_offset + limit)

default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2026, 8, 15),
    'retries': 1,
}

with DAG('fetch_posts_pipeline', default_args=default_args, schedule_interval='*/10 * * * *', catchup=False) as dag:
    PythonOperator(
        task_id='fetch_and_store', 
        python_callable=fetch_and_store_posts
    )