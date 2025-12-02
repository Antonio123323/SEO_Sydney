#!/bin/bash
# Скрипт добавления нового сайта
# Использование: ./add_site.sh папка домен
# Пример: ./add_site.sh mysite24 example.com

set -e

if [ $# -ne 2 ]; then
    echo "Использование: $0 <папка> <домен>"
    echo "Пример: $0 mysite24 example.com"
    exit 1
fi

FOLDER=$1
DOMAIN=$2
SERVICE_NAME=$FOLDER

echo "=========================================="
echo "Добавление сайта: $SERVICE_NAME -> $DOMAIN"
echo "=========================================="

# Проверка существования папки
if [ ! -d "$FOLDER" ]; then
    echo "Ошибка: Папка $FOLDER не существует!"
    exit 1
fi

# Создание конфигурации Nginx
echo "Создание конфигурации Nginx..."

# Проверка и создание директории nginx/conf.d если её нет
if [ ! -d "nginx/conf.d" ]; then
    mkdir -p nginx/conf.d
    echo "✅ Создана директория nginx/conf.d"
fi

NGINX_CONF="nginx/conf.d/${DOMAIN}.conf"

cat > "$NGINX_CONF" << EOF
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    return 301 https://${DOMAIN}\$request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name ${DOMAIN} www.${DOMAIN};

    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

    if (\$host = www.${DOMAIN}) {
        return 301 https://${DOMAIN}\$request_uri;
    }

    location / {
        set \$upstream http://${SERVICE_NAME}:5000;
        proxy_pass \$upstream;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_redirect off;
    }

    location /static {
        set \$upstream http://${SERVICE_NAME}:5000;
        proxy_pass \$upstream;
        proxy_cache_valid 200 1d;
        add_header Cache-Control "public, max-age=86400";
    }
}
EOF

echo "✅ Конфигурация Nginx создана: $NGINX_CONF"

# Добавление сервиса в docker-compose.yml
echo "Добавление сервиса в docker-compose.yml..."

# Проверка существования сервиса
if grep -q "  ${SERVICE_NAME}:" docker-compose.yml; then
    echo "⚠️  Сервис $SERVICE_NAME уже существует в docker-compose.yml"
else
    # Создаем временный файл с новым сервисом
    cat > /tmp/new_service.yml << EOF
  # Flask приложение для ${DOMAIN}
  ${SERVICE_NAME}:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ${SERVICE_NAME}
    working_dir: /app
    volumes:
      - ./${FOLDER}:/app
    environment:
      - FLASK_ENV=production
    expose:
      - "5000"
    restart: unless-stopped
    networks:
      - flask_network

EOF
    
    # Вставляем перед networks:
    awk -v new_service="$(cat /tmp/new_service.yml)" '
        /^networks:/ {
            print new_service
        }
        {print}
    ' docker-compose.yml > docker-compose.yml.tmp && mv docker-compose.yml.tmp docker-compose.yml
    rm /tmp/new_service.yml
    
    echo "✅ Сервис добавлен в docker-compose.yml"
fi

# Добавление в depends_on nginx
if ! grep -q "      - ${SERVICE_NAME}" docker-compose.yml; then
    # Находим последнюю строку с - mysite в depends_on и добавляем после неё
    awk -v service="${SERVICE_NAME}" '
        /nginx:/ { in_nginx=1 }
        in_nginx && /depends_on:/ { in_depends=1; print; next }
        in_depends && /      - mysite/ { 
            # Сохраняем все зависимости в массив для проверки дубликатов
            deps[NR] = $0
            if ($0 !~ service) {
                print
                if (!added) {
                    print "      - " service
                    added = 1
                }
            }
            next
        }
        in_depends && /restart:/ { 
            if (!added) {
                print "      - " service
            }
            in_depends=0; in_nginx=0 
        }
        { print }
    ' docker-compose.yml > docker-compose.yml.tmp && mv docker-compose.yml.tmp docker-compose.yml
    
    # Удаляем дубликаты в depends_on
    awk '
        /nginx:/ { in_nginx=1 }
        in_nginx && /depends_on:/ { 
            print
            in_depends=1
            seen[""] = ""
            next
        }
        in_depends && /      - / {
            if (!seen[$0]++) {
                print
            }
            next
        }
        in_depends && /restart:/ {
            in_depends=0
            in_nginx=0
        }
        { print }
    ' docker-compose.yml > docker-compose.yml.tmp && mv docker-compose.yml.tmp docker-compose.yml
    
    echo "✅ Зависимость добавлена в nginx"
fi

# Получение SSL сертификата
echo ""
echo "Получение SSL сертификата для $DOMAIN..."
read -p "Получить SSL сертификат через certbot? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if ! command -v certbot &> /dev/null; then
        echo "Установка certbot..."
        apt update
        apt install -y certbot python3-certbot-nginx
    fi
    
    echo "Получение сертификата..."
    
    # Проверка наличия системного nginx (установлен, но может быть остановлен)
    if command -v nginx &> /dev/null; then
        echo "Использование nginx плагина для получения сертификата..."
        # Запускаем nginx временно для certbot, если он остановлен
        if ! systemctl is-active --quiet nginx 2>/dev/null; then
            echo "Запуск системного nginx для certbot..."
            systemctl start nginx
        fi
        
        certbot --nginx \
            -d "$DOMAIN" \
            -d "www.$DOMAIN" \
            --email caleb1martinez12345@gmail.com \
            --agree-tos \
            --non-interactive || {
            echo "⚠️  Ошибка через nginx плагин. Пробуем standalone..."
            
            # Останавливаем nginx и контейнеры для standalone
            systemctl stop nginx 2>/dev/null || true
            docker compose down 2>/dev/null || true
            sleep 2
            
            certbot certonly --standalone \
                -d "$DOMAIN" \
                -d "www.$DOMAIN" \
                --email caleb1martinez12345@gmail.com \
                --agree-tos \
                --non-interactive \
                --preferred-challenges http || echo "⚠️  Ошибка получения сертификата. Получите вручную: certbot --nginx -d $DOMAIN"
        }
        
        # Останавливаем системный nginx обратно (если автозапуск отключен)
        if ! systemctl is-enabled --quiet nginx 2>/dev/null; then
            systemctl stop nginx 2>/dev/null || true
        fi
    else
        # Используем standalone режим, если nginx не установлен
        echo "Остановка контейнеров для standalone режима..."
        docker compose down 2>/dev/null || true
        sleep 2
        
        certbot certonly --standalone \
            -d "$DOMAIN" \
            -d "www.$DOMAIN" \
            --email caleb1martinez12345@gmail.com \
            --agree-tos \
            --non-interactive \
            --preferred-challenges http || echo "⚠️  Ошибка получения сертификата. Установите nginx или получите вручную: certbot certonly --standalone -d $DOMAIN"
    fi
    
    # Запуск контейнеров обратно (если были остановлены)
    if ! docker compose ps | grep -q "Up"; then
        echo "Запуск контейнеров..."
        docker compose up -d 2>/dev/null || true
    fi
    
    # Обновление docker-compose.yml для SSL (если еще не добавлен)
    if ! grep -q "/etc/letsencrypt:/etc/letsencrypt:ro" docker-compose.yml; then
        sed -i 's|      # - /etc/letsencrypt:/etc/letsencrypt:ro|      - /etc/letsencrypt:/etc/letsencrypt:ro|g' docker-compose.yml
    fi
fi

echo ""
echo "=========================================="
echo "✅ Готово!"
echo "=========================================="
echo ""
echo "Запустите контейнеры:"
echo "  docker compose up -d --build"
echo ""