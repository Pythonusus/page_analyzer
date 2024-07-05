from flask import Flask

app = Flask(__name__)


# Обработчик главной страницы
@app.route('/')
def index():
    return 'Hello, World!'
