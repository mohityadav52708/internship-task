from __future__ import annotations

import webbrowser
import urllib.parse


def open_url(url: str) -> str:
    # Basic normalization
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    webbrowser.open_new_tab(url)
    return f"Opened URL: {url}"


def search_web(query: str) -> str:
    encoded = urllib.parse.urlencode({"q": query})
    url = f"https://www.google.com/search?{encoded}"
    webbrowser.open_new_tab(url)
    return f"Searched the web for: {query}"