import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, make_response, render_template

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# Обработчик главной страницы
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
    error = validate_url(data)
    if error:
        flash(error, "danger")
        messages = get_flashed_messages()
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

    messages = get_flashed_messages()
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
