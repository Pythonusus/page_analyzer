import os
from datetime import date as dt

from psycopg2 import connect, extras
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def add_url_to_db(url):
    with connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute(
                """
                INSERT INTO urls (name, created_at)
                VALUES (%(str)s, %(date)s)
                RETURNING id;
                """,
                {"name": url, "date": dt.today().isoformat()},
            )
            url_id = cur.fetchone().id
    conn.close()
    return url_id
