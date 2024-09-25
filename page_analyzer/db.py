"""Utilities to work with database."""

from datetime import date as dt

from psycopg2 import connect, extras


def connect_to_db(app):
    return connect(app.config.get("DATABASE_URL"))


def exec_query(conn, query, params=None):
    """
    General function to execute SQL queries.

    Args:
        conn (connection obj): DB connection
        query (str): SQL query
        params (tuple or dict, optional): Query params. Defaults to None

    Returns:
        list of tuples: Query result data
    """
    with conn:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute(query, params)
            data = cur.fetchall()
    return data


def find_url_by_name(conn, url):
    result = exec_query(conn, "SELECT * FROM urls WHERE name = %s;", (url,))
    return result[0] if result else None


def find_url_by_id(conn, url_id):
    result = exec_query(conn, "SELECT * FROM urls WHERE id = %s;", (url_id,))
    return result[0] if result else None


def get_all_urls(conn):
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
    result = exec_query(conn, query)
    return result


def get_all_url_checks(conn, url_id):
    result = exec_query(
        conn,
        "SELECT * FROM url_checks WHERE url_id = %s;",
        (url_id,)
    )
    return result


def add_url_to_db(conn, url):
    query = """
        INSERT INTO urls (name, created_at)
        VALUES (%(name)s, %(date)s)
        RETURNING id;
    """

    result = exec_query(conn, query, {"name": url, "date": dt.today()})
    url_id = result[0].id
    return url_id


def add_check_to_db(conn, url_id, status_code, data):
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

    result = exec_query(conn, query, params)
    check_id = result[0].id
    return check_id
