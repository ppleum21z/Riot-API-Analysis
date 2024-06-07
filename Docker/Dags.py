from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import pendulum
from Match_history import getmatch
import os
from airflow.providers.mysql.operators.mysql import MySqlOperator

def read_sql_file(sql_file):
    with open(sql_file, 'r') as file:
        return file.read()
    
sql_file_dir = "/opt/airflow/sql/"

create_song_sql = read_sql_file(os.path.join(sql_file_dir, "CreateSongTable.sql"))
create_artist_sql = read_sql_file(os.path.join(sql_file_dir, "CreateArtistTable.sql"))
create_album_sql = read_sql_file(os.path.join(sql_file_dir, "CreateAlbumTable.sql"))
insert_song_sql = read_sql_file(os.path.join(sql_file_dir , "InsertSong.sql" ))
insert_artist_sql = read_sql_file(os.path.join(sql_file_dir , "InsertArtist.sql" ))
insert_album_sql = read_sql_file(os.path.join(sql_file_dir , "Insertalbum.sql" ))

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2019, 11, 30),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG(
    dag_id="My_matchhistory",
    schedule_interval="0 0 * * *",  # Daily schedule
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    default_args=default_args,
    tags=["lolmatch"]
) as dag:

    t1 = PythonOperator(
        task_id='get_data_lol',
        python_callable=getmatch
    )


t1 


