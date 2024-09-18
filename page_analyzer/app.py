import os

import psycopg2
import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for
)

from page_analyzer.db import (
    add_check_to_db,
    add_url_to_db,
    find_url_by_id,
    find_url_by_name,
    get_all_url_checks,
    get_all_urls
)
from page_analyzer.utils import normalize_url, parse_html, validate_url

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    """Show main page"""
    return render_template("index.html", messages=[], url="")


@app.route("/urls")
def show_urls_list():
    """Select all urls from DB and show them"""
    urls = get_all_urls()
    return render_template(
        "urls.html",
        urls=urls,
    )


@app.route("/urls/<url_id>")
def show_url_page(url_id):
    """
    Select specific url from DB by id.
    Show url's page.

    Args:
        url_id (str): url id in DB
    """
    messages = get_flashed_messages(with_categories=True)
    data = find_url_by_id(url_id)
    checks = get_all_url_checks(url_id)
    return render_template(
        "url.html",
        data=data,
        checks=checks,
        messages=messages
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
        messages = get_flashed_messages(with_categories=True)
        return (
            render_template(
                "index.html",
                url=url,
                messages=messages,
            ),
            422,
        )
    url = normalize_url(url)
    url_in_db = find_url_by_name(url)
    if url_in_db:
        url_id = url_in_db.id
        flash("Страница уже существует", "info")
    else:
        url_id = add_url_to_db(url)
        flash("Страница успешно добавлена", "success")

    return redirect(url_for("show_url_page", url_id=url_id))


@app.post("/urls/<url_id>/checks")
def post_check(url_id):
    """
    WRITE LATER
    """
    url = find_url_by_id(url_id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("show_url_page", url_id=url_id))

    status_code = response.status_code
    html = response.text
    data = parse_html(html)
    add_check_to_db(url_id, status_code, data)
    flash("Страница успешно проверена", "success")
    return redirect(url_for("show_url_page", url_id=url_id))


# Get png image from static
@app.route("/<image>")
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
