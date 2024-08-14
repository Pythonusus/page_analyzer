import os
from datetime import datetime as dt

import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def add_url_to_db(url):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO urls (name, created_at)
                VALUES (%(str)s, %(date)s)
                RETURNING id;
                """,
                {"name": url, "date": dt.now().isoformat()},
            )
            url_id = cur.fetchone()["id"]
    conn.close()
    return url_id
