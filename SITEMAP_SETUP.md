# sitemap.xml ni yaratish uchun Flask route

# app/routes/main.py'ga qo'shing:

from flask import Blueprint, render_template, current_app, jsonify
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap for search engines"""
    base_url = 'https://nogiron.pythonanywhere.com'
    
    urls = [
        {
            'loc': f'{base_url}/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '1.0'
        },
        {
            'loc': f'{base_url}/register',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8'
        },
        {
            'loc': f'{base_url}/login',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8'
        },
        {
            'loc': f'{base_url}/doctors',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.9'
        },
    ]
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return xml, 200, {'Content-Type': 'application/xml'}

# app/__init__.py'da register qilish:

def create_app():
    app = Flask(__name__)
    # ... other config ...
    
    from app.routes.main import bp
    app.register_blueprint(bp)
    
    return app
