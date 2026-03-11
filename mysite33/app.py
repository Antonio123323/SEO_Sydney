from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, send_file
import os
import requests
import json
import urllib.parse
from datetime import datetime

# Явные пути для корректной работы независимо от рабочей директории
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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

@app.route('/blog/actualites-crypto-2025')
def blog_actualites_crypto_2025():
    return render_template('blog/actualites-crypto-2025/index.html')

@app.route('/blog/actualites-crypto-canada-2025')
def blog_actualites_crypto_canada_2025():
    return render_template('blog/actualites-crypto-canada-2025/index.html')

@app.route('/blog/bitcoin-halving-2025-trading-crypto')
def blog_bitcoin_halving_2025():
    return render_template('blog/bitcoin-halving-2025-trading-crypto/index.html')

@app.route('/blog/bourse-crypto-canada')
def blog_bourse_crypto_canada():
    return render_template('blog/bourse-crypto-canada/index.html')

@app.route('/blog/bourse-crypto-canada-binance-vs-coinbase')
def blog_bourse_crypto_canada_binance_vs_coinbase():
    return render_template('blog/bourse-crypto-canada-binance-vs-coinbase/index.html')

@app.route('/blog/bourse-crypto-canada-direct')
def blog_bourse_crypto_canada_direct():
    return render_template('blog/bourse-crypto-canada-direct/index.html')

@app.route('/blog/celebrites-et-cryptomonnaie-bitcoin-elon-musk')
def blog_celebrites_et_cryptomonnaie_bitcoin_elon_musk():
    return render_template('blog/celebrites-et-cryptomonnaie-bitcoin-elon-musk/index.html')

@app.route('/blog/celebrites-influencent-bitcoin')
def blog_celebrites_influencent_bitcoin():
    return render_template('blog/celebrites-influencent-bitcoin/index.html')

@app.route('/blog/commencer-trader-bourse-crypto-quebec')
def blog_commencer_trader_bourse_crypto_quebec():
    return render_template('blog/commencer-trader-bourse-crypto-quebec/index.html')

@app.route('/blog/comparatif-plateforme-crypto-canada-2025')
def blog_comparatif_plateforme_crypto_canada_2025():
    return render_template('blog/comparatif-plateforme-crypto-canada-2025/index.html')

@app.route('/blog/comprendre-bourse-crypto-investir')
def blog_comprendre_bourse_crypto_investir():
    return render_template('blog/comprendre-bourse-crypto-investir/index.html')

@app.route('/blog/comprendre-cryptomonnaie-simple')
def blog_comprendre_cryptomonnaie_simple():
    return render_template('blog/comprendre-cryptomonnaie-simple/index.html')

@app.route('/blog/creation-cryptomonnaie-2025')
def blog_creation_cryptomonnaie_2025():
    return render_template('blog/creation-cryptomonnaie-2025/index.html')

@app.route('/blog/creer-cryptomonnaie-2025')
def blog_creer_cryptomonnaie_2025():
    return render_template('blog/creer-cryptomonnaie-2025/index.html')

@app.route('/blog/creer-cryptomonnaie-au-canada')
def blog_creer_cryptomonnaie_au_canada():
    return render_template('blog/creer-cryptomonnaie-au-canada/index.html')

@app.route('/blog/creer-cryptomonnaie-canada')
def blog_creer_cryptomonnaie_canada():
    return render_template('blog/creer-cryptomonnaie-canada/index.html')

@app.route('/blog/creer-cryptomonnaie-facilement')
def blog_creer_cryptomonnaie_facilement():
    return render_template('blog/creer-cryptomonnaie-facilement/index.html')

@app.route('/blog/cryptomonnaie-2025-revolution-financiere')
def blog_cryptomonnaie_2025_revolution_financiere():
    return render_template('blog/cryptomonnaie-2025-revolution-financiere/index.html')

@app.route('/blog/cryptomonnaie-celebrites-succes-ou-arnaque')
def blog_cryptomonnaie_celebrites_succes_ou_arnaque():
    return render_template('blog/cryptomonnaie-celebrites-succes-ou-arnaque/index.html')

@app.route('/blog/cryptomonnaie-economie-numerique-canada')
def blog_cryptomonnaie_economie_numerique_canada():
    return render_template('blog/cryptomonnaie-economie-numerique-canada/index.html')

@app.route('/blog/cryptomonnaie-verte-revolution-ecologique')
def blog_cryptomonnaie_verte_revolution_ecologique():
    return render_template('blog/cryptomonnaie-verte-revolution-ecologique/index.html')

@app.route('/blog/cryptomonnaies-prometteuses-canada-2025')
def blog_cryptomonnaies_prometteuses_canada_2025():
    return render_template('blog/cryptomonnaies-prometteuses-canada-2025/index.html')

@app.route('/blog/de-musk-a-trump-crypto-celebrites')
def blog_de_musk_a_trump_crypto_celebrites():
    return render_template('blog/de-musk-a-trump-crypto-celebrites/index.html')

@app.route('/blog/elon-musk-cryptomonnaie-fortune-numerique')
def blog_elon_musk_cryptomonnaie_fortune_numerique():
    return render_template('blog/elon-musk-cryptomonnaie-fortune-numerique/index.html')

@app.route('/blog/equipement-minage-cryptomonnaie-2025')
def blog_equipement_minage_cryptomonnaie_2025():
    return render_template('blog/equipement-minage-cryptomonnaie-2025/index.html')

@app.route('/blog/erreurs-minage-cryptomonnaie')
def blog_erreurs_minage_cryptomonnaie():
    return render_template('blog/erreurs-minage-cryptomonnaie/index.html')

@app.route('/blog/essor-plateformes-crypto-quebec')
def blog_essor_plateformes_crypto_quebec():
    return render_template('blog/essor-plateformes-crypto-quebec/index.html')

@app.route('/blog/gerer-emotions-trading-cryptomonnaie')
def blog_gerer_emotions_trading_cryptomonnaie():
    return render_template('blog/gerer-emotions-trading-cryptomonnaie/index.html')

@app.route('/blog/histoire-actualites-crypto')
def blog_histoire_actualites_crypto():
    return render_template('blog/histoire-actualites-crypto/index.html')

@app.route('/blog/ia-bourse-crypto-canada')
def blog_ia_bourse_crypto_canada():
    return render_template('blog/ia-bourse-crypto-canada/index.html')

@app.route('/blog/ia-crypto-bourse-revolution')
def blog_ia_crypto_bourse_revolution():
    return render_template('blog/ia-crypto-bourse-revolution/index.html')

@app.route('/blog/investir-bourse-crypto-canada-erreurs-eviter')
def blog_investir_bourse_crypto_canada_erreurs_eviter():
    return render_template('blog/investir-bourse-crypto-canada-erreurs-eviter/index.html')

@app.route('/blog/jeunes-bourse-crypto-quebec')
def blog_jeunes_bourse_crypto_quebec():
    return render_template('blog/jeunes-bourse-crypto-quebec/index.html')

@app.route('/blog/jeunes-crypto-quebec')
def blog_jeunes_crypto_quebec():
    return render_template('blog/jeunes-crypto-quebec/index.html')

@app.route('/blog/la-presse-crypto-canada')
def blog_la_presse_crypto_canada():
    return render_template('blog/la-presse-crypto-canada/index.html')

@app.route('/blog/le-futur-de-la-cryptomonnaie-opportunite-ou-illusion-numerique')
def blog_le_futur_de_la_cryptomonnaie():
    return render_template('blog/le-futur-de-la-cryptomonnaie-opportunite-ou-illusion-numerique/index.html')

@app.route('/blog/les-cryptomonnaies-expliquees-comprendre-avant-investir')
def blog_les_cryptomonnaies_expliquees():
    return render_template('blog/les-cryptomonnaies-expliquees-comprendre-avant-investir/index.html')

@app.route('/blog/meilleures-plateformes-crypto-canada-2025')
def blog_meilleures_plateformes_crypto_canada_2025():
    return render_template('blog/meilleures-plateformes-crypto-canada-2025/index.html')

@app.route('/blog/minage-cryptomonnaie-2025')
def blog_minage_cryptomonnaie_2025():
    return render_template('blog/minage-cryptomonnaie-2025/index.html')

@app.route('/blog/minage-cryptomonnaie-canada')
def blog_minage_cryptomonnaie_canada():
    return render_template('blog/minage-cryptomonnaie-canada/index.html')

@app.route('/blog/normand-brathwaite-cryptomonnaie-quebec-verite')
def blog_normand_brathwaite():
    return render_template('blog/normand-brathwaite-cryptomonnaie-quebec-verite/index.html')

@app.route('/blog/plateforme-crypto-centralisee-ou-decentralisee')
def blog_plateforme_crypto_centralisee_ou_decentralisee():
    return render_template('blog/plateforme-crypto-centralisee-ou-decentralisee/index.html')

@app.route('/blog/previsions-2025-actualites-crypto')
def blog_previsions_2025_actualites_crypto():
    return render_template('blog/previsions-2025-actualites-crypto/index.html')

@app.route('/blog/pourquoi-cryptomonnaies-populaires-canada')
def blog_pourquoi_cryptomonnaies_populaires_canada():
    return render_template('blog/pourquoi-cryptomonnaies-populaires-canada/index.html')

@app.route('/blog/quest-ce-quune-cryptomonnaie-definition-simple')
def blog_quest_ce_quune_cryptomonnaie():
    return render_template('blog/quest-ce-quune-cryptomonnaie-definition-simple/index.html')

@app.route('/blog/top-5-cryptos-rentables-2025')
def blog_top_5_cryptos_rentables_2025():
    return render_template('blog/top-5-cryptos-rentables-2025/index.html')

@app.route('/blog/top-5-plateformes-crypto-quebec-2025-plateforme-crypto')
def blog_top_5_plateformes_crypto_quebec_2025():
    return render_template('blog/top-5-plateformes-crypto-quebec-2025-plateforme-crypto/index.html')

@app.route('/blog/trading-cryptomonnaie-vs-investissement')
def blog_trading_cryptomonnaie_vs_investissement():
    return render_template('blog/trading-cryptomonnaie-vs-investissement/index.html')

@app.route('/blog/trading-social-cryptomonnaie')
def blog_trading_social_cryptomonnaie():
    return render_template('blog/trading-social-cryptomonnaie/index.html')

@app.route('/blog/trading-vs-investissement')
def blog_trading_vs_investissement():
    return render_template('blog/trading-vs-investissement/index.html')

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
    """Генерирует sitemap.xml автоматически из зарегистрированных маршрутов."""
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
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>'
    return Response(xml, mimetype='application/xml', headers={'Content-Type': 'application/xml; charset=utf-8'})


# Старт приложения
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


