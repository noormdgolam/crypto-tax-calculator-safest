# Extended Car Warranty Hub - Static Site Generator

This is a custom Python-based static site generator for the Extended Car Warranty Hub, optimized for SEO, Google AdSense, and ultra-fast Core Web Vitals.

## Requirements
- Python 3.9+

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `.\venv\Scripts\activate` (Windows)
3. Install requirements: `pip install -r _src/requirements.txt`

## Working with Content
- All source code and templates are in the `_src` folder.
- Run `cd _src && python generate_content.py` to regenerate the dummy articles and configurations.

## Building the Site
1. From the `_src` directory, run: `python generate_site.py`
2. The site will be built in the root directory (one level above `_src`).

## Deploying
- The site is configured for cPanel Git deployment. 
- Commit all changes (including the generated HTML files in the root) and push to the cPanel remote.
- The `.cpanel.yml` file handles moving the files to the correct `public_html` subdomain folder.

## Configuration Items to Update Later
- In `_src/_templates/base.html` and `_src/_templates/article.html`: Update the `ca-pub-XXXXXXXXXXXXXXXX` and `data-ad-slot` placeholders with your actual AdSense publisher ID.
- In `_src/_templates/base.html`: Update the Google Analytics `G-XXXXXXXXXX` placeholders.
- Connect the newsletter forms in `_src/_templates/base.html` and `_src/_templates/article.html` to a real email provider (e.g., Mailchimp, ConvertKit).
