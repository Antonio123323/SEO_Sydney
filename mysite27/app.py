from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, send_file
import os
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

@app.route('/blog/ai-crypto-bots-uk')
def ai_crypto_bots_uk():
    return render_template('blog/ai-crypto-bots-uk/index.html')

@app.route('/blog/ai-crypto-trading-uk')
def ai_crypto_trading_uk():
    return render_template('blog/ai-crypto-trading-uk/index.html')

@app.route('/blog/avoid-crypto-scams-uk')
def avoid_crypto_scams_uk():
    return render_template('blog/avoid-crypto-scams-uk/index.html')

@app.route('/blog/bitcoin-halving-uk')
def bitcoin_halving_uk():
    return render_template('blog/bitcoin-halving-uk/index.html')

@app.route('/blog/blockchain-courses-uk')
def blockchain_courses_uk():
    return render_template('blog/blockchain-courses-uk/index.html')

@app.route('/blog/brexit-crypto-uk')
def brexit_crypto_uk():
    return render_template('blog/brexit-crypto-uk/index.html')

@app.route('/blog/buy-bitcoin-uk')
def buy_bitcoin_uk():
    return render_template('blog/buy-bitcoin-uk/index.html')

@app.route('/blog/crypto-apps-uk')
def crypto_apps_uk():
    return render_template('blog/crypto-apps-uk/index.html')

@app.route('/blog/crypto-arbitrage-uk')
def crypto_arbitrage_uk():
    return render_template('blog/crypto-arbitrage-uk/index.html')

@app.route('/blog/crypto-bull-run-uk')
def crypto_bull_run_uk():
    return render_template('blog/crypto-bull-run-uk/index.html')

@app.route('/blog/crypto-business-london')
def crypto_business_london():
    return render_template('blog/crypto-business-london/index.html')

@app.route('/blog/crypto-challenges-uk')
def crypto_challenges_uk():
    return render_template('blog/crypto-challenges-uk/index.html')

@app.route('/blog/crypto-cold-storage-uk')
def crypto_cold_storage_uk():
    return render_template('blog/crypto-cold-storage-uk/index.html')

@app.route('/blog/crypto-credit-cards-uk')
def crypto_credit_cards_uk():
    return render_template('blog/crypto-credit-cards-uk/index.html')

@app.route('/blog/crypto-education-uk')
def crypto_education_uk():
    return render_template('blog/crypto-education-uk/index.html')

@app.route('/blog/crypto-etf-uk')
def crypto_etf_uk():
    return render_template('blog/crypto-etf-uk/index.html')

@app.route('/blog/crypto-events-london')
def crypto_events_london():
    return render_template('blog/crypto-events-london/index.html')

@app.route('/blog/crypto-friendly-banks-uk')
def crypto_friendly_banks_uk():
    return render_template('blog/crypto-friendly-banks-uk/index.html')

@app.route('/blog/crypto-influencers-uk')
def crypto_influencers_uk():
    return render_template('blog/crypto-influencers-uk/index.html')

@app.route('/blog/crypto-investment-uk')
def crypto_investment_uk():
    return render_template('blog/crypto-investment-uk/index.html')

@app.route('/blog/crypto-loans-uk')
def crypto_loans_uk():
    return render_template('blog/crypto-loans-uk/index.html')

@app.route('/blog/crypto-market-uk-2025')
def crypto_market_uk_2025():
    return render_template('blog/crypto-market-uk-2025/index.html')

@app.route('/blog/crypto-mining-uk')
def crypto_mining_uk():
    return render_template('blog/crypto-mining-uk/index.html')

@app.route('/blog/crypto-projects-uk-2025')
def crypto_projects_uk_2025():
    return render_template('blog/crypto-projects-uk-2025/index.html')

@app.route('/blog/crypto-regulations-uk-2025')
def crypto_regulations_uk_2025():
    return render_template('blog/crypto-regulations-uk-2025/index.html')

@app.route('/blog/crypto-startups-london')
def crypto_startups_london():
    return render_template('blog/crypto-startups-london/index.html')

@app.route('/blog/crypto-stock-apps-uk')
def crypto_stock_apps_uk():
    return render_template('blog/crypto-stock-apps-uk/index.html')

@app.route('/blog/crypto-tax-uk-2025')
def crypto_tax_uk_2025():
    return render_template('blog/crypto-tax-uk-2025/index.html')

@app.route('/blog/crypto-trading-uk')
def crypto_trading_uk():
    return render_template('blog/crypto-trading-uk/index.html')

@app.route('/blog/crypto-wallets-uk')
def crypto_wallets_uk():
    return render_template('blog/crypto-wallets-uk/index.html')

@app.route('/blog/defi-guide-uk')
def defi_guide_uk():
    return render_template('blog/defi-guide-uk/index.html')

@app.route('/blog/defi-platforms-uk')
def defi_platforms_uk():
    return render_template('blog/defi-platforms-uk/index.html')

@app.route('/blog/diversify-crypto-uk')
def diversify_crypto_uk():
    return render_template('blog/diversify-crypto-uk/index.html')

@app.route('/blog/fca-crypto-ads-uk')
def fca_crypto_ads_uk():
    return render_template('blog/fca-crypto-ads-uk/index.html')

@app.route('/blog/fca-crypto-banks-uk')
def fca_crypto_banks_uk():
    return render_template('blog/fca-crypto-banks-uk/index.html')

@app.route('/blog/fca-crypto-exchanges-uk')
def fca_crypto_exchanges_uk():
    return render_template('blog/fca-crypto-exchanges-uk/index.html')

@app.route('/blog/gbp-stablecoin-uk')
def gbp_stablecoin_uk():
    return render_template('blog/gbp-stablecoin-uk/index.html')

@app.route('/blog/hmrc-crypto-tax-uk')
def hmrc_crypto_tax_uk():
    return render_template('blog/hmrc-crypto-tax-uk/index.html')

@app.route('/blog/hmrc-crypto-tracking')
def hmrc_crypto_tracking():
    return render_template('blog/hmrc-crypto-tracking/index.html')

@app.route('/blog/nft-tax-uk-2025')
def nft_tax_uk_2025():
    return render_template('blog/nft-tax-uk-2025/index.html')

@app.route('/blog/prop-trading-london')
def prop_trading_london():
    return render_template('blog/prop-trading-london/index.html')

@app.route('/blog/reduce-crypto-tax-uk')
def reduce_crypto_tax_uk():
    return render_template('blog/reduce-crypto-tax-uk/index.html')

@app.route('/blog/send-gbp-binance-uk')
def send_gbp_binance_uk():
    return render_template('blog/send-gbp-binance-uk/index.html')

@app.route('/blog/stablecoins-uk-2025')
def stablecoins_uk_2025():
    return render_template('blog/stablecoins-uk-2025/index.html')

@app.route('/blog/staking-crypto-uk')
def staking_crypto_uk():
    return render_template('blog/staking-crypto-uk/index.html')

@app.route('/blog/trading-courses-uk')
def trading_courses_uk():
    return render_template('blog/trading-courses-uk/index.html')

@app.route('/blog/trading-psychology-uk')
def trading_psychology_uk():
    return render_template('blog/trading-psychology-uk/index.html')

@app.route('/blog/tradingview-crypto-uk')
def tradingview_crypto_uk():
    return render_template('blog/tradingview-crypto-uk/index.html')

@app.route('/blog/uk-crypto-outlook')
def uk_crypto_outlook():
    return render_template('blog/uk-crypto-outlook/index.html')

@app.route('/blog/uk-crypto-regulation')
def uk_crypto_regulation():
    return render_template('blog/uk-crypto-regulation/index.html')

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
    sitemap_path = os.path.join(app.root_path, 'templates', 'sitemap.xml')
    response = send_file(sitemap_path, mimetype='application/xml', as_attachment=False)
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return response


# Старт приложения
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


