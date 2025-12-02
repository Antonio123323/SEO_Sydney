from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests
import json
import urllib.parse
from datetime import datetime


app = Flask(__name__, static_folder='static', template_folder='templates')



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

# Route to handle sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    xml_content = render_template('sitemap.xml')
    return Response(xml_content, mimetype='application/xml')

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
@app.route('/blog')
def blog():
    return render_template('blog/index.html')

# Routes for blog subdirectories
@app.route('/blog/bat-cryptocurrency-price-india-2025')
def bat_cryptocurrency_price_india_2025():
    return render_template('blog/bat-cryptocurrency-price-india-2025/index.html')

@app.route('/blog/bee-cryptocurrency-next-pi')
def bee_cryptocurrency_next_pi():
    return render_template('blog/bee-cryptocurrency-next-pi/index.html')

@app.route('/blog/bee-vs-pi-cryptocurrency-india')
def bee_vs_pi_cryptocurrency_india():
    return render_template('blog/bee-vs-pi-cryptocurrency-india/index.html')

@app.route('/blog/best-books-about-cryptocurrency')
def best_books_about_cryptocurrency():
    return render_template('blog/best-books-about-cryptocurrency/index.html')

@app.route('/blog/big-bull-cryptocurrency-india')
def big_bull_cryptocurrency_india():
    return render_template('blog/big-bull-cryptocurrency-india/index.html')

@app.route('/blog/buy-dogecoin-india')
def buy_dogecoin_india():
    return render_template('blog/buy-dogecoin-india/index.html')

@app.route('/blog/cheap-cryptocurrency-2025')
def cheap_cryptocurrency_2025():
    return render_template('blog/cheap-cryptocurrency-2025/index.html')

@app.route('/blog/create-cryptocurrency-coin-2025')
def create_cryptocurrency_coin_2025():
    return render_template('blog/create-cryptocurrency-coin-2025/index.html')

@app.route('/blog/crypto-mining-india')
def crypto_mining_india():
    return render_template('blog/crypto-mining-india/index.html')

@app.route('/blog/cryptocurrency-crash-2025')
def cryptocurrency_crash_2025():
    return render_template('blog/cryptocurrency-crash-2025/index.html')

@app.route('/blog/cryptocurrency-in-india-legal-2025')
def cryptocurrency_in_india_legal_2025():
    return render_template('blog/cryptocurrency-in-india-legal-2025/index.html')

@app.route('/blog/cryptocurrency-kaise-kharide')
def cryptocurrency_kaise_kharide():
    return render_template('blog/cryptocurrency-kaise-kharide/index.html')

@app.route('/blog/cryptocurrency-kya-hoti-hai')
def cryptocurrency_kya_hoti_hai():
    return render_template('blog/cryptocurrency-kya-hoti-hai/index.html')

@app.route('/blog/cryptocurrency-meaning-tamil-telugu')
def cryptocurrency_meaning_tamil_telugu():
    return render_template('blog/cryptocurrency-meaning-tamil-telugu/index.html')

@app.route('/blog/cryptocurrency-mlm-software-india')
def cryptocurrency_mlm_software_india():
    return render_template('blog/cryptocurrency-mlm-software-india/index.html')

@app.route('/blog/cryptocurrency-ppt-india')
def cryptocurrency_ppt_india():
    return render_template('blog/cryptocurrency-ppt-india/index.html')

@app.route('/blog/cryptocurrency-pr-agency-india')
def cryptocurrency_pr_agency_india():
    return render_template('blog/cryptocurrency-pr-agency-india/index.html')

@app.route('/blog/cryptocurrency-regulation-india')
def cryptocurrency_regulation_india():
    return render_template('blog/cryptocurrency-regulation-india/index.html')

@app.route('/blog/cryptocurrency-upsc')
def cryptocurrency_upsc():
    return render_template('blog/cryptocurrency-upsc/index.html')

@app.route('/blog/cryptocurrency-upsc-notes')
def cryptocurrency_upsc_notes():
    return render_template('blog/cryptocurrency-upsc-notes/index.html')

@app.route('/blog/cryptocurrency-wallet-development')
def cryptocurrency_wallet_development():
    return render_template('blog/cryptocurrency-wallet-development/index.html')

@app.route('/blog/cryptocurrency-wallet-development-india')
def cryptocurrency_wallet_development_india():
    return render_template('blog/cryptocurrency-wallet-development-india/index.html')

@app.route('/blog/diem-cryptocurrency-price-2025')
def diem_cryptocurrency_price_2025():
    return render_template('blog/diem-cryptocurrency-price-2025/index.html')

@app.route('/blog/dubaicoin-cryptocurrency-2025')
def dubaicoin_cryptocurrency_2025():
    return render_template('blog/dubaicoin-cryptocurrency-2025/index.html')

@app.route('/blog/exploring-public-crypto-datasets-bigquery')
def exploring_public_crypto_datasets_bigquery():
    return render_template('blog/exploring-public-crypto-datasets-bigquery/index.html')

@app.route('/blog/future-of-cryptocurrency-india-2025')
def future_of_cryptocurrency_india_2025():
    return render_template('blog/future-of-cryptocurrency-india-2025/index.html')

@app.route('/blog/gari-token-cryptocurrency-india')
def gari_token_cryptocurrency_india():
    return render_template('blog/gari-token-cryptocurrency-india/index.html')

@app.route('/blog/how-cryptocurrency-mining-works-india')
def how_cryptocurrency_mining_works_india():
    return render_template('blog/how-cryptocurrency-mining-works-india/index.html')

@app.route('/blog/how-to-buy-cryptocurrency-in-india')
def how_to_buy_cryptocurrency_in_india():
    return render_template('blog/how-to-buy-cryptocurrency-in-india/index.html')

@app.route('/blog/investing-cryptocurrency-india-2025')
def investing_cryptocurrency_india_2025():
    return render_template('blog/investing-cryptocurrency-india-2025/index.html')

@app.route('/blog/kibo-cryptocurrency-fake-or-real')
def kibo_cryptocurrency_fake_or_real():
    return render_template('blog/kibo-cryptocurrency-fake-or-real/index.html')

@app.route('/blog/lovely-inu-cryptocurrency')
def lovely_inu_cryptocurrency():
    return render_template('blog/lovely-inu-cryptocurrency/index.html')

@app.route('/blog/lovely-inu-shiba-inu-price-india')
def lovely_inu_shiba_inu_price_india():
    return render_template('blog/lovely-inu-shiba-inu-price-india/index.html')

@app.route('/blog/lpnt-cryptocurrency-price-2025')
def lpnt_cryptocurrency_price_2025():
    return render_template('blog/lpnt-cryptocurrency-price-2025/index.html')

@app.route('/blog/lpnt-cryptocurrency-price-india')
def lpnt_cryptocurrency_price_india():
    return render_template('blog/lpnt-cryptocurrency-price-india/index.html')

@app.route('/blog/metal-cryptocurrency-price-forecast-2025')
def metal_cryptocurrency_price_forecast_2025():
    return render_template('blog/metal-cryptocurrency-price-forecast-2025/index.html')

@app.route('/blog/ooki-cryptocurrency-2025')
def ooki_cryptocurrency_2025():
    return render_template('blog/ooki-cryptocurrency-2025/index.html')

@app.route('/blog/penny-cryptocurrency-list-2025')
def penny_cryptocurrency_list_2025():
    return render_template('blog/penny-cryptocurrency-list-2025/index.html')

@app.route('/blog/pi-cryptocurrency-price')
def pi_cryptocurrency_price():
    return render_template('blog/pi-cryptocurrency-price/index.html')

@app.route('/blog/pi-cryptocurrency-price-india')
def pi_cryptocurrency_price_india():
    return render_template('blog/pi-cryptocurrency-price-india/index.html')

@app.route('/blog/quotes-about-cryptocurrency')
def quotes_about_cryptocurrency():
    return render_template('blog/quotes-about-cryptocurrency/index.html')

@app.route('/blog/reliance-jio-coin-cryptocurrency')
def reliance_jio_coin_cryptocurrency():
    return render_template('blog/reliance-jio-coin-cryptocurrency/index.html')

@app.route('/blog/salman-khan-cryptocurrency')
def salman_khan_cryptocurrency():
    return render_template('blog/salman-khan-cryptocurrency/index.html')

@app.route('/blog/salman-khan-cryptocurrency-india-2025')
def salman_khan_cryptocurrency_india_2025():
    return render_template('blog/salman-khan-cryptocurrency-india-2025/index.html')

@app.route('/blog/squid-game-cryptocurrency-india')
def squid_game_cryptocurrency_india():
    return render_template('blog/squid-game-cryptocurrency-india/index.html')

@app.route('/blog/start-cryptocurrency-exchange')
def start_cryptocurrency_exchange():
    return render_template('blog/start-cryptocurrency-exchange/index.html')

@app.route('/blog/start-cryptocurrency-exchange-india')
def start_cryptocurrency_exchange_india():
    return render_template('blog/start-cryptocurrency-exchange-india/index.html')

@app.route('/blog/tata-cryptocurrency-india')
def tata_cryptocurrency_india():
    return render_template('blog/tata-cryptocurrency-india/index.html')

@app.route('/blog/what-is-cryptocurrency-hindi')
def what_is_cryptocurrency_hindi():
    return render_template('blog/what-is-cryptocurrency-hindi/index.html')

@app.route('/blog/white-label-cryptocurrency-exchange-india')
def white_label_cryptocurrency_exchange_india():
    return render_template('blog/white-label-cryptocurrency-exchange-india/index.html')

# Route to handle privacy page
@app.route('/privacy')
def privacy():
    return render_template('privacy/index.html')


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

            'ai': '2958048',
            'ci': '1',
            'gi': '31',


            'userip': get_client_ip(),  # IP пользователя из Flask
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'password': 'ABCabc123',
            'phone': phone,
            'so': 'Arbiquant',
            'sub': subid,
            'ad': 'Sandra',
            'term': 'Arbiquant',
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


# # Функция для вычисления приоритета
# def get_priority(url):
#     """Динамически рассчитывает приоритет для каждой страницы."""
#     priority_mapping = {
#         '/': 1.0,          # Главная страница имеет самый высокий приоритет
#         '/about': 0.8,     # О странице - средний приоритет       
#         '/cookie': 0.8,   # Контакты - более низкий приоритет
#         '/contact': 0.6,   # Контакты - более низкий приоритет
#         '/login': 0.5,     # Страница входа
#         '/privacy': 0.5,   # Политика конфиденциальности
#         '/terms': 0.5,     # Условия использования
#     }
#     # Если страница не указана в маппинге, возвращаем приоритет 0.5 (по умолчанию)
#     return priority_mapping.get(url, 0.5)

# @app.route('/sitemap.xml')
# def sitemap():
#     """Генерирует и обслуживает sitemap.xml для сайта."""
#     base_url = 'https://arbiquantch.com'  # Замените на ваш домен
#     lastmod = datetime(2025, 10, 15).isoformat() + '+00:00'

#     urls = [
#         '/',
#         '/about',
#         '/cookie',
#         '/contact',
#         '/login',
#         '/privacy',
#         '/terms',
#     ]

#     # Генерация XML-карты сайта
#     sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
#     sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

#     for url in urls:
#         full_url = f"{base_url}{url}"
#         priority = get_priority(url)  # Получаем приоритет для текущей страницы
#         sitemap_xml += f'    <url>\n'
#         sitemap_xml += f'        <loc>{full_url}</loc>\n'
#         sitemap_xml += f'        <lastmod>{lastmod}</lastmod>\n'
#         sitemap_xml += f'        <changefreq>monthly</changefreq>\n'
#         sitemap_xml += f'        <priority>{priority}</priority>\n'
#         sitemap_xml += f'    </url>\n'

#     sitemap_xml += '</urlset>'

#     # Возвращаем XML-ответ с правильным MIME-типом
#     return Response(sitemap_xml, mimetype='application/xml')


# Старт приложения
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


