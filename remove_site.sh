#!/bin/bash
# Скрипт удаления конфигурации сайта из nginx и docker-compose.yml
# Использование: ./remove_site.sh имя_сервиса домен
# Пример: ./remove_site.sh mysite24 cryptohorizon-ae.com

set -e

if [ $# -ne 2 ]; then
    echo "Использование: $0 <имя_сервиса> <домен>"
    echo "Пример: $0 mysite24 cryptohorizon-ae.com"
    exit 1
fi

SERVICE_NAME=$1
DOMAIN=$2
NGINX_CONF="nginx/conf.d/${DOMAIN}.conf"

echo "=========================================="
echo "Удаление сайта: $SERVICE_NAME -> $DOMAIN"
echo "=========================================="

# Удаление конфигурации nginx (если существует)
# Ищем файлы конфигурации, которые могут содержать домен (включая варианты с символами)
NGINX_REMOVED=0
BACKUP_DIR="nginx/conf.d/backups"
mkdir -p "$BACKUP_DIR"

# Ищем все возможные варианты имени файла конфигурации
POSSIBLE_CONFS=(
    "${NGINX_CONF}"
    "nginx/conf.d/${DOMAIN}#.conf"
    "nginx/conf.d/${DOMAIN}*.conf"
)

FOUND_CONF=""

# Проверяем точное совпадение
if [ -f "$NGINX_CONF" ]; then
    FOUND_CONF="$NGINX_CONF"
else
    # Ищем файлы, содержащие домен в имени (включая варианты с #)
    for conf_file in nginx/conf.d/*.conf; do
        if [ -f "$conf_file" ]; then
            # Проверяем, содержит ли файл упоминание домена
            if grep -q "$DOMAIN" "$conf_file" 2>/dev/null; then
                FOUND_CONF="$conf_file"
                break
            fi
        fi
    done
fi

if [ -n "$FOUND_CONF" ] && [ -f "$FOUND_CONF" ]; then
    echo "Удаление конфигурации nginx: $FOUND_CONF"
    
    # Создаем резервную копию перед удалением
    BACKUP_FILE="${BACKUP_DIR}/$(basename $FOUND_CONF).$(date +%Y%m%d_%H%M%S).bak"
    cp "$FOUND_CONF" "$BACKUP_FILE"
    echo "✅ Создана резервная копия: $BACKUP_FILE"
    
    # Удаляем файл конфигурации
    rm "$FOUND_CONF"
    echo "✅ Удален файл конфигурации: $FOUND_CONF"
    NGINX_REMOVED=1
else
    echo "⚠️  Файл конфигурации для $DOMAIN не найден (пропускаем)"
    NGINX_REMOVED=0
fi

# Проверяем синтаксис nginx (если конфигурация была удалена и контейнер запущен)
if [ "$NGINX_REMOVED" -eq 1 ] && docker ps | grep -q nginx_proxy; then
    echo ""
    echo "Проверка синтаксиса конфигурации nginx..."
    if docker exec nginx_proxy nginx -t 2>&1 | grep -q "syntax is ok"; then
        echo "✅ Синтаксис конфигурации nginx корректен"
        echo ""
        echo "Перезагрузка конфигурации nginx..."
        if docker exec nginx_proxy nginx -s reload; then
            echo "✅ Конфигурация nginx успешно перезагружена"
        else
            echo "⚠️  Не удалось перезагрузить конфигурацию, перезапускаю контейнер..."
            docker compose restart nginx
        fi
    else
        echo "❌ Ошибка в синтаксисе конфигурации nginx!"
        docker exec nginx_proxy nginx -t
        echo ""
        echo "⚠️  Восстановите файл из резервной копии:"
        echo "   cp $BACKUP_FILE $NGINX_CONF"
        exit 1
    fi
fi

# Удаление SSL сертификатов Let's Encrypt
echo ""
echo "Удаление SSL сертификатов..."

CERT_LIVE="/etc/letsencrypt/live/${DOMAIN}"
CERT_ARCHIVE="/etc/letsencrypt/archive/${DOMAIN}"
CERT_RENEWAL="/etc/letsencrypt/renewal/${DOMAIN}.conf"

CERT_REMOVED=0

# Пытаемся удалить через certbot (предпочтительный способ)
if command -v certbot >/dev/null 2>&1; then
    if certbot certificates 2>/dev/null | grep -q "Certificate Name: ${DOMAIN}"; then
        echo "Найден сертификат для $DOMAIN, удаление через certbot..."
        if sudo certbot delete --cert-name "$DOMAIN" --non-interactive 2>/dev/null; then
            echo "✅ Сертификат $DOMAIN успешно удален через certbot"
            CERT_REMOVED=1
        else
            echo "⚠️  Не удалось удалить через certbot, попробуем вручную..."
        fi
    else
        echo "✅ Сертификат для $DOMAIN не найден в certbot"
    fi
fi

# Если certbot не удалось использовать или не установлен, удаляем вручную
if [ "$CERT_REMOVED" -eq 0 ]; then
    # Проверяем наличие сертификатов
    if [ -d "$CERT_LIVE" ] || [ -d "$CERT_ARCHIVE" ] || [ -f "$CERT_RENEWAL" ]; then
        echo "Найдены файлы сертификатов для $DOMAIN, удаление..."
        
        if [ -d "$CERT_LIVE" ]; then
            sudo rm -rf "$CERT_LIVE" 2>/dev/null && echo "✅ Удален $CERT_LIVE" || echo "⚠️  Не удалось удалить $CERT_LIVE (требуются права root)"
        fi
        
        if [ -d "$CERT_ARCHIVE" ]; then
            sudo rm -rf "$CERT_ARCHIVE" 2>/dev/null && echo "✅ Удален $CERT_ARCHIVE" || echo "⚠️  Не удалось удалить $CERT_ARCHIVE (требуются права root)"
        fi
        
        if [ -f "$CERT_RENEWAL" ]; then
            sudo rm -f "$CERT_RENEWAL" 2>/dev/null && echo "✅ Удален $CERT_RENEWAL" || echo "⚠️  Не удалось удалить $CERT_RENEWAL (требуются права root)"
        fi
        
        CERT_REMOVED=1
    else
        echo "✅ Сертификаты для $DOMAIN не найдены"
    fi
fi

# Если не удалось удалить автоматически, выводим инструкции
if [ "$CERT_REMOVED" -eq 0 ] && ( [ -d "$CERT_LIVE" ] || [ -d "$CERT_ARCHIVE" ] || [ -f "$CERT_RENEWAL" ] ); then
    echo ""
    echo "⚠️  Не удалось автоматически удалить сертификаты"
    echo "   Выполните вручную:"
    echo "   sudo certbot delete --cert-name $DOMAIN"
    echo "   или:"
    echo "   sudo rm -rf $CERT_LIVE"
    echo "   sudo rm -rf $CERT_ARCHIVE"
    echo "   sudo rm -f $CERT_RENEWAL"
fi

# Удаление сервиса из docker-compose.yml
echo ""
echo "Удаление сервиса из docker-compose.yml..."

if ! grep -q "  ${SERVICE_NAME}:" docker-compose.yml; then
    echo "⚠️  Сервис $SERVICE_NAME не найден в docker-compose.yml"
else
    # Создаем резервную копию docker-compose.yml
    cp docker-compose.yml docker-compose.yml.bak.$(date +%Y%m%d_%H%M%S)
    echo "✅ Создана резервная копия docker-compose.yml"
    
    # Удаляем секцию сервиса из docker-compose.yml
    # Используем awk для удаления блока сервиса (от начала до следующего сервиса или networks:)
    awk -v service="${SERVICE_NAME}" '
        BEGIN { in_service=0; indent_level=0 }
        /^  [a-zA-Z0-9_-]+:/ { 
            if ($1 == "  " service ":") { 
                in_service=1
                next
            } else if (in_service) {
                # Встретили следующий сервис - выходим из режима удаления
                in_service=0
            }
        }
        in_service && /^networks:/ { 
            # Дошли до секции networks - выходим из режима удаления
            in_service=0
        }
        !in_service { print }
    ' docker-compose.yml > docker-compose.yml.tmp && mv docker-compose.yml.tmp docker-compose.yml
    
    echo "✅ Сервис $SERVICE_NAME удален из docker-compose.yml"
    
    # Удаляем зависимость из depends_on nginx (если есть)
    if grep -q "depends_on:" docker-compose.yml && grep -A 10 "nginx:" docker-compose.yml | grep -q "depends_on:"; then
        # Удаляем строку с зависимостью от сервиса
        awk -v service="${SERVICE_NAME}" '
            /nginx:/ { in_nginx=1 }
            in_nginx && /depends_on:/ { in_depends=1; print; next }
            in_depends && /      - / {
                if ($0 ~ "      - " service "$") {
                    next  # Пропускаем строку с этим сервисом
                }
            }
            in_depends && /^    [a-zA-Z]/ && !/depends_on/ { in_depends=0 }
            { print }
        ' docker-compose.yml > docker-compose.yml.tmp && mv docker-compose.yml.tmp docker-compose.yml
        
        echo "✅ Зависимость $SERVICE_NAME удалена из depends_on nginx"
    fi
fi

echo ""
echo "=========================================="
echo "✅ Готово! Сайт $SERVICE_NAME ($DOMAIN) удален"
echo "=========================================="
if [ "$NGINX_REMOVED" -eq 1 ]; then
    echo ""
    echo "Резервная копия nginx конфигурации: $BACKUP_FILE"
fi
echo ""
echo "Для применения изменений выполните:"
echo "  docker compose up -d --build"
if [ "$NGINX_REMOVED" -eq 1 ]; then
    echo "  docker compose restart nginx"
fi

