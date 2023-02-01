# importing psycopg2
import sys

import psycopg2
from decouple import config
"""
Drop all tables of database you given.
"""

try:
    conn = psycopg2.connect(
        database=config('POSTGRES_DB'),
        user=config('POSTGRES_USER'),
        password=config('POSTGRES_PASSWORD'),
        host=config('HOST'),
        port=config('PORT')
    )
    conn.set_isolation_level(0)
except Exception:
    print("Unable to connect to the database.")

cur = conn.cursor()

try:
    cur.execute(
        "SELECT table_schema,table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' ORDER BY table_schema,table_name"
    )
    rows = cur.fetchall()
    for row in rows:
        print("dropping table: ", row[1])
        cur.execute(f"drop table {row[1]} cascade")
    cur.close()
    conn.close()
except Exception:
    print("Error: ", sys.exc_info()[1])
