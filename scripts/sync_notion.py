#!/usr/bin/env python3
"""
Metanomics — Notion Blog Sync Script
Fetches published posts from a Notion database and generates static HTML.

Required env vars (set as GitHub Secrets):
  NOTION_API_KEY      — your Notion integration token
  NOTION_DATABASE_ID  — the ID of your blog posts database

Notion database should have these properties:
  Title   (title)
  Status  (select)   — "Published" to go live
  Date    (date)
  Excerpt (rich_text)
  Slug    (rich_text) — URL-friendly name e.g. "my-post-title"
  Cover   (url)       — optional cover image URL
"""

import os
import re
import json
import html
import requests
from pathlib import Path
from datetime import datetime

# ── Config ─────────────────────────────────────────────────────────────────
NOTION_API_KEY     = os.environ.get("NOTION_API_KEY", "")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "")

if not NOTION_API_KEY or not NOTION_DATABASE_ID:
    raise SystemExit("ERROR: NOTION_API_KEY and NOTION_DATABASE_ID must be set.")

SITE_ROOT  = Path(__file__).parent.parent
POSTS_DIR  = SITE_ROOT / "posts"
POSTS_DIR.mkdir(exist_ok=True)

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def notion_query_database(database_id, filter_=None, sorts=None):
    """Query a Notion database, returning all results (handles pagination)."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    body = {}
    if filter_:
        body["filter"] = filter_
    if sorts:
        body["sorts"] = sorts
    results = []
    while True:
        resp = requests.post(url, headers=NOTION_HEADERS, json=body)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        body["start_cursor"] = data["next_cursor"]
    return results

def notion_get_block_children(block_id, start_cursor=None):
    """Fetch one page of block children."""
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    params = {}
    if start_cursor:
        params["start_cursor"] = start_cursor
    resp = requests.get(url, headers=NOTION_HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()

# ── Helpers ─────────────────────────────────────────────────────────────────
def plain_text(rich_text_arr: list) -> str:
    return "".join(t.get("plain_text", "") for t in rich_text_arr)

def rich_text_to_html(rich_text_arr: list) -> str:
    out = ""
    for t in rich_text_arr:
        content = html.escape(t.get("plain_text", ""))
        ann = t.get("annotations", {})
        href = t.get("href")
        if ann.get("code"):        content = f"<code>{content}</code>"
        if ann.get("bold"):        content = f"<strong>{content}</strong>"
        if ann.get("italic"):      content = f"<em>{content}</em>"
        if ann.get("strikethrough"): content = f"<del>{content}</del>"
        if ann.get("underline"):   content = f"<u>{content}</u>"
        if href:                   content = f'<a href="{html.escape(href)}">{content}</a>'
        out += content
    return out

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text

def format_date(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str.split("T")[0])
        return dt.strftime("%B %-d, %Y")
    except Exception:
        return date_str

# ── Blocks → HTML ────────────────────────────────────────────────────────────
def blocks_to_html(blocks: list) -> str:
    out = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        btype = b.get("type", "")
        data  = b.get(btype, {})

        if btype == "paragraph":
            text = rich_text_to_html(data.get("rich_text", []))
            if text.strip():
                out.append(f"<p>{text}</p>")

        elif btype == "heading_1":
            text = rich_text_to_html(data.get("rich_text", []))
            out.append(f"<h1>{text}</h1>")

        elif btype == "heading_2":
            text = rich_text_to_html(data.get("rich_text", []))
            out.append(f"<h2>{text}</h2>")

        elif btype == "heading_3":
            text = rich_text_to_html(data.get("rich_text", []))
            out.append(f"<h3>{text}</h3>")

        elif btype == "bulleted_list_item":
            items = []
            while i < len(blocks) and blocks[i].get("type") == "bulleted_list_item":
                t = rich_text_to_html(blocks[i]["bulleted_list_item"].get("rich_text", []))
                items.append(f"  <li>{t}</li>")
                i += 1
            out.append("<ul>\n" + "\n".join(items) + "\n</ul>")
            continue

        elif btype == "numbered_list_item":
            items = []
            while i < len(blocks) and blocks[i].get("type") == "numbered_list_item":
                t = rich_text_to_html(blocks[i]["numbered_list_item"].get("rich_text", []))
                items.append(f"  <li>{t}</li>")
                i += 1
            out.append("<ol>\n" + "\n".join(items) + "\n</ol>")
            continue

        elif btype == "quote":
            text = rich_text_to_html(data.get("rich_text", []))
            out.append(f"<blockquote>{text}</blockquote>")

        elif btype == "callout":
            text = rich_text_to_html(data.get("rich_text", []))
            icon = data.get("icon", {}).get("emoji", "")
            out.append(f'<blockquote class="callout">{icon} {text}</blockquote>')

        elif btype == "divider":
            out.append("<hr>")

        elif btype == "image":
            img_data = data
            if img_data.get("type") == "file":
                url = img_data["file"]["url"]
            elif img_data.get("type") == "external":
                url = img_data["external"]["url"]
            else:
                url = ""
            caption = plain_text(img_data.get("caption", []))
            safe_url = html.escape(url)
            safe_cap = html.escape(caption)
            out.append(
                f'<figure><img src="{safe_url}" alt="{safe_cap}" loading="lazy">'
                f"<figcaption>{safe_cap}</figcaption></figure>"
            )

        elif btype == "code":
            text = html.escape(plain_text(data.get("rich_text", [])))
            lang = data.get("language", "")
            out.append(f'<pre><code class="language-{lang}">{text}</code></pre>')

        elif btype == "video":
            if data.get("type") == "external":
                url = data["external"]["url"]
                safe_url = html.escape(url)
                out.append(f'<p><a href="{safe_url}" target="_blank" rel="noopener">[Video: {safe_url}]</a></p>')

        elif btype == "bookmark":
            url = data.get("url", "")
            safe_url = html.escape(url)
            caption = plain_text(data.get("caption", []))
            label = html.escape(caption) if caption else safe_url
            out.append(f'<p><a href="{safe_url}" target="_blank" rel="noopener">{label}</a></p>')

        i += 1

    return "\n".join(out)

# ── Post HTML template ───────────────────────────────────────────────────────
def post_html(title, date_str, author, content_html, cover_url, slug, excerpt):
    cover_tag = (
        f'<div class="post-cover-wrap"><img class="post-cover" src="{html.escape(cover_url)}" alt="{html.escape(title)}" loading="lazy"></div>'
        if cover_url else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} | Metanomics</title>
  <meta name="description" content="{html.escape(excerpt[:160]) if excerpt else html.escape(title)}">

  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(excerpt[:200]) if excerpt else ''}">
  <meta property="og:image" content="{html.escape(cover_url) if cover_url else 'https://static.wixstatic.com/media/2d97c8_ac118d96d2d9410893ea007048192f3d~mv2.png'}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Metanomics">

  <link rel="icon" type="image/png" href="../assets/images/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

<nav class="site-nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-brand">
      <img class="nav-logo"
        src="../assets/images/logo.png"
        alt="Metanomics Logo" width="44" height="44">
      <div class="nav-brand-text">
        <span class="nav-title">Metanomics</span>
        <span class="nav-subtitle">Reverse Engineering The Economy of Zion</span>
      </div>
    </a>
    <div class="nav-links">
      <a href="../index.html">Home</a>
      <a href="../blog.html" class="active">Blog</a>
    </div>
    <button class="nav-menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <line x1="3" y1="6" x2="21" y2="6"/>
        <line x1="3" y1="12" x2="21" y2="12"/>
        <line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
    </button>
  </div>
</nav>
<div class="nav-mobile" id="mobileNav">
  <a href="../index.html" onclick="closeMenu()">Home</a>
  <a href="../blog.html" onclick="closeMenu()">Blog</a>
</div>

<div class="page-body">
  <section class="post-hero">
    <div class="container">
      <a class="post-back" href="../blog.html">&larr; All Posts</a>
      <h1>{html.escape(title)}</h1>
      <div class="post-meta">
        <span class="post-meta-date">{html.escape(date_str)}</span>
        <span class="post-meta-author">by {html.escape(author)}</span>
      </div>
    </div>
  </section>

  {cover_tag}

  <section class="post-content-section">
    <div class="container">
      <article class="post-content">
        {content_html}
      </article>

      <div style="margin-top:4rem; padding-top:2rem; border-top:1px solid var(--border); text-align:center;">
        <a class="post-back" href="../blog.html">&larr; Back to All Posts</a>
      </div>
    </div>
  </section>
</div>

<footer class="site-footer">
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand-col">
        <img class="footer-logo"
          src="../assets/images/logo.png"
          alt="Metanomics" width="56" height="56" loading="lazy">
        <p class="footer-site-name">Metanomics</p>
        <p class="footer-tagline">Reverse Engineering The Economy of Zion</p>
      </div>
      <div class="footer-newsletter-col">
        <h4>Remembrance Newsletter</h4>
        <p>Stay connected with new insights, blog posts, and updates.</p>
        <form class="newsletter-form-inline" id="footer-subscribe-form">
          <input type="email" name="email" placeholder="your@email.com" required aria-label="Email address">
          <button type="submit">Subscribe</button>
        </form>
        <div class="subscribe-msg" id="footer-msg" aria-live="polite"></div>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="footer-copy">&copy; 2026 by High Noon Product. All rights reserved.</p>
    </div>
  </div>
</footer>

<script>

  /* ---- Mobile Nav Active State ---- */
  (function() {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-mobile a').forEach(function(link) {
      const href = link.getAttribute('href');
      if (
        (href.includes('index.html') && (path === '/' || path.endsWith('/') || path.endsWith('index.html'))) ||
        (href.includes('blog.html') && path.endsWith('blog.html')) ||
        (href === '../index.html' && (path === '/' || path.endsWith('/') || path.endsWith('index.html')))
      ) {
        link.classList.add('active');
      }
    });
  })();

  const menuBtn = document.getElementById('menuBtn');
  const mobileNav = document.getElementById('mobileNav');
  menuBtn.addEventListener('click', () => {{
    const isOpen = mobileNav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', isOpen);
  }});
  function closeMenu() {{ mobileNav.classList.remove('open'); }}

  /* ---- Beehiiv Subscribe (via Cloudflare Worker proxy) ---- */
  const SUBSCRIBE_URL = 'https://metanomics-subscribe.trevorspencer89.workers.dev';
  async function subscribeToBeehiiv(email, msgId, btn) {{
    const msgEl = document.getElementById(msgId);
    const origText = btn.textContent;
    btn.disabled = true; btn.textContent = 'Subscribing…';
    msgEl.textContent = ''; msgEl.className = 'subscribe-msg';
    try {{
      const res = await fetch(SUBSCRIBE_URL, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ email }})
      }});
      if (res.ok) {{ msgEl.textContent = '✓ You\'re subscribed! Check your inbox.'; msgEl.classList.add('subscribe-success'); btn.form.reset(); }}
      else {{ throw new Error('failed'); }}
    }} catch {{ msgEl.textContent = 'Something went wrong. Please try again.'; msgEl.classList.add('subscribe-error'); btn.disabled = false; btn.textContent = origText; }}
  }}
  document.getElementById('footer-subscribe-form').addEventListener('submit', e => {{
    e.preventDefault();
    subscribeToBeehiiv(e.target.email.value, 'footer-msg', e.target.querySelector('button[type="submit"]'));
  }});
</script>
</body>
</html>"""

# ── Blog listing HTML ────────────────────────────────────────────────────────
def blog_card_html(title, date_str, excerpt, slug, cover_url):
    cover_block = (
        f'<img class="post-card-cover" src="{html.escape(cover_url)}" alt="{html.escape(title)}" loading="lazy">'
        if cover_url else
        """<div class="post-card-cover-placeholder">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M4 4h16v16H4V4zm2 4v10h12V8H6zm2 2h8v2H8v-2zm0 4h6v2H8v-2z"/>
        </svg>
      </div>"""
    )
    return f"""        <a class="post-card" href="posts/{html.escape(slug)}.html">
          {cover_block}
          <div class="post-card-body">
            <p class="post-card-date">{html.escape(date_str)}</p>
            <h2 class="post-card-title">{html.escape(title)}</h2>
            <p class="post-card-excerpt">{html.escape(excerpt)}</p>
            <span class="post-card-link">Read More &rarr;</span>
          </div>
        </a>"""

# ── Main sync ────────────────────────────────────────────────────────────────
def main():
    print(f"Fetching posts from Notion database {NOTION_DATABASE_ID}...")

    # Query only Published posts, newest first
    pages = notion_query_database(
        NOTION_DATABASE_ID,
        filter_={"property": "Status", "select": {"equals": "Published"}},
        sorts=[{"property": "Date", "direction": "descending"}],
    )
    print(f"Found {len(pages)} published post(s).")

    cards = []

    for page in pages:
        props = page.get("properties", {})
        page_id = page["id"]

        # Extract properties
        title   = plain_text(props.get("Title", {}).get("title", []))
        excerpt = plain_text(props.get("Excerpt", {}).get("rich_text", []))
        slug    = plain_text(props.get("Slug", {}).get("rich_text", [])) or slugify(title)
        date_raw = (props.get("Date", {}).get("date") or {}).get("start", "")
        date_str = format_date(date_raw) if date_raw else "Undated"

        # Cover image: prefer the built-in Notion page cover (set via "Add cover"
        # at the top of any Notion page on mobile or desktop), then fall back to
        # the Cover URL property in the database.
        page_cover = page.get("cover") or {}
        if page_cover.get("type") == "external":
            cover_url = page_cover["external"]["url"]
        elif page_cover.get("type") == "file":
            cover_url = page_cover["file"]["url"]
        else:
            cover_url = props.get("Cover", {}).get("url", "") or ""

        if not title:
            print(f"  Skipping page {page_id} — no title.")
            continue

        print(f"  Processing: '{title}' ({slug})")

        # Fetch full page content (blocks), paginating if needed
        all_blocks = []
        cursor = None
        while True:
            result = notion_get_block_children(page_id, start_cursor=cursor)
            all_blocks.extend(result.get("results", []))
            if not result.get("has_more"):
                break
            cursor = result.get("next_cursor")

        content_html = blocks_to_html(all_blocks)

        # Write individual post file
        post_file = POSTS_DIR / f"{slug}.html"
        post_file.write_text(
            post_html(title, date_str, "Trevor Spencer", content_html, cover_url, slug, excerpt),
            encoding="utf-8"
        )
        print(f"    → Written: posts/{slug}.html")

        cards.append(blog_card_html(title, date_str, excerpt, slug, cover_url))

    # ── Regenerate blog.html grid ──
    blog_html_path = SITE_ROOT / "blog.html"
    if blog_html_path.exists():
        original = blog_html_path.read_text(encoding="utf-8")

        if cards:
            new_grid = (
                '<div class="posts-grid">\n\n'
                + "\n\n".join(cards)
                + "\n\n      </div>"
            )
        else:
            new_grid = '<div class="posts-grid"><p class="no-posts">No posts yet. Check back soon.</p></div>'

        # Replace between markers
        updated = re.sub(
            r"<!-- POSTS-START -->.*?<!-- POSTS-END -->",
            f"<!-- POSTS-START -->\n      {new_grid}\n      <!-- POSTS-END -->",
            original,
            flags=re.DOTALL,
        )
        blog_html_path.write_text(updated, encoding="utf-8")
        print(f"\nUpdated blog.html with {len(cards)} post card(s).")
    else:
        print("\nWARNING: blog.html not found — skipping grid update.")

    print("\nSync complete!")

if __name__ == "__main__":
    main()
