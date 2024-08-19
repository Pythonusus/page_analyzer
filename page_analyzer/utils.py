from urllib.parse import urlparse, urlunparse
def normalize_url(url):
    return urlunparse(urlparse(url))
