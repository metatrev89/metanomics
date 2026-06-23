#!/usr/bin/env python3
"""
Ping all search engines and AI crawlers after publishing content.
Notifies Bing (via IndexNow) and Google (via sitemap ping).

Usage:
    python3 scripts/ping_all.py
"""

import sys
import os

# Allow imports from the scripts directory
sys.path.insert(0, os.path.dirname(__file__))

from ping_bing import ping_indexnow, get_urls_from_sitemap
from ping_google import ping_google

SITEMAP_URL = "https://www.metanomics.org/sitemap.xml"

print("=" * 50)
print("  Metanomics — Search Engine Ping")
print("=" * 50)

print("\n[1/2] Bing / IndexNow")
print("-" * 30)
urls = get_urls_from_sitemap(SITEMAP_URL)
if urls:
    ping_indexnow(urls)

print("\n[2/2] Google")
print("-" * 30)
ping_google()

print("\n" + "=" * 50)
print("  Done. All engines notified.")
print("=" * 50)
