<div align="center">

<img width=300px height=300px src="https://i.imgur.com/LSullCZ.jpeg" alt="Page analyzer logo">

# Page analyzer

### Hexlet tests and maintainability status:
[![Actions Status](https://github.com/Pythonusus/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pythonusus/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c0b8636dbde831224ab2/maintainability)](https://codeclimate.com/github/Pythonusus/python-project-83/maintainability)

</div>

## 🔗 Link to web-service
[Try Page analyzer by this link](https://python-project-83-0p8a.onrender.com/)

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Built Using](#built_using)
- [Authors](#authors)
- [Logo](#logo)

<a name = "about"></a>
## 🧐 About

Page Analyzer is a simple Flask web-application that checks sites for SEO suitability

<a name = "getting_started"></a>
## 🏁 Getting Started

### Prerequisites

1. python >= 3.10
2. flask >= 3.0.3
3. gunicorn >= 22.0.0
4. python-dotenv >= 1.0.1
5. psycopg2-binary >= 2.9.9
6. validators >= 0.33.0
7. beautifulsoup4 >= 4.12.3
8. requests >= 2.32.3

### Installing with Docker
1. Clone GitHub repo:
```
git clone https://github.com/Pythonusus/page_analyzer.git
```
2. Install Docker using [official guide](https://docs.docker.com/desktop/)

3. Provide all neccessary environmental variables. You can see example of .env file in [.env.example](https://github.com/Pythonusus/python-project-83/blob/main/.env.example) file.

4. Build and run the Docker container:
```
make docker-build-prod
make docker-start-prod
```
The application will be available at http://localhost:8000


### Installing without Docker

1. Clone GitHub repo:
```
git clone https://github.com/Pythonusus/python-project-83
```

2. Provide all neccessary environmental variables. You can see example of .env file in [.env.example](https://github.com/Pythonusus/python-project-83/blob/main/.env.example) file.

3. Install Poetry and config it:
```
sudo apt-get update && \
     apt-get install -y curl build-essential libpq-dev && \
     rm -rf /var/lib/apt/lists/* && \
     curl -sSL https://install.python-poetry.org | python3 - && \
     poetry config virtualenvs.in-project true
```

4. Install all neccessary dependencies using Poetry and connect to DB via pysql utility:
```
make build
```

5. Start Page analyzer locally:
```
make start
```

<a name = "built_using"></a>
## ⛏️ Built Using

- [Poetry](https://python-poetry.org) - Python packaging and dependency management tool
- [PostgreSQL](https://www.postgresql.org/) - Powerful, open source object-relational database system
- [Flask](https://pypi.org/project/Flask/) - Lightweight WSGI web application framework
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP Server for UNIX
- [Docker](https://www.docker.com/) - Open platform for building, shipping, and running applications

<a name = "authors"></a>
## ✍️ Authors

[@Pythonusus](https://github.com/Pythonusus)

<a name = "logo"></a>
## Logo
Made with [Ideogram AI](https://ideogram.ai/)

Stored at [imgur.com](https://imgur.com/)
