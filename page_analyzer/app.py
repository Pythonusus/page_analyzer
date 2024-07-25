from flask import Flask, render_template

app = Flask(__name__)


# Обработчик главной страницы
@app.route("/")
def index():
    return render_template("index.html")
