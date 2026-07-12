import os
import json
import shutil
import datetime
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

# Paths
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(SRC_DIR, '_data')
TEMPLATES_DIR = os.path.join(SRC_DIR, '_templates')

# Create Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
env.filters['slugify'] = slugify

def load_data():
    with open(os.path.join(DATA_DIR, 'site.json'), 'r', encoding='utf-8') as f:
        site = json.load(f)
    with open(os.path.join(DATA_DIR, 'articles.json'), 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    site['year'] = datetime.datetime.now().year
    return site, articles

def create_static_pages(site, articles):
    # Base setup
    static_pages = [
        {
            "slug": "about-us",
            "title": "About Us",
            "meta_description": "Learn more about Crypto Tax Calculator Guide and our mission to provide the best tax reporting strategies.",
            "content": f"""
            <h2>Who We Are</h2>
            <p>Crypto Tax Calculator Guide is a premier resource dedicated to helping US crypto investors navigate the complex world of tax reporting and compliance.</p>
            <h2>Our Mission</h2>
            <p>Our mission is simple: to provide actionable, trustworthy information that helps you navigate complex tax regulations, minimize audit risks, and utilize safe API integrations for your crypto portfolio.</p>
            <div class="author-bio-box" style="margin-top: 30px;">
                <img src="/assets/images/author.svg" alt="{site['author']['name']}" class="author-avatar" width="80" height="80">
                <div class="bio-text">
                    <h4>{site['author']['name']}</h4>
                    <p>{site['author']['bio']}</p>
                </div>
            </div>
            """
        },
        {
            "slug": "contact",
            "title": "Contact Us",
            "meta_description": "Get in touch with the Crypto Tax Calculator Guide team.",
            "content": """
            <h2>Get In Touch</h2>
            <p>Have questions about crypto taxes, or want to partner with us? We'd love to hear from you.</p>
            <form style="display: flex; flex-direction: column; gap: 15px; max-width: 500px; margin-top: 20px;">
                <input type="text" placeholder="Your Name" required style="padding: 10px;">
                <input type="email" placeholder="Your Email" required style="padding: 10px;">
                <textarea placeholder="Your Message" rows="5" required style="padding: 10px;"></textarea>
                <button type="submit" class="btn btn-primary" onclick="event.preventDefault(); alert('Message sent!');">Send Message</button>
            </form>
            """
        },
        {
            "slug": "privacy-policy",
            "title": "Privacy Policy",
            "meta_description": "Privacy policy for Extended Car Warranty Hub.",
            "content": """
            <p>Last updated: May 20, 2024</p>
            <h2>1. Information We Collect</h2>
            <p>We may collect personal information such as your email address when you subscribe to our newsletter.</p>
            <h2>2. Use of Cookies and Google AdSense</h2>
            <p>We use cookies to enhance your experience. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to our website. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to our sites and/or other sites on the Internet. You may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank">Ads Settings</a>.</p>
            <h2>3. Contact</h2>
            <p>If you have any questions about this Privacy Policy, please <a href="/contact">contact us</a>.</p>
            """
        },
        {
            "slug": "terms-of-service",
            "title": "Terms of Service",
            "meta_description": "Terms of service for using our website.",
            "content": """
            <h2>1. Acceptance of Terms</h2>
            <p>By accessing our website, you agree to be bound by these Terms of Service and all applicable laws and regulations.</p>
            <h2>2. Intellectual Property</h2>
            <p>All content on this site is the property of Extended Car Warranty Hub unless otherwise noted.</p>
            """
        },
        {
            "slug": "disclaimer",
            "title": "Disclaimer",
            "meta_description": "Financial and legal disclaimer for our content.",
            "content": """
            <h2>General Disclaimer</h2>
            <p>The content provided on Extended Car Warranty Hub is for informational and educational purposes only. It is not intended as financial, legal, or professional advice. Always consult with a licensed insurance broker, financial advisor, or legal counsel before making decisions regarding commercial vehicle warranties, service contracts, or insurance policies.</p>
            <p>We make no representations as to the accuracy, completeness, or suitability of any information on this site and will not be liable for any errors, omissions, or delays in this information or any losses, injuries, or damages arising from its display or use.</p>
            """
        }
    ]
    
    page_template = env.get_template('page.html')
    for page in static_pages:
        html = page_template.render(site=site, page=page)
        out_dir = os.path.join(ROOT_DIR, page['slug'])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)

def build():
    print("Loading data...")
    site, articles = load_data()
    
    # 1. Homepage
    print("Building homepage...")
    index_template = env.get_template('index.html')
    index_html = index_template.render(site=site, articles=articles)
    with open(os.path.join(ROOT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    # 2. 404 Page
    print("Building 404 page...")
    not_found_template = env.get_template('404.html')
    with open(os.path.join(ROOT_DIR, '404.html'), 'w', encoding='utf-8') as f:
        f.write(not_found_template.render(site=site))
        
    # 3. Static Pages
    print("Building static pages...")
    create_static_pages(site, articles)
    
    # 4. Category Pages
    print("Building category pages...")
    category_template = env.get_template('category.html')
    for cat in site['categories']:
        cat_articles = [a for a in articles if a['category'] == cat]
        html = category_template.render(site=site, category=cat, articles=cat_articles)
        cat_dir = os.path.join(ROOT_DIR, 'category', slugify(cat))
        os.makedirs(cat_dir, exist_ok=True)
        with open(os.path.join(cat_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
            
    # 5. Articles
    print(f"Building {len(articles)} articles...")
    article_template = env.get_template('article.html')
    for i, article in enumerate(articles):
        # Get related articles (same category, exclude self, max 3)
        related = [a for a in articles if a['category'] == article['category'] and a['slug'] != article['slug']][:3]
        if len(related) < 3:
            # Fill with random articles if not enough in same category
            other = [a for a in articles if a['slug'] != article['slug'] and a not in related]
            related.extend(other[:3-len(related)])
            
        html = article_template.render(site=site, article=article, related_articles=related)
        article_dir = os.path.join(ROOT_DIR, article['slug'])
        os.makedirs(article_dir, exist_ok=True)
        with open(os.path.join(article_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
            
    # 6. Search Index
    print("Building search index...")
    search_index = [
        {"title": a['title'], "url": f"/{a['slug']}", "description": a['meta_description'], "category": a['category']} 
        for a in articles
    ]
    with open(os.path.join(ROOT_DIR, 'search_index.json'), 'w', encoding='utf-8') as f:
        json.dump(search_index, f)

    # 7. Sitemap.xml
    print("Building sitemap.xml...")
    urls = [
        {"loc": site['site_url'] + "/", "priority": "1.0"},
        {"loc": site['site_url'] + "/about-us", "priority": "0.7"},
        {"loc": site['site_url'] + "/contact", "priority": "0.7"}
    ]
    for cat in site['categories']:
        urls.append({"loc": f"{site['site_url']}/category/{slugify(cat)}", "priority": "0.8"})
    for a in articles:
        urls.append({"loc": f"{site['site_url']}/{a['slug']}", "priority": "0.9"})
        
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap += f'  <url>\n    <loc>{u["loc"]}</loc>\n    <priority>{u["priority"]}</priority>\n  </url>\n'
    sitemap += '</urlset>'
    with open(os.path.join(ROOT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)
        
    # 8. RSS Feed
    print("Building rss.xml...")
    rss = f'<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0">\n<channel>\n  <title>{site["site_name"]}</title>\n  <link>{site["site_url"]}</link>\n  <description>{site["description"]}</description>\n'
    for a in articles[:50]: # limit RSS to latest 50
        rss += f'  <item>\n    <title>{a["title"]}</title>\n    <link>{site["site_url"]}/{a["slug"]}</link>\n    <description>{a["meta_description"]}</description>\n  </item>\n'
    rss += '</channel>\n</rss>'
    with open(os.path.join(ROOT_DIR, 'rss.xml'), 'w', encoding='utf-8') as f:
        f.write(rss)
        
    # 9. robots.txt
    print("Building robots.txt...")
    robots = f"User-agent: *\nAllow: /\nSitemap: {site['site_url']}/sitemap.xml\n"
    with open(os.path.join(ROOT_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots)
        
    # 10. Copy Assets and PWA files
    print("Copying assets...")
    dest_assets = os.path.join(ROOT_DIR, 'assets')
    if os.path.exists(dest_assets):
        shutil.rmtree(dest_assets)
    shutil.copytree(os.path.join(SRC_DIR, 'assets'), dest_assets)
    
    # Create image directories
    os.makedirs(os.path.join(dest_assets, 'images'), exist_ok=True)
    
    # Generate placeholder images using SVG
    def create_placeholder(path, text, width, height):
        svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="{width}" height="{height}" fill="#0F172A"/>
            <text x="{width/2}" y="{height/2}" font-family="Arial" font-size="24" fill="#ffffff" text-anchor="middle" dominant-baseline="middle">{text}</text>
        </svg>'''
        with open(path, 'w') as f:
            f.write(svg)

    create_placeholder(os.path.join(dest_assets, 'images', 'og-default.jpg'), 'OG Image', 1200, 630)
    create_placeholder(os.path.join(dest_assets, 'images', 'author.svg'), 'Author', 80, 80)
    create_placeholder(os.path.join(dest_assets, 'images', 'icon-192.png'), 'Icon 192', 192, 192)
    create_placeholder(os.path.join(dest_assets, 'images', 'icon-512.png'), 'Icon 512', 512, 512)
    
    shutil.copy2(os.path.join(SRC_DIR, 'manifest.json'), os.path.join(ROOT_DIR, 'manifest.json'))
    shutil.copy2(os.path.join(SRC_DIR, 'sw.js'), os.path.join(ROOT_DIR, 'sw.js'))
    
    print("Site generated successfully!")

if __name__ == "__main__":
    build()
