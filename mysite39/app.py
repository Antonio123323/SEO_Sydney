from flask import Flask, abort, render_template, request, redirect, url_for, jsonify, Response
import os
import requests
import json
import urllib.parse
from pathlib import Path
from datetime import datetime

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

@app.route('/blog')
@app.route('/blog/')
def blog():
    return render_template('blog/index.html')

@app.route('/blog/<path:slug>')
@app.route('/blog/<path:slug>/')
def blog_post(slug):
    clean_slug = slug.strip('/')
    template_path = TEMPLATES_DIR / 'blog' / clean_slug / 'index.html'
    if not template_path.is_file():
        abort(404)
    return render_template(f'blog/{clean_slug}/index.html')

@app.route('/news')
@app.route('/news/')
def news():
    return render_template('news/index.html')

@app.route('/news/<path:slug>')
@app.route('/news/<path:slug>/')
def news_post(slug):
    clean_slug = slug.strip('/')
    template_path = TEMPLATES_DIR / 'news' / clean_slug / 'index.html'
    if not template_path.is_file():
        abort(404)
    return render_template(f'news/{clean_slug}/index.html')

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
            # 'ai': '2958048',
            # 'ci': '1',
            # 'gi': '63',


            'ai': '2958048',
            'ci': '1',
            'gi': '63',


            'userip': get_client_ip(),  # IP пользователя из Flask
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'password': 'ABCabc123',
            'phone': phone,
            'so': 'CryptoStratégie',
            'sub': subid,
            'ad': 'Ameli',
            'term': 'CryptoStratégie',
            'lg': 'fr',
            'campaign': country
        }
        # Отправляем запрос на https://ag.arbgroup.shop/api/signup/procform
        headers = {
            'Content-Type': 'application/json',
            # Keitaro
            # 'x-trackbox-username': 'Keitaro',
            # 'x-trackbox-password': 'TB4v{\FD^TX~]A-:GK',

            'x-trackbox-username': 'Ameli',
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
        postback_url = f"https://kbose.com/009e2bc/postback?status=lead&sub_id={urllib.parse.quote(subid)}&sub_id_20={urllib.parse.quote(first_name)}&sub_id_21={urllib.parse.quote(last_name)}&sub_id_23={urllib.parse.quote(email)}&sub_id_22={urllib.parse.quote(phone)}"
        postback_response = requests.get(postback_url)
        if postback_response.status_code != 200:
            print(f"Ошибка постбэка: {postback_response.status_code} - {postback_response.text}")

        # Возвращаем результат клиенту (аналогично PHP: echo $result)
        return jsonify({'status': 'success', 'message': result})

    except Exception as e:
        error_message = f"Ошибка обработки запроса: {str(e)}"
        print(error_message)
        return jsonify({'status': 'error', 'message': error_message}), 500


def get_priority(path):
    """Приоритет: главная — 1.0, статьи/новости — 0.7, остальные — 0.8."""
    normalized = path.rstrip('/') or '/'
    if normalized == '/':
        return 1.0
    if normalized.startswith('/blog/') or normalized.startswith('/news/'):
        return 0.7
    return 0.8


def _collect_section_urls(base_url, section, lastmod):
    """Собирает URL статей из templates/{section}/{slug}/index.html."""
    urls = []
    section_dir = TEMPLATES_DIR / section
    if not section_dir.is_dir():
        return urls
    for slug_dir in sorted(section_dir.iterdir()):
        if not slug_dir.is_dir() or not (slug_dir / 'index.html').is_file():
            continue
        slug = slug_dir.name
        if slug == 'index':
            continue
        path = f'/{section}/{slug}'
        loc = f'{base_url}{path}'
        priority = get_priority(path)
        urls.append(
            f'  <url>\n'
            f'    <loc>{loc}</loc>\n'
            f'    <lastmod>{lastmod}</lastmod>\n'
            f'    <priority>{priority:.1f}</priority>\n'
            f'  </url>'
        )
    return urls


@app.route('/sitemap.xml')
def sitemap():
    """Генерирует sitemap.xml из маршрутов Flask и шаблонов blog/news."""
    base_url = request.url_root.rstrip('/')
    if request.headers.get('X-Forwarded-Proto') == 'https':
        base_url = base_url.replace('http://', 'https://')
    lastmod = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    exclude_rules = {
        '/static', '/sitemap.xml', '/index.php', '/index.html', '/send', '/404', '/login',
    }
    seen_paths = set()
    urls = []

    def add_url(path):
        normalized = path.rstrip('/') or '/'
        if normalized in seen_paths or normalized in exclude_rules:
            return
        seen_paths.add(normalized)
        loc = f'{base_url}{normalized}' if normalized != '/' else f'{base_url}/'
        priority = get_priority(normalized)
        urls.append(
            f'  <url>\n'
            f'    <loc>{loc}</loc>\n'
            f'    <lastmod>{lastmod}</lastmod>\n'
            f'    <priority>{priority:.1f}</priority>\n'
            f'  </url>'
        )

    for rule in app.url_map.iter_rules():
        if rule.rule.startswith('/static') or rule.rule in exclude_rules:
            continue
        if rule.endpoint == 'static' or rule.methods and 'GET' not in rule.methods:
            continue
        if any(p in rule.rule for p in ['<', '>']):
            continue
        add_url(rule.rule)

    urls.extend(_collect_section_urls(base_url, 'blog', lastmod))
    urls.extend(_collect_section_urls(base_url, 'news', lastmod))

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(urls)
        + '\n</urlset>'
    )
    return Response(xml, mimetype='application/xml', headers={'Content-Type': 'application/xml; charset=utf-8'})


# Старт приложения
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


