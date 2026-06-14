# Metanomics.org — Setup Guide

This guide walks you through getting the site live, connecting Notion as your blog CMS, and wiring up Beehiiv for your forms.

---

## Step 1 — Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in (or create a free account)
2. Click **New repository**
3. Name it `metanomics` (or `metanomics.org`)
4. Set it to **Public** (required for free GitHub Pages)
5. Click **Create repository**

---

## Step 2 — Upload the Site Files

**Option A — Drag & drop (easiest):**
1. Open your new repo on GitHub
2. Click **Add file → Upload files**
3. Drag the entire contents of your Metanomics project folder into the upload area
4. Click **Commit changes**

**Option B — GitHub Desktop app (recommended for ongoing use):**
1. Download [GitHub Desktop](https://desktop.github.com)
2. Clone your new repo
3. Copy all your site files into the cloned folder
4. Click **Commit to main** → **Push origin**

---

## Step 3 — Enable GitHub Pages

1. In your GitHub repo, click **Settings** → **Pages** (left sidebar)
2. Under **Source**, select **Deploy from a branch**
3. Branch: `main` | Folder: `/ (root)`
4. Click **Save**
5. After ~2 minutes, your site is live at `https://[your-github-username].github.io/metanomics`

---

## Step 4 — Point Your Domain (metanomics.org) to GitHub Pages

In your domain registrar (wherever you bought metanomics.org):

**Add these DNS records:**

| Type  | Name | Value                  |
|-------|------|------------------------|
| A     | @    | 185.199.108.153        |
| A     | @    | 185.199.109.153        |
| A     | @    | 185.199.110.153        |
| A     | @    | 185.199.111.153        |
| CNAME | www  | [your-username].github.io |

Then back in GitHub → Settings → Pages → Custom domain: enter `metanomics.org` and check **Enforce HTTPS**.

DNS changes take 10 min–48 hours to fully propagate.

---

## Step 5 — Set Up Notion as Your Blog CMS

### 5a — Create a Notion Integration

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **New integration**
3. Name it `Metanomics Blog`
4. Select your workspace
5. Click **Submit** → copy the **Internal Integration Token** (starts with `secret_`)

### 5b — Create Your Blog Database in Notion

1. In Notion, create a new page → choose **Table / Database**
2. Name it `Metanomics Blog Posts`
3. Add these properties (some may already exist):

| Property Name | Type       | Notes                          |
|---------------|------------|--------------------------------|
| Title         | Title      | (default — already exists)     |
| Status        | Select     | Add options: Draft, Published  |
| Date          | Date       | Publication date               |
| Excerpt       | Text       | Short summary (1-2 sentences)  |
| Slug          | Text       | URL slug e.g. `my-post-title`  |
| Cover         | URL        | Optional cover image URL       |

4. Click the `...` menu on the database page → **Add connections** → select `Metanomics Blog`
5. Copy the **Database ID** from the URL: `notion.so/[workspace]/[DATABASE-ID]?v=...`

### 5c — Write Your First Post

1. Add a new row to your database
2. Fill in Title, Excerpt, Slug (no spaces — use hyphens), Date
3. Set Status to **Published** when ready to go live
4. Write your blog content in the body of the page (click to open the row)
5. The GitHub Action will pick it up within the hour!

---

## Step 6 — Add Notion Secrets to GitHub

1. In your GitHub repo: **Settings → Secrets and variables → Actions**
2. Click **New repository secret** — add these two:

| Secret Name        | Value                              |
|--------------------|------------------------------------|
| NOTION_API_KEY     | Your integration token (secret_…)  |
| NOTION_DATABASE_ID | Your database ID                   |

---

## Step 7 — Manually Trigger a Sync (Test It)

1. In your GitHub repo, click **Actions** tab
2. Click **Sync Blog Posts from Notion**
3. Click **Run workflow** → **Run workflow**
4. Watch it run — it should pass ✅ and your blog will update

After this, it runs automatically every hour. When you publish a post in Notion, it goes live within ~60 minutes. You can also hit **Run workflow** manually anytime for instant publish.

---

## Step 8 — Connect Beehiiv Forms

### 8a — PDF Download Form

1. Log into [beehiiv.com](https://beehiiv.com)
2. Go to **Settings → Forms** → **Create new form**
3. Name it "Free PDF Download"
4. Customize fields: First Name, Last Name, Email
5. Click **Embed** → copy the `<iframe>` code
6. Open `index.html` in your project folder
7. Find the comment `<!-- PLACEHOLDER FORM — remove this and paste your Beehiiv <iframe> embed here -->`
8. Delete the entire `<form class="placeholder-form">` block and paste your Beehiiv iframe

**Set up the welcome email with your PDF link:**
1. In Beehiiv: **Settings → Welcome Email** → enable it
2. Write the email: include a button/link to your PDF (hosted on Google Drive, Dropbox, etc.)
   - Google Drive: upload PDF → right-click → Share → "Anyone with link" → copy link
3. Save and activate the welcome email

### 8b — Newsletter Footer Form

1. In Beehiiv: **Settings → Forms** → create another form (or use the same one)
2. Name it "Newsletter Signup"
3. Embed it in `index.html` (find `<!-- PASTE BEEHIIV NEWSLETTER EMBED HERE -->`)
4. Do the same for `blog.html` and the post template in `scripts/sync_notion.py`

---

## Step 9 — Download & Host Your Images Locally (Optional but Recommended)

The site currently loads the logo and book cover from the Wix CDN. To fully own all assets:

1. Visit your Wix site → right-click the logo image → **Save Image As** → save as `logo.png`
2. Save the book cover as `book-cover.jpg`
3. Put both in `assets/images/`
4. In `index.html`, replace the two Wix CDN URLs with `assets/images/logo.png` and `assets/images/book-cover.jpg`

---

## Publishing a Blog Post (Your Daily Workflow)

1. Open Notion on your phone (or desktop)
2. Go to your **Metanomics Blog Posts** database
3. Create a new row → fill in Title, Date, Excerpt, Slug
4. Write your post content in the page body
5. Set **Status → Published**
6. Wait up to 1 hour for auto-sync — OR go to GitHub Actions → **Run workflow** for instant publish

That's it. No code. No login to the site. Just Notion.

---

## File Structure Reference

```
metanomics.org/
├── index.html                  ← Main landing page
├── blog.html                   ← Blog listing (auto-regenerated)
├── assets/
│   ├── css/style.css           ← All styles
│   └── images/                 ← Book cover images
├── posts/                      ← Individual post pages (auto-generated)
├── scripts/
│   └── sync_notion.py          ← Notion sync script
└── .github/workflows/
    └── notion-sync.yml         ← GitHub Action
```

---

## Questions?

Feel free to come back and ask Claude to help with:
- Adding new sections to the site
- Changing colors or fonts
- Adding Google Analytics
- Troubleshooting the GitHub Action
