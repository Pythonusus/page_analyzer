import os
from datetime import date as dt

from dotenv import load_dotenv
from psycopg2 import connect, extras

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def exec_query(query, params=None):
    with connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute(query, params)
            data = cur.fetchall()
    conn.close()
    return data


def find_url_by_name(url):
    query_result = exec_query("SELECT * FROM urls WHERE name = %s;", (url,))
    return query_result[0] if query_result else None


def find_url_by_id(url_id):
    query_result = exec_query("SELECT * FROM urls WHERE id = %s;", (url_id,))
    return query_result[0] if query_result else None


def get_all_urls():
    query = """
        WITH last_checks AS (
        SELECT *
        FROM url_checks AS checks1
        WHERE checks1.id = (
            SELECT MAX(checks2.id)
            FROM url_checks AS checks2
            WHERE checks1.url_id = checks2.url_id
            )
        )

        SELECT
            urls.id,
            urls.name,
            last_checks.status_code,
            last_checks.created_at AS last_check
        FROM urls
        LEFT JOIN last_checks ON urls.id = last_checks.url_id
        ORDER BY urls.id DESC;
    """
    query_result = exec_query(query)
    return query_result


def get_all_url_checks(url_id):
    query_result = exec_query(
        "SELECT * FROM url_checks WHERE url_id = %s;",
        (url_id,)
    )
    return query_result


def add_url_to_db(url):
    query = """
        INSERT INTO urls (name, created_at)
        VALUES (%(name)s, %(date)s)
        RETURNING id;
    """

    query_result = exec_query(query, {"name": url, "date": dt.today()})
    url_id = query_result[0].id
    return url_id


def add_check_to_db(url_id, status_code, data):
    query = """
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
        RETURNING id;
    """

    params = {
        "url_id": url_id,
        "status_code": status_code,
        "h1": data.get("h1"),
        "title": data.get("title"),
        "description": data.get("description"),
        "created_at": dt.today()
    }

    query_result = exec_query(query, params)
    check_id = query_result[0].id
    return check_id
