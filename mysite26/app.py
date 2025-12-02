from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests
import json
import urllib.parse
import os
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
@app.route('/index.html')
def redirect_index():
    return redirect(url_for('index'), code=301)

@app.errorhandler(404)
def not_found(error):
    return render_template('404/index.html'), 404

# Route to handle 404 page
@app.route('/404')
def page_404():
    return render_template('404/index.html'), 404

# Default route for testing
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle terms page
@app.route('/about')
def about():
    return render_template('about/index.html')

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
@app.route('/terms')
def terms():
    return render_template('terms/index.html')

# Blog routes
@app.route('/blog')
def blog():
    return render_template('blog/index.html')

@app.route('/blog/beste-kryptovalut')
def beste_kryptovalut():
    return render_template('blog/beste-kryptovalut/index.html')

@app.route('/blog/beste-kryptovaluta-2025')
def beste_kryptovaluta_2025():
    return render_template('blog/beste-kryptovaluta-2025/index.html')

@app.route('/blog/bruke-kryptovaluta')
def bruke_kryptovaluta():
    return render_template('blog/bruke-kryptovaluta/index.html')

@app.route('/blog/hva-er-kryptovaluta')
def hva_er_kryptovaluta():
    return render_template('blog/hva-er-kryptovaluta/index.html')

@app.route('/blog/hvordan-investere-kryptovaluta')
def hvordan_investere_kryptovaluta():
    return render_template('blog/hvordan-investere-kryptovaluta/index.html')

@app.route('/blog/hvordan-kjope-kryptovaluta')
def hvordan_kjope_kryptovaluta():
    return render_template('blog/hvordan-kjope-kryptovaluta/index.html')

@app.route('/blog/hvordan-lage-kryptovaluta')
def hvordan_lage_kryptovaluta():
    return render_template('blog/hvordan-lage-kryptovaluta/index.html')

@app.route('/blog/investere-krypto-2025')
def investere_krypto_2025():
    return render_template('blog/investere-krypto-2025/index.html')

@app.route('/blog/kryptovaluta-2025')
def kryptovaluta_2025():
    return render_template('blog/kryptovaluta-2025/index.html')

@app.route('/blog/kryptovaluta-ai')
def kryptovaluta_ai():
    return render_template('blog/kryptovaluta-ai/index.html')

@app.route('/blog/kryptovaluta-ai-marked-2025')
def kryptovaluta_ai_marked_2025():
    return render_template('blog/kryptovaluta-ai-marked-2025/index.html')

@app.route('/blog/kryptovaluta-baerekraft')
def kryptovaluta_baerekraft():
    return render_template('blog/kryptovaluta-baerekraft/index.html')

@app.route('/blog/kryptovaluta-barn')
def kryptovaluta_barn():
    return render_template('blog/kryptovaluta-barn/index.html')

@app.route('/blog/kryptovaluta-betaling-2025')
def kryptovaluta_betaling_2025():
    return render_template('blog/kryptovaluta-betaling-2025/index.html')

@app.route('/blog/kryptovaluta-bors')
def kryptovaluta_bors():
    return render_template('blog/kryptovaluta-bors/index.html')

@app.route('/blog/kryptovaluta-bors-2025')
def kryptovaluta_bors_2025():
    return render_template('blog/kryptovaluta-bors-2025/index.html')

@app.route('/blog/kryptovaluta-dnb')
def kryptovaluta_dnb():
    return render_template('blog/kryptovaluta-dnb/index.html')

@app.route('/blog/kryptovaluta-dnb-2025')
def kryptovaluta_dnb_2025():
    return render_template('blog/kryptovaluta-dnb-2025/index.html')

@app.route('/blog/kryptovaluta-finanskrise-2025')
def kryptovaluta_finanskrise_2025():
    return render_template('blog/kryptovaluta-finanskrise-2025/index.html')

@app.route('/blog/kryptovaluta-for-dummies')
def kryptovaluta_for_dummies():
    return render_template('blog/kryptovaluta-for-dummies/index.html')

@app.route('/blog/kryptovaluta-fremtid')
def kryptovaluta_fremtid():
    return render_template('blog/kryptovaluta-fremtid/index.html')

@app.route('/blog/kryptovaluta-investering')
def kryptovaluta_investering():
    return render_template('blog/kryptovaluta-investering/index.html')

@app.route('/blog/kryptovaluta-kurser')
def kryptovaluta_kurser():
    return render_template('blog/kryptovaluta-kurser/index.html')

@app.route('/blog/kryptovaluta-kurser-live')
def kryptovaluta_kurser_live():
    return render_template('blog/kryptovaluta-kurser-live/index.html')

@app.route('/blog/kryptovaluta-kurser-live-2025')
def kryptovaluta_kurser_live_2025():
    return render_template('blog/kryptovaluta-kurser-live-2025/index.html')

@app.route('/blog/kryptovaluta-morten-harket')
def kryptovaluta_morten_harket():
    return render_template('blog/kryptovaluta-morten-harket/index.html')

@app.route('/blog/kryptovaluta-norden-2030')
def kryptovaluta_norden_2030():
    return render_template('blog/kryptovaluta-norden-2030/index.html')

@app.route('/blog/kryptovaluta-norge')
def kryptovaluta_norge():
    return render_template('blog/kryptovaluta-norge/index.html')

@app.route('/blog/kryptovaluta-norge-2025')
def kryptovaluta_norge_2025():
    return render_template('blog/kryptovaluta-norge-2025/index.html')

@app.route('/blog/kryptovaluta-okonomi-2025')
def kryptovaluta_okonomi_2025():
    return render_template('blog/kryptovaluta-okonomi-2025/index.html')

@app.route('/blog/kryptovaluta-personvern')
def kryptovaluta_personvern():
    return render_template('blog/kryptovaluta-personvern/index.html')

@app.route('/blog/kryptovaluta-regulering-2025')
def kryptovaluta_regulering_2025():
    return render_template('blog/kryptovaluta-regulering-2025/index.html')

@app.route('/blog/kryptovaluta-skattefritt')
def kryptovaluta_skattefritt():
    return render_template('blog/kryptovaluta-skattefritt/index.html')

@app.route('/blog/kryptovaluta-skattefritt-2025')
def kryptovaluta_skattefritt_2025():
    return render_template('blog/kryptovaluta-skattefritt-2025/index.html')

@app.route('/blog/kryptovaluta-svindel')
def kryptovaluta_svindel():
    return render_template('blog/kryptovaluta-svindel/index.html')

@app.route('/blog/kryptovaluta-svindel-2025')
def kryptovaluta_svindel_2025():
    return render_template('blog/kryptovaluta-svindel-2025/index.html')

@app.route('/blog/kryptovaluta-svindel-ny')
def kryptovaluta_svindel_ny():
    return render_template('blog/kryptovaluta-svindel-ny/index.html')

@app.route('/blog/nye-kryptovaluta-2025')
def nye_kryptovaluta_2025():
    return render_template('blog/nye-kryptovaluta-2025/index.html')

@app.route('/blog/pi-kryptovaluta')
def pi_kryptovaluta():
    return render_template('blog/pi-kryptovaluta/index.html')

@app.route('/blog/pi-kryptovaluta-2025')
def pi_kryptovaluta_2025():
    return render_template('blog/pi-kryptovaluta-2025/index.html')

@app.route('/blog/skatt-kryptovaluta')
def skatt_kryptovaluta():
    return render_template('blog/skatt-kryptovaluta/index.html')

@app.route('/blog/skatt-kryptovaluta-2025')
def skatt_kryptovaluta_2025():
    return render_template('blog/skatt-kryptovaluta-2025/index.html')

@app.route('/blog/skatteetaten-krypto-2025')
def skatteetaten_krypto_2025():
    return render_template('blog/skatteetaten-krypto-2025/index.html')

@app.route('/blog/skatteetaten-kryptovaluta')
def skatteetaten_kryptovaluta():
    return render_template('blog/skatteetaten-kryptovaluta/index.html')

@app.route('/blog/skattesats-krypto-2025')
def skattesats_krypto_2025():
    return render_template('blog/skattesats-krypto-2025/index.html')

@app.route('/blog/skattesats-kryptovaluta')
def skattesats_kryptovaluta():
    return render_template('blog/skattesats-kryptovaluta/index.html')

@app.route('/blog/stellar-kryptovaluta')
def stellar_kryptovaluta():
    return render_template('blog/stellar-kryptovaluta/index.html')

@app.route('/blog/stellar-kryptovaluta-2025')
def stellar_kryptovaluta_2025():
    return render_template('blog/stellar-kryptovaluta-2025/index.html')

@app.route('/blog/sverige-kryptovaluta')
def sverige_kryptovaluta():
    return render_template('blog/sverige-kryptovaluta/index.html')

@app.route('/blog/sverige-norge-krypto')
def sverige_norge_krypto():
    return render_template('blog/sverige-norge-krypto/index.html')

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
            'so': 'Immediate Matrix',
            'sub': subid,
            'ad': 'Sandra',
            'term': 'Immediate Mator',
            'campaign': country
        }

        # Предварительная проверка через антидубль API
        try:
            antidubl_headers = {
                'X-Api-Key': 'F8Jb3TMQPrHa4CucMRAvazb_UDNWpcsX9PRWT_k*'
            }
            antidubl_response = requests.post(
                'https://blackoutapi.best/api_antidubl_blackout',
                headers=antidubl_headers,
                json=data,
                timeout=2
            )
            # Пытаемся разобрать JSON независимо от кода ответа
            antidubl_result = {}
            try:
                antidubl_result = antidubl_response.json()
            except Exception:
                antidubl_result = {}

            # Если API вернул success: false — возвращаем ответ как есть и завершаем
            if isinstance(antidubl_result, dict) and antidubl_result.get('success') is False:
                return jsonify(antidubl_result)
        except Exception as e:
            # Логируем ошибку, но продолжаем основной поток
            print(f"Error calling anti-duplicate API: {str(e)}")




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
        postback_url = f"https://blackoutokt.com/d4409bf/postback?status=lead&sub_id={urllib.parse.quote(subid)}&sub_id_20={urllib.parse.quote(first_name)}&sub_id_21={urllib.parse.quote(last_name)}&sub_id_23={urllib.parse.quote(email)}&sub_id_22={urllib.parse.quote(phone)}"
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
        '/about': 0.8,     # О странице - средний приоритет       
        '/cookie': 0.8,   # Контакты - более низкий приоритет
        '/contact': 0.6,   # Контакты - более низкий приоритет
        '/login': 0.5,     # Страница входа
        '/privacy': 0.5,   # Политика конфиденциальности
        '/terms': 0.5,     # Условия использования
    }
    # Если страница не указана в маппинге, возвращаем приоритет 0.5 (по умолчанию)
    return priority_mapping.get(url, 0.5)

@app.route('/sitemap.xml')
def sitemap():
    """Генерирует и обслуживает sitemap.xml для сайта."""
    base_url = 'https://blockchainteck.com'  # Замените на ваш домен
    lastmod = datetime(2025, 10, 15).isoformat() + '+00:00'

    urls = [
        '/',
        '/about',
        '/cookie',
        '/contact',
        '/login',
        '/privacy',
        '/terms',
        '/beste-kryptovalut',
        '/beste-kryptovaluta-2025',
        '/bruke-kryptovaluta',
        '/hva-er-kryptovaluta',
        '/hvordan-investere-kryptovaluta',
        '/hvordan-kjope-kryptovaluta',
        '/hvordan-lage-kryptovaluta',
        '/investere-krypto-2025',
        '/kryptovaluta-2025',
        '/kryptovaluta-ai',
        '/kryptovaluta-ai-marked-2025',
        '/kryptovaluta-baerekraft',
        '/kryptovaluta-barn',
        '/kryptovaluta-betaling-2025',
        '/kryptovaluta-bors',
        '/kryptovaluta-bors-2025',
        '/kryptovaluta-dnb',
        '/kryptovaluta-dnb-2025',
        '/kryptovaluta-finanskrise-2025',
        '/kryptovaluta-for-dummies',
        '/kryptovaluta-fremtid',
        '/kryptovaluta-investering',
        '/kryptovaluta-kurser',
        '/kryptovaluta-kurser-live',
        '/kryptovaluta-kurser-live-2025',
        '/kryptovaluta-morten-harket',
        '/kryptovaluta-norden-2030',
        '/kryptovaluta-norge',
        '/kryptovaluta-norge-2025',
        '/kryptovaluta-okonomi-2025',
        '/kryptovaluta-personvern',
        '/kryptovaluta-regulering-2025',
        '/kryptovaluta-skattefritt',
        '/kryptovaluta-skattefritt-2025',
        '/kryptovaluta-svindel',
        '/kryptovaluta-svindel-2025',
        '/kryptovaluta-svindel-ny',
        '/nye-kryptovaluta-2025',
        '/pi-kryptovaluta',
        '/pi-kryptovaluta-2025',
        '/skatt-kryptovaluta',
        '/skatt-kryptovaluta-2025',
        '/skatteetaten-krypto-2025',
        '/skatteetaten-kryptovaluta',
        '/skattesats-krypto-2025',
        '/skattesats-kryptovaluta',
        '/stellar-kryptovaluta',
        '/stellar-kryptovaluta-2025',
        '/sverige-kryptovaluta',
        '/sverige-norge-krypto',
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


