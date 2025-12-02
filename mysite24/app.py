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
    return redirect(url_for('index'), code=301)

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
# @app.route('/cookie')
# def cookie():
#     return render_template('cookie/index.html')

# Route to handle blog page
@app.route('/blog')
def blog():
    return render_template('blog/index.html')

# Routes for blog subdirectories
@app.route('/ai-bitcoin-mining')
def ai_bitcoin_mining():
    return render_template('blog/ai-bitcoin-mining/index.html')

@app.route('/ai-bitcoin-price-prediction-uae')
def ai_bitcoin_price_prediction_uae():
    return render_template('blog/ai-bitcoin-price-prediction-uae/index.html')

@app.route('/ai-crypto-future-uae')
def ai_crypto_future_uae():
    return render_template('blog/ai-crypto-future-uae/index.html')

@app.route('/best-crypto-to-invest-uae-2025')
def best_crypto_to_invest_uae_2025():
    return render_template('blog/best-crypto-to-invest-uae-2025/index.html')

@app.route('/best-crypto-uae')
def best_crypto_uae():
    return render_template('blog/best-crypto-uae/index.html')

@app.route('/best-crypto-uae-wallet')
def best_crypto_uae_wallet():
    return render_template('blog/best-crypto-uae-wallet/index.html')

@app.route('/best-crypto-wallet-uae')
def best_crypto_wallet_uae():
    return render_template('blog/best-crypto-wallet-uae/index.html')

@app.route('/bitcoin-2025-halving-profits')
def bitcoin_2025_halving_profits():
    return render_template('blog/bitcoin-2025-halving-profits/index.html')

@app.route('/bitcoin-halving-2025-analysis')
def bitcoin_halving_2025_analysis():
    return render_template('blog/bitcoin-halving-2025-analysis/index.html')

@app.route('/bitcoin-mining-apps')
def bitcoin_mining_apps():
    return render_template('blog/bitcoin-mining-apps/index.html')

@app.route('/bitcoin-mining-apps-2025')
def bitcoin_mining_apps_2025():
    return render_template('blog/bitcoin-mining-apps-2025/index.html')

@app.route('/bitcoin-mining-future-2025')
def bitcoin_mining_future_2025():
    return render_template('blog/bitcoin-mining-future-2025/index.html')

@app.route('/bitcoin-mining-home-uae')
def bitcoin_mining_home_uae():
    return render_template('blog/bitcoin-mining-home-uae/index.html')

@app.route('/bitcoin-price-change')
def bitcoin_price_change():
    return render_template('blog/bitcoin-price-change/index.html')

@app.route('/bitcoin-price-forecast-uae-2025')
def bitcoin_price_forecast_uae_2025():
    return render_template('blog/bitcoin-price-forecast-uae-2025/index.html')

@app.route('/bitcoin-safe-investment-uae-2025')
def bitcoin_safe_investment_uae_2025():
    return render_template('blog/bitcoin-safe-investment-uae-2025/index.html')

@app.route('/bitcoin-supply-demand')
def bitcoin_supply_demand():
    return render_template('blog/bitcoin-supply-demand/index.html')

@app.route('/bitcoin-uae-2025')
def bitcoin_uae_2025():
    return render_template('blog/bitcoin-uae-2025/index.html')

@app.route('/btc-vs-eth-uae')
def btc_vs_eth_uae():
    return render_template('blog/btc-vs-eth-uae/index.html')

@app.route('/buy-bitcoin-in-uae-with-credit-card')
def buy_bitcoin_in_uae_with_credit_card():
    return render_template('blog/buy-bitcoin-in-uae-with-credit-card/index.html')

@app.route('/buy-crypto-in-uae')
def buy_crypto_in_uae():
    return render_template('blog/buy-crypto-in-uae/index.html')

@app.route('/cloud-mining-uae')
def cloud_mining_uae():
    return render_template('blog/cloud-mining-uae/index.html')

@app.route('/cloud-vs-traditional-mining')
def cloud_vs_traditional_mining():
    return render_template('blog/cloud-vs-traditional-mining/index.html')

@app.route('/crypto-2025-trends')
def crypto_2025_trends():
    return render_template('blog/crypto-2025-trends/index.html')

@app.route('/crypto-abu-dhabi')
def crypto_abu_dhabi():
    return render_template('blog/crypto-abu-dhabi/index.html')

@app.route('/crypto-ai-uae')
def crypto_ai_uae():
    return render_template('blog/crypto-ai-uae/index.html')

@app.route('/crypto-browser-wallet-uae')
def crypto_browser_wallet_uae():
    return render_template('blog/crypto-browser-wallet-uae/index.html')

@app.route('/crypto-buy-uae')
def crypto_buy_uae():
    return render_template('blog/crypto-buy-uae/index.html')

@app.route('/crypto-coins-comparison')
def crypto_coins_comparison():
    return render_template('blog/crypto-coins-comparison/index.html')

@app.route('/crypto-future-financial-system')
def crypto_future_financial_system():
    return render_template('blog/crypto-future-financial-system/index.html')

@app.route('/crypto-invest-tips')
def crypto_invest_tips():
    return render_template('blog/crypto-invest-tips/index.html')

@app.route('/crypto-labs-digital-wallets-uae-2025')
def crypto_labs_digital_wallets_uae_2025():
    return render_template('blog/crypto-labs-digital-wallets-uae-2025/index.html')

@app.route('/crypto-license-uae')
def crypto_license_uae():
    return render_template('blog/crypto-license-uae/index.html')

@app.route('/crypto-market-analysis-uae')
def crypto_market_analysis_uae():
    return render_template('blog/crypto-market-analysis-uae/index.html')

@app.route('/crypto-market-dubai')
def crypto_market_dubai():
    return render_template('blog/crypto-market-dubai/index.html')

@app.route('/crypto-projects-dubai-2025')
def crypto_projects_dubai_2025():
    return render_template('blog/crypto-projects-dubai-2025/index.html')

@app.route('/crypto-real-uae')
def crypto_real_uae():
    return render_template('blog/crypto-real-uae/index.html')

@app.route('/crypto-trends-buying-uae-2025')
def crypto_trends_buying_uae_2025():
    return render_template('blog/crypto-trends-buying-uae-2025/index.html')

@app.route('/crypto-trends-uae-2025')
def crypto_trends_uae_2025():
    return render_template('blog/crypto-trends-uae-2025/index.html')

@app.route('/crypto-uae')
def crypto_uae():
    return render_template('blog/crypto-uae/index.html')

@app.route('/crypto-wallet-2025')
def crypto_wallet_2025():
    return render_template('blog/crypto-wallet-2025/index.html')

@app.route('/crypto-wallet-guide-uae')
def crypto_wallet_guide_uae():
    return render_template('blog/crypto-wallet-guide-uae/index.html')

@app.route('/green-crypto-future')
def green_crypto_future():
    return render_template('blog/green-crypto-future/index.html')

@app.route('/ma-hiya-alomlat-almushafara')
def ma_hiya_alomlat_almushafara():
    return render_template('blog/ma-hiya-alomlat-almushafara/index.html')

@app.route('/mustaqbal-crypto-uae-2025')
def mustaqbal_crypto_uae_2025():
    return render_template('blog/mustaqbal-crypto-uae-2025/index.html')

@app.route('/rising-cryptos-2025-uae')
def rising_cryptos_2025_uae():
    return render_template('blog/rising-cryptos-2025-uae/index.html')

@app.route('/smart-crypto-wallet-uae-2025')
def smart_crypto_wallet_uae_2025():
    return render_template('blog/smart-crypto-wallet-uae-2025/index.html')

@app.route('/start-crypto-investment-uae')
def start_crypto_investment_uae():
    return render_template('blog/start-crypto-investment-uae/index.html')

@app.route('/sustainable-bitcoin-mining-uae')
def sustainable_bitcoin_mining_uae():
    return render_template('blog/sustainable-bitcoin-mining-uae/index.html')

@app.route('/what-is-bitcoin-mining-uae-2025')
def what_is_bitcoin_mining_uae_2025():
    return render_template('blog/what-is-bitcoin-mining-uae-2025/index.html')

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


# Функция для вычисления приоритета
def get_priority(url):
    """Динамически рассчитывает приоритет для каждой страницы."""
    priority_mapping = {
        '/': 1.0,          # Главная страница имеет самый высокий приоритет
        '/about': 0.8,     # О странице - средний приоритет       
        '/blog': 0.8,   # Контакты - более низкий приоритет
        '/contact': 0.6,   # Контакты - более низкий приоритет
        '/privacy': 0.5,   # Политика конфиденциальности
        '/terms': 0.5,     # Условия использования
    }
    # Если страница не указана в маппинге, возвращаем приоритет 0.5 (по умолчанию)
    return priority_mapping.get(url, 0.5)

# @app.route('/sitemap.xml')
# def sitemap():
#     """Генерирует и обслуживает sitemap.xml для сайта."""
#     base_url = 'https://cryptohorizon-ae.com'  # Замените на ваш домен
#     lastmod = datetime(2025, 10, 15).isoformat() + '+00:00'

#     urls = [
#         '/',
#         '/about',
#         '/blog',
#         '/contact',
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


