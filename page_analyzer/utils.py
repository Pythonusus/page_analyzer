"""Normalisation, validation and parsing utilities."""

from urllib.parse import urlparse

from bs4 import BeautifulSoup
from validators import url as url_validator

MAX_URL_LENGTH = 255


def normalize_url(url):
    data = urlparse(url)
    return f"{data.scheme}://{data.netloc}".lower()


def validate_url(url):
    if not url_validator(url):
        return "Некорректный URL"
    if len(url) > MAX_URL_LENGTH:
        return "URL превышает 255 символов"
    return None


def parse_html(html):
    """
    Parse h1, title, description content.

    Args:
        html (str): HTML string or an open filehandler

    Returns:
        dict: keys "h1", "title", "description" with parsed data or None
    """
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    h1 = soup.h1
    title = soup.title
    description = soup.find("meta", attrs={"name": "description"}) or {}
    data["h1"] = h1.string if h1 else None
    data["title"] = title.string if title else None
    data["description"] = description.get("content")
    return data
