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
    
    

@app.route('/index.php')
def redirect_index():
    return redirect(url_for('index'), code=301)

@app.errorhandler(404)
def not_found(error):
    return render_template('404/404.html'), 404


# Default route for testing
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle about page
@app.route('/about')
def about():
    return render_template('about/index.html')

# Route to handle privacy page
@app.route('/privacy')
def privacy():
    return render_template('privacy/index.html')

# Route to handle terms page
@app.route('/terms')
def terms():
    return render_template('terms/index.html')

# Route to handle modern-income-sources-crypto-nfts-ai page
@app.route('/modern-income-sources-crypto-nfts-ai')
def modern_income_sources_crypto_nfts_ai():
    return render_template('modern-income-sources-crypto-nfts-ai/index.html')

# Route to handle passive-income-investing-etfs-stocks-bonds page
@app.route('/passive-income-investing-etfs-stocks-bonds')
def passive_income_investing_etfs_stocks_bonds():
    return render_template('passive-income-investing-etfs-stocks-bonds/index.html')

# Route to handle passive-income-with-ai-artificial-intelligence page
@app.route('/passive-income-with-ai-artificial-intelligence')
def passive_income_with_ai_artificial_intelligence():
    return render_template('passive-income-with-ai-artificial-intelligence/index.html')

# Route to handle types-of-passive-income-for-beginners page
@app.route('/types-of-passive-income-for-beginners')
def types_of_passive_income_for_beginners():
    return render_template('types-of-passive-income-for-beginners/index.html')

# Route to handle wat-is-passief-inkomen page
@app.route('/wat-is-passief-inkomen')
def wat_is_passief_inkomen():
    return render_template('wat-is-passief-inkomen/index.html')


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
            'so': 'Allpaskapitaal',
            'sub': subid,
            'ad': 'Sandra',
            'term': 'Allpaskapitaal',
            'lg': 'nl',
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



# Route to generate and serve sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    """Generate and serve a sitemap.xml for the website."""
    # Base URL (ensure this matches your domain, e.g., https://yourdomain.com)
    base_url = 'http://allpaskapitaal.com'  # Replace with your actual domain
    # Current date for lastmod (February 27, 2025)
    lastmod = datetime(2025, 2, 27).isoformat() + '+00:00'

    # List of URLs to include in the sitemap
    urls = [
        '/',
        '/about',
        '/privacy',
        '/terms',
        '/modern-income-sources-crypto-nfts-ai',
        '/passive-income-investing-etfs-stocks-bonds',
        '/passive-income-with-ai-artificial-intelligence',
        '/types-of-passive-income-for-beginners',
        '/wat-is-passief-inkomen',
    ]

    # Generate XML sitemap
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        full_url = f"{base_url}{url}"
        # Priority: 1.0 for homepage, 0.9 for others
        priority = '1.0' if url == '/' else '0.9'
        sitemap_xml += f'    <url>\n'
        sitemap_xml += f'        <loc>{full_url}</loc>\n'
        sitemap_xml += f'        <lastmod>{lastmod}</lastmod>\n'
        sitemap_xml += f'        <changefreq>monthly</changefreq>\n'
        sitemap_xml += f'        <priority>{priority}</priority>\n'
        sitemap_xml += f'    </url>\n'

    sitemap_xml += '</urlset>'

    # Return the XML response with the correct content type
    return Response(sitemap_xml, mimetype='application/xml')


# Старт приложения
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


