from flask import Flask, render_template, request, redirect, Response
from datetime import datetime, timezone
import os

app = Flask(__name__, static_folder='static')


@app.before_request
def redirect_to_https():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return redirect(request.url.replace('http://', 'https://'), code=301)
    if request.host.startswith('www.'):
        new_host = request.host[4:]
        new_url = request.url.replace(f'//www.{new_host}', f'//{new_host}')
        return redirect(new_url, code=301)


@app.errorhandler(404)
def not_found(error):
    return render_template('404/index.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about/index.html')


@app.route('/blog')
@app.route('/blog/')
def blog():
    return render_template('blog/index.html')


@app.route('/blog/<slug>')
@app.route('/blog/<slug>/')
def blog_article(slug):
    template_path = f'blog/{slug}/index.html'
    full = os.path.join(app.root_path, 'templates', template_path)
    if not os.path.isfile(full):
        return render_template('404/index.html'), 404
    return render_template(template_path)


@app.route('/privacy-policy')
@app.route('/privacy-policy/')
def privacy_policy():
    return render_template('privacy-policy/index.html')


@app.route('/disclaimer')
@app.route('/disclaimer/')
def disclaimer():
    return render_template('disclaimer/index.html')


@app.route('/terms-of-service')
@app.route('/terms-of-service/')
def terms_of_service():
    return render_template('terms-of-service/index.html')


@app.route('/index.php')
def redirect_index():
    return redirect('/', code=301)


@app.route('/sitemap.xml')
def sitemap():
    base_url = request.url_root.rstrip('/')
    if request.headers.get('X-Forwarded-Proto') == 'https':
        base_url = base_url.replace('http://', 'https://')
    lastmod = datetime.now(timezone.utc).date().isoformat()
    urls = [
        '/',
        '/about/',
        '/blog/',
        '/privacy-policy/',
        '/disclaimer/',
        '/terms-of-service/',
    ]
    blog_dir = os.path.join(app.root_path, 'templates', 'blog')
    if os.path.isdir(blog_dir):
        for name in sorted(os.listdir(blog_dir)):
            article = os.path.join(blog_dir, name, 'index.html')
            if os.path.isfile(article):
                urls.append(f'/blog/{name}/')

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        lines.append('  <url>')
        lines.append(f"    <loc>{(base_url + url).rstrip('/')}</loc>")
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append('    <changefreq>monthly</changefreq>')
        lines.append('    <priority>0.8</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')
    return Response('\n'.join(lines), mimetype='application/xml')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
