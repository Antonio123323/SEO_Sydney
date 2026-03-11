from flask import Flask, abort, render_template, request, redirect, url_for, jsonify, Response
import os
import requests
import json
import urllib.parse
from pathlib import Path
from datetime import datetime
from jinja2 import TemplateNotFound

# Явные пути для корректной работы независимо от рабочей директории
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = Path(BASE_DIR) / 'templates'
app = Flask(__name__,
    static_folder=os.path.join(BASE_DIR, 'static'),
    template_folder=os.path.join(BASE_DIR, 'templates'))



@app.before_request
def redirect_to_https():
    # HTTP→HTTPS и www→non-www обрабатывает Nginx. Flask не редиректит при запросе через прокси,
    # чтобы избежать ERR_TOO_MANY_REDIRECTS (Cloudflare Flexible SSL и др.)
    if request.headers.get('X-Forwarded-For'):
        return  # За прокси — редиректы делает Nginx
    # Redirect HTTP to HTTPS (только при прямом подключении)
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return redirect(request.url.replace('http://', 'https://'), code=301)
    # Redirect www to non-www
    if request.host.startswith('www.'):
        new_host = request.host[4:]
        new_url = request.url.replace(f'//www.{new_host}', f'//{new_host}')
        return redirect(new_url, code=301)
    
    

@app.route('/index.php')
@app.route('/index.html')
def redirect_index():
    return redirect(url_for('index'), code=301)

@app.errorhandler(404)
def not_found(error):
    return render_template('404/404.html'), 404

# Route to handle 404 page
@app.route('/404')
def page_404():
    return render_template('404/404.html'), 404

# Default route for testing
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle blog index page
@app.route('/blog')
@app.route('/blog/')
def blog_index():
    return render_template('blog/index.html')

# Route to handle blog post pages
@app.route('/blog/<slug>')
@app.route('/blog/<slug>/')
def blog_post(slug):
    try:
        return render_template(f'blog/{slug}/index.html')
    except TemplateNotFound:
        abort(404)

# Route to handle contact page
@app.route('/contact')
def contact():
    return render_template('contact/index.html')

# Route to handle cookie page
@app.route('/cookie')
def cookie():
    return render_template('cookie/index.html')

# Route to handle login page
@app.route('/login')
def login():
    return render_template('login/index.html')

# Route to handle privacy page
@app.route('/privacy')
def privacy():
    return render_template('privacy/index.html')

# Route to handle terms page
@app.route('/about')
def about():
    return render_template('about/index.html')

# Route to handle terms page
@app.route('/terms')
def terms():
    return render_template('terms/index.html')


def get_client_ip():
    """ Получает реальный IP пользователя, учитывая прокси. """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]  # Берём первый IP из списка
    return request.remote_addr  # Если заголовок отсутствует, используем стандартный способ

# Route to handle form submission (replacing send.php)
@app.route('/send', methods=['POST'])
def send_data():
    try:
        # Получаем данные из формы
        country_code = request.form.get('country_code', '')
        country = request.form.get('country', '')
        phone = request.form.get('phone', '')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        email = request.form.get('email', '')
        subid = request.form.get('subid', '')

        # Форматируем телефонный номер (аналогично PHP: добавляем country_code, если его нет)
        if country_code and not phone.startswith(country_code):
            phone = country_code + phone

        # Подготавливаем данные для отправки на агрегацию
        data = {
            # Keitaro
            # 'ai': '2958032',
            # 'ci': '1',
            # 'gi': '17',


            'ai': '2958048',
            'ci': '1',
            'gi': '31',


            'userip': get_client_ip(),  # IP пользователя из Flask
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'password': 'ABCabc123',
            'phone': phone,
            'so': 'Immediate Matrix',
            'sub': subid,
            'ad': 'Sandra',
            'term': 'Immediate Matrix',
            'lg': 'EN',
            'campaign': country
        }
        # Отправляем запрос на https://ag.arbgroup.shop/api/signup/procform
        headers = {
            'Content-Type': 'application/json',
            # Keitaro
            # 'x-trackbox-username': 'Keitaro',
            # 'x-trackbox-password': 'TB4v{\FD^TX~]A-:GK',

            'x-trackbox-username': 'Sandra',
            'x-trackbox-password': 'wdH9Jiid4F!ru_9Ck*eU',
            'x-api-key': '2643889w34df345676ssdas323tgc738'
        }

        response = requests.post(
            'https://ag.arbboteam.com/api/signup/procform',
            headers=headers,
            data=json.dumps(data)
        )

        # Проверяем ответ от API
        if response.status_code == 200:
            result = response.text
            print(f"Успешно отправлено на агрегацию: {result}")
        else:
            result = f"Ошибка при отправке на агрегацию: {response.status_code} - {response.text}"
            return jsonify({'status': 'error', 'message': result}), 500

        # Выполняем постбэк-запрос
        postback_url = f"https://blackoutorg.com/d4409bf/postback?status=lead&sub_id={urllib.parse.quote(subid)}&sub_id_20={urllib.parse.quote(first_name)}&sub_id_21={urllib.parse.quote(last_name)}&sub_id_23={urllib.parse.quote(email)}&sub_id_22={urllib.parse.quote(phone)}"
        postback_response = requests.get(postback_url)
        if postback_response.status_code != 200:
            print(f"Ошибка постбэка: {postback_response.status_code} - {postback_response.text}")

        # Возвращаем результат клиенту (аналогично PHP: echo $result)
        return jsonify({'status': 'success', 'message': result})

    except Exception as e:
        error_message = f"Ошибка обработки запроса: {str(e)}"
        print(error_message)
        return jsonify({'status': 'error', 'message': error_message}), 500


# Функция для вычисления приоритета
def get_priority(url):
    """Динамически рассчитывает приоритет для каждой страницы."""
    priority_mapping = {
        '/': 1.0,
        '/about': 0.8,
        '/cookie': 0.8,
        '/contact': 0.6,
        '/login': 0.5,
        '/privacy': 0.5,
        '/terms': 0.5,
        '/blog': 0.8,
    }
    return priority_mapping.get(url, 0.5)


@app.route('/sitemap.xml')
def sitemap():
    """Генерирует sitemap.xml автоматически из зарегистрированных маршрутов и blog-шаблонов."""
    base_url = request.url_root.rstrip('/')
    if request.headers.get('X-Forwarded-Proto') == 'https':
        base_url = base_url.replace('http://', 'https://')
    lastmod = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    exclude_rules = {'/static', '/sitemap.xml', '/index.php', '/index.html', '/send'}
    urls = []
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith('/static') or rule.rule in exclude_rules:
            continue
        if rule.endpoint == 'static' or rule.methods and 'GET' not in rule.methods:
            continue
        if any(p in rule.rule for p in ['<', '>']):
            continue
        path = rule.rule if rule.rule != '/' else ''
        loc = f"{base_url}{path}"
        priority = get_priority(rule.rule)
        urls.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>{priority:.2f}</priority>\n  </url>')
    # Добавляем blog-посты из шаблонов (динамический маршрут /blog/<slug>)
    blog_dir = TEMPLATES_DIR / 'blog'
    if blog_dir.is_dir():
        for slug_dir in blog_dir.iterdir():
            if slug_dir.is_dir() and (slug_dir / 'index.html').is_file():
                slug = slug_dir.name
                if slug != 'index':
                    loc = f"{base_url}/blog/{slug}"
                    urls.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>0.64</priority>\n  </url>')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>'
    return Response(xml, mimetype='application/xml', headers={'Content-Type': 'application/xml; charset=utf-8'})


# Старт приложения
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

