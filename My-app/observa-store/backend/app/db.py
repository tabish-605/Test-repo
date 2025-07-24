# backend/app/db.py
import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres",
        database="ecommerce",
        user=os.environ.get("POSTGRES_USER", "user"),
        password=os.environ.get("POSTGRES_PASSWORD", "password")
    )
    return conn
