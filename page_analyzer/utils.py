from urllib.parse import urlparse, urlunparse

from validators import url as url_validator

MAX_URL_LENGTH = 255


def normalize_url(url):
    return urlunparse(urlparse(url))


def validate_url(url):
    if not url_validator(url):
        return "Некорректный URL"
    elif len(url) > MAX_URL_LENGTH:
        return "URL превышает 255 символов"
