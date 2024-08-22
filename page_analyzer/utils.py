from urllib.parse import urlparse

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
