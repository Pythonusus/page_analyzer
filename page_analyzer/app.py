from flask import Flask, make_response, render_template

app = Flask(__name__)


# Обработчик главной страницы
@app.route("/")
def index():
    return render_template("index.html")


# Обработчик загрузки статики
@app.route("/<file>")
def get_static(file):
    with open(f"page_analyzer/static/{file}", mode="rb") as f:
        logo = f.read()
    res = make_response(logo)
    res.headers["Content-Type"] = "image/png"
    return res
