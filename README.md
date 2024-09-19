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

### Installing

1. Clone GitHub repo:
```
git clone https://github.com/Pythonusus/python-project-83
```

2. Provide SECRET_KEY environmental variable to secure your data:
```
export SECRET_KEY=yourveryhardtobreakpassword
```

3. Provide DATABASE_URL environmental variable to connect to your PostgreSQL database:
```
export DATABASE_URL={provider}://{user}:{password}@{host}:{port}/{db}
```

3. Install all neccessary dependencies using Poetry and connect to DB via pysql utility:
```
make build
```

4. Start Page analyzer locally:
```
make start
```

<a name = "built_using"></a>
## ⛏️ Built Using

- [Poetry](https://python-poetry.org) - Python packaging and dependency management tool
- [PostgreSQL](https://www.postgresql.org/) - Powerful, open source object-relational database system
- [Flask](https://pypi.org/project/Flask/) - Lightweight WSGI web application framework
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP Server for UNIX

<a name = "authors"></a>
## ✍️ Authors

[@Pythonusus](https://github.com/Pythonusus)

<a name = "logo"></a>
## Logo
Made with [Ideogram AI](https://ideogram.ai/)

Stored at [imgur.com](https://imgur.com/)
