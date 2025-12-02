#!/bin/bash
# Скрипт для исправления устаревшего синтаксиса http2 в конфигурациях nginx
# Использование: ./fix_nginx_http2.sh

set -e

echo "=========================================="
echo "Исправление конфигураций nginx"
echo "=========================================="

FIXED=0

# Проверка и исправление локальных файлов
if [ -d "nginx/conf.d" ]; then
    for conf_file in nginx/conf.d/*.conf; do
        if [ -f "$conf_file" ]; then
            # Проверяем, есть ли устаревший синтаксис
            if grep -q "listen 443 ssl http2;" "$conf_file"; then
                echo "Исправление локального файла: $conf_file"
                # Создаем резервную копию
                cp "$conf_file" "${conf_file}.bak"
                # Заменяем устаревший синтаксис (для Linux/Mac)
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    # macOS
                    sed -i '' 's/listen 443 ssl http2;/listen 443 ssl;\
    http2 on;/' "$conf_file"
                else
                    # Linux
                    sed -i 's/listen 443 ssl http2;/listen 443 ssl;\n    http2 on;/' "$conf_file"
                fi
                FIXED=$((FIXED + 1))
                echo "✅ Исправлено: $conf_file"
            fi
        fi
    done
fi

# Исправление файлов внутри контейнера (если контейнер запущен)
if docker ps | grep -q nginx_proxy; then
    echo "Проверка файлов внутри контейнера..."
    CONTAINER_FILES=$(docker exec nginx_proxy sh -c "ls /etc/nginx/conf.d/*.conf 2>/dev/null || echo ''" | tr '\n' ' ')
    
    for conf_file in $CONTAINER_FILES; do
        if [ -n "$conf_file" ]; then
            # Проверяем, есть ли устаревший синтаксис
            if docker exec nginx_proxy grep -q "listen 443 ssl http2;" "$conf_file" 2>/dev/null; then
                echo "Исправление файла в контейнере: $conf_file"
                # Создаем резервную копию в контейнере
                docker exec nginx_proxy sh -c "cp $conf_file ${conf_file}.bak"
                # Исправляем файл
                docker exec nginx_proxy sh -c "sed -i 's/listen 443 ssl http2;/listen 443 ssl;\\n    http2 on;/' $conf_file"
                FIXED=$((FIXED + 1))
                echo "✅ Исправлено в контейнере: $conf_file"
            fi
        fi
    done
fi

if [ $FIXED -eq 0 ]; then
    echo "✅ Все конфигурации уже исправлены или не найдены файлы для исправления"
else
    echo "=========================================="
    echo "✅ Исправлено файлов: $FIXED"
    echo "=========================================="
    echo "Перезапустите nginx контейнер:"
    echo "docker compose restart nginx"
fi

