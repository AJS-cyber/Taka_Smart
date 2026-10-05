"""Small, dependency-free online knowledge client for TakaSmart."""

import json
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


LANGUAGES = {"sw": "sw", "en": "en", "fr": "fr"}


def _request_json(url):
    request = Request(url, headers={"User-Agent": "TakaSmart/1.0 (waste education platform)"})
    with urlopen(request, timeout=4) as response:
        return json.loads(response.read().decode("utf-8"))


def search_knowledge(query, lang="sw"):
    """Find a short, attributed public reference; return None on any failure."""
    query = re.sub(r"\s+", " ", str(query or "")).strip()
    if len(query) < 3:
        return None
    language = LANGUAGES.get(lang, "en")
    params = urlencode({
        "action": "query", "list": "search", "srsearch": query,
        "srlimit": 1, "format": "json", "utf8": 1
    })
    try:
        result = _request_json(f"https://{language}.wikipedia.org/w/api.php?{params}")
        hits = result.get("query", {}).get("search", [])
        if not hits:
            return None
        title = hits[0].get("title")
        if not title:
            return None
        summary = _request_json(
            f"https://{language}.wikipedia.org/api/rest_v1/page/summary/"
            f"{title.replace(' ', '_')}"
        )
        extract = re.sub(r"\s+", " ", summary.get("extract", "")).strip()
        if not extract:
            return None
        return {
            "title": title,
            "extract": extract[:900],
            "url": summary.get("content_urls", {}).get("desktop", {}).get("page")
            or f"https://{language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
        }
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, OSError):
        return None
