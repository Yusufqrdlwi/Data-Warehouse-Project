from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests
import pendulum  # Digunakan untuk mengatur timezone secara akurat

def fetch_and_store_posts():
    # Ambil offset saat ini, mulai dari 0 jika belum ada
    current_offset = int(Variable.get("post_offset", default_var=0))
    limit = 10
    
    # 1. Parameterized URL (Tetap dipertahankan dari tugas sebelumnya)
    base_url = "https://jsonplaceholder.typicode.com/posts"
    api_params = {
        "_start": current_offset,
        "_limit": limit
    }
    
    response = requests.get(base_url, params=api_params)
    posts = response.json()
    
    if not posts:
        print("Data habis.")
        return

    # Mendapatkan waktu saat ini langsung dalam format WIB (Asia/Jakarta)
    waktu_sekarang_wib = pendulum.now('Asia/Jakarta').to_datetime_string()

    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # 2. Pembuatan Tabel (Memastikan PRIMARY KEY terpasang)
    create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT PRIMARY KEY,
            user_id INT,
            title VARCHAR(255),
            body TEXT,
            waktu_penarikan TIMESTAMP
        );
    """
    pg_hook.run(create_table_query)
    
    # 3. LOGIC DATABASE-LEVEL VALIDATION (ANTI-DUPLIKASI)
    # Menggunakan klausa 'ON CONFLICT (id) DO NOTHING'
    # Jika database mendeteksi ID yang sama masuk, database yang akan MENOLAKNYA secara otomatis.
    insert_query = """
        INSERT INTO transactions (id, user_id, title, body, waktu_penarikan)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """
    
    # Di level Python, kita hanya melakukan satu kali perintah eksekusi batch/loop
    # tanpa perlu melakukan query SELECT nge-cek satu-satu ke DB lagi.
    for post in posts:
        pg_hook.run(
            insert_query, 
            parameters=(post['id'], post['userId'], post['title'], post['body'], waktu_sekarang_wib)
        )
        
    # Tambah offset untuk penarikan 10 menit berikutnya
    Variable.set("post_offset", current_offset + limit)

# Mengatur start_date DAG agar menggunakan timezone Asia/Jakarta (WIB)
local_tz = pendulum.timezone("Asia/Jakarta")
default_args = {
    'owner': 'data_engineer', 
    'start_date': datetime(2026, 8, 15, tzinfo=local_tz)
}

with DAG('fetch_posts_pipeline', default_args=default_args, schedule_interval='*/10 * * * *', catchup=False) as dag:
    PythonOperator(task_id='fetch_and_store', python_callable=fetch_and_store_posts)