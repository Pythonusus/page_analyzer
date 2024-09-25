"""HTTP requests handlers."""

import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for
)

from page_analyzer import db
from page_analyzer.utils import normalize_url, parse_html, validate_url

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")


@app.get("/")
def index():
    """Show main page"""
    return render_template("index.html")


@app.get("/urls")
def show_urls_list():
    """Select all urls from DB and show them"""
    conn = db.connect_to_db()
    urls = db.get_all_urls(conn)
    conn.close()
    return render_template(
        "urls.html",
        urls=urls,
    )


@app.get("/urls/<url_id>")
def show_url_page(url_id):
    """
    Select specific url from DB by id.
    Show url's page.

    Args:
        url_id (str): url id in DB
    """

    conn = db.connect_to_db()
    data = db.find_url_by_id(conn, url_id)
    checks = db.get_all_url_checks(conn, url_id)
    conn.close()
    return render_template(
        "url.html",
        data=data,
        checks=checks,
    )


@app.post("/urls")
def submit_url():
    """
    Recieve url from form.
    Validate user data.
    If data has errors, flash error message.
    If no errors occured, check if url is present in DB.
    If url is present in DB, redirect to url page and flash info message.
    If url is not in DB, add url to DB, redirect to url page
    and flash success message.
    """
    data = request.form.to_dict()
    url = data.get("url")
    error = validate_url(url)
    if error:
        flash(error, "danger")

        return (
            render_template(
                "index.html",
                url=url,
            ),
            422,
        )
    url = normalize_url(url)
    conn = db.connect_to_db()
    url_in_db = db.find_url_by_name(conn, url)

    if url_in_db:
        url_id = url_in_db.id
        flash("Страница уже существует", "info")
    else:
        url_id = db.add_url_to_db(conn, url)
        flash("Страница успешно добавлена", "success")

    conn.close()
    return redirect(url_for("show_url_page", url_id=url_id))


@app.post("/urls/<url_id>/checks")
def post_check(url_id):
    """
    Find url in DB by given url_id.
    Perform SEO-analysis of given url.
    If error occures, redirect to url page and flash error message.
    If no errors occured, parse html from given url, add check to DB,
    redirect to url page and flash success message.
    """
    conn = db.connect_to_db()
    url = db.find_url_by_id(conn, url_id)
    try:
        response = requests.get(url.name, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "danger")
        conn.close()
        return redirect(url_for("show_url_page", url_id=url_id))

    status_code = response.status_code
    html = response.text
    data = parse_html(html)
    db.add_check_to_db(conn, url_id, status_code, data)
    flash("Страница успешно проверена", "success")
    conn.close()
    return redirect(url_for("show_url_page", url_id=url_id))


# Get png image from static
@app.get("/<image>")
def get_png_image(image):
    """
    Returns png image from static files.

    Args:
        image (str): file name

    Returns:
        Response obj: png image
    """
    with open(f"page_analyzer/static/{image}", mode="rb") as f:
        image = f.read()
    res = make_response(image)
    res.headers["Content-Type"] = "image/png"
    return res
