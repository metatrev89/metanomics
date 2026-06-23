#!/usr/bin/env python3
"""
Ping Bing (and other IndexNow-compatible engines) with all site URLs.
Run this after publishing new content to speed up indexing.

Usage:
    python3 scripts/ping_bing.py
"""

import json
import urllib.request
import xml.etree.ElementTree as ET

# IndexNow config
KEY = "8c654cb410ed47b9a1b9524a18dde924"
HOST = "www.metanomics.org"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"


def get_urls_from_sitemap(sitemap_url):
    """Fetch and parse sitemap, return list of URLs."""
    print(f"Fetching sitemap: {sitemap_url}")
    with urllib.request.urlopen(sitemap_url) as response:
        content = response.read()
    root = ET.fromstring(content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall("sm:url/sm:loc", ns)]
    return urls


def ping_indexnow(urls):
    """Submit URLs to IndexNow API."""
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    print(f"\nSubmitting {len(urls)} URL(s) to IndexNow...")
    for url in urls:
        print(f"  {url}")
    with urllib.request.urlopen(req) as response:
        status = response.status
    print(f"\nResponse: HTTP {status}")
    if status == 200:
        print("Success — Bing has been notified.")
    elif status == 202:
        print("Accepted — URLs queued for crawling.")
    else:
        print(f"Unexpected status code: {status}")


if __name__ == "__main__":
    urls = get_urls_from_sitemap(SITEMAP_URL)
    if not urls:
        print("No URLs found in sitemap.")
    else:
        ping_indexnow(urls)
