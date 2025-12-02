from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests
import json
import urllib.parse
from datetime import datetime


app = Flask(__name__, static_folder='static')



@app.before_request
def redirect_to_https():
    # Redirect HTTP to HTTPS
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return redirect(request.url.replace('http://', 'https://'), code=301)

    # Redirect www to non-www
    if request.host.startswith('www.'):
        new_host = request.host[4:]  # Remove 'www.'
        new_url = request.url.replace(f'//www.{new_host}', f'//{new_host}')
        return redirect(new_url, code=301)
    
    
    
    
    
    

@app.errorhandler(404)
def not_found(error):
    return render_template('404/index.html'), 404


# Default route for testing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about/index.html')

@app.route('/beste-crypto-exchanges-voor-belgen')
def a():
    return render_template('beste-crypto-exchanges-voor-belgen/index.html')

@app.route('/beste-wallets-voor-belgen')
def b():
    return render_template('beste-wallets-voor-belgen/index.html')

@app.route('/hoe-begin-je-met-beleggen-in-belgie')
def d():
    return render_template('hoe-begin-je-met-beleggen-in-belgie/index.html')

@app.route('/hoe-wordt-crypto-belast-in-belgie')
def e():
    return render_template('hoe-wordt-crypto-belast-in-belgie/index.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy/index.html')

@app.route('/strategieen-voor-passief-beleggen')
def f():
    return render_template('strategieen-voor-passief-beleggen/index.html')

@app.route('/terms')
def g():
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

            'ai': '2958048',
            'ci': '1',
            'gi': '31',


            'userip': get_client_ip(),  # IP пользователя из Flask
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'password': 'ABCabc123',
            'phone': phone,
            'so': 'Dinera Paynex',
            'sub': subid,
            'ad': 'Sandra',
            'term': 'Dinera Paynex',
            'lg': 'ES',
            'campaign': country
        }

        headers = {
            'Content-Type': 'application/json',
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
        postback_url = f"https://blackoutkt.com/d4409bf/postback?status=lead&sub_id={urllib.parse.quote(subid)}&sub_id_20={urllib.parse.quote(first_name)}&sub_id_21={urllib.parse.quote(last_name)}&sub_id_23={urllib.parse.quote(email)}&sub_id_22={urllib.parse.quote(phone)}"
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
        '/': 1.0,          # Главная страница имеет самый высокий приоритет
        '/about': 0.9,     # О странице - средний приоритет       
        '/privacy': 0.9,   # Политика конфиденциальности
        '/terms': 0.9,     # Условия использования
        '/beste-crypto-exchanges-voor-belgen': 0.9,
        '/beste-wallets-voor-belgen': 0.9,
        '/hoe-begin-je-met-beleggen-in-belgie': 0.9,
        '/hoe-wordt-crypto-belast-in-belgie': 0.9,
        '/strategieen-voor-passief-beleggen': 0.9,
    }
    # Если страница не указана в маппинге, возвращаем приоритет 0.5 (по умолчанию)
    return priority_mapping.get(url, 0.5)

@app.route('/sitemap.xml')
def sitemap():
    """Генерирует и обслуживает sitemap.xml для сайта."""
    base_url = 'https://cryptobelbe.com'  # Замените на ваш домен
    lastmod = datetime(2025, 9, 30).isoformat() + '+00:00'

    urls = [
        '/',
        '/about',
        '/privacy',
        '/terms',
        '/beste-crypto-exchanges-voor-belgen',
        '/beste-wallets-voor-belgen',
        '/hoe-begin-je-met-beleggen-in-belgie',
        '/hoe-wordt-crypto-belast-in-belgie',
        '/strategieen-voor-passief-beleggen',
    ]

    # Генерация XML-карты сайта
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        full_url = f"{base_url}{url}"
        priority = get_priority(url)  # Получаем приоритет для текущей страницы
        sitemap_xml += f'    <url>\n'
        sitemap_xml += f'        <loc>{full_url}</loc>\n'
        sitemap_xml += f'        <lastmod>{lastmod}</lastmod>\n'
        sitemap_xml += f'        <changefreq>monthly</changefreq>\n'
        sitemap_xml += f'        <priority>{priority}</priority>\n'
        sitemap_xml += f'    </url>\n'

    sitemap_xml += '</urlset>'

    # Возвращаем XML-ответ с правильным MIME-типом
    return Response(sitemap_xml, mimetype='application/xml')


# Старт приложения
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


