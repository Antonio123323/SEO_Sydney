#!/bin/bash
# Скрипт для поиска и исправления проблемных конфигураций nginx с неправильными путями к сертификатам
# Использование: ./fix_nginx_certs.sh

set -e

echo "=========================================="
echo "Поиск проблемных конфигураций nginx"
echo "=========================================="

FIXED=0
PROBLEMS=0

# Проверяем все конфигурации nginx
if [ ! -d "nginx/conf.d" ]; then
    echo "❌ Директория nginx/conf.d не найдена"
    exit 1
fi

for conf_file in nginx/conf.d/*.conf; do
    if [ ! -f "$conf_file" ]; then
        continue
    fi
    
    # Ищем проблемные пути к сертификатам (с символами #, пробелами и т.д.)
    if grep -q "ssl_certificate.*#" "$conf_file" 2>/dev/null || \
       grep -q "ssl_certificate.*[[:space:]]" "$conf_file" 2>/dev/null; then
        
        PROBLEMS=$((PROBLEMS + 1))
        echo ""
        echo "⚠️  Найдена проблемная конфигурация: $conf_file"
        
        # Показываем проблемные строки
        echo "Проблемные строки:"
        grep -n "ssl_certificate" "$conf_file" | grep -E "[#[:space:]]" || true
        
        # Пытаемся извлечь домен из конфигурации
        DOMAIN=$(grep -oP "server_name\s+\K[^\s;]+" "$conf_file" | head -1 | sed 's/www\.//')
        
        if [ -n "$DOMAIN" ]; then
            echo "Извлеченный домен: $DOMAIN"
            
            # Создаем резервную копию
            BACKUP_FILE="${conf_file}.bak.$(date +%Y%m%d_%H%M%S)"
            cp "$conf_file" "$BACKUP_FILE"
            echo "✅ Создана резервная копия: $BACKUP_FILE"
            
            # Исправляем пути к сертификатам
            sed -i "s|/etc/letsencrypt/live/[^/]*#/|/etc/letsencrypt/live/${DOMAIN}/|g" "$conf_file"
            sed -i "s|/etc/letsencrypt/live/[^/]* /|/etc/letsencrypt/live/${DOMAIN}/|g" "$conf_file"
            sed -i "s|ssl_certificate.*cryptohorizon-ae.com#|ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem|g" "$conf_file"
            sed -i "s|ssl_certificate_key.*cryptohorizon-ae.com#|ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem|g" "$conf_file"
            
            echo "✅ Исправлен файл: $conf_file"
            FIXED=$((FIXED + 1))
        else
            echo "❌ Не удалось извлечь домен из конфигурации"
            echo "   Рекомендуется удалить или исправить файл вручную"
        fi
    fi
done

if [ $PROBLEMS -eq 0 ]; then
    echo ""
    echo "✅ Проблемных конфигураций не найдено"
else
    echo ""
    echo "=========================================="
    echo "Найдено проблем: $PROBLEMS"
    echo "Исправлено: $FIXED"
    echo "=========================================="
    
    # Проверяем синтаксис nginx (если контейнер запущен)
    if docker ps | grep -q nginx_proxy; then
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
        fi
    fi
fi

