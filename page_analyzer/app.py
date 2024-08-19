import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, make_response, render_template

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)


# Обработчик главной страницы
@app.route("/")
def index():
    return render_template("index.html")


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
