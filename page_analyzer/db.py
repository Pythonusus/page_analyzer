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
                VALUES (%(name)s, %(date)s)
                RETURNING id;
                """,
                {"name": url, "date": dt.today()},
            )
            url_id = cur.fetchone().id
    conn.close()
    return url_id


def find_url_by_name(url):
    with connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s;", (url,))
            data = cur.fetchone()
    conn.close()
    return data


def find_url_by_id(url_id):
    with connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s;", (url_id,))
            data = cur.fetchone()
    conn.close()
    return data


def get_all_urls():
    with connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls;")
            data = cur.fetchall()
    conn.close()
    return data


def add_check_to_db(url_id):
    with connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute(
                """
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description, created_at)
                VALUES (
                    %(url_id)s,
                    %(status_code)s,
                    %(h1)s,
                    %(title)s,
                    %(description)s,
                    %(created_at)s
                )
                RETURNING url_id;
                """,
                {
                    "url_id": url_id,
                    "status_code": None,
                    "h1": None,
                    "title": None,
                    "description": None,
                    "created_at": dt.today()
                }
            )
            url_id = cur.fetchone().url_id
    conn.close()
    return url_id


def get_all_url_checks(url_id):
    with connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute(
                "SELECT * FROM url_checks WHERE url_id = %s;",
                (url_id,)
            )
            data = cur.fetchall()
    conn.close()
    return data
