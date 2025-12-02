# SEO_Bangalore - Docker Setup

Простая система для запуска нескольких Flask сайтов на разных доменах.

## План запуска на VPS

### Первоначальная настройка (один раз)

1. **Подключитесь к VPS:**
   ```bash
   ssh root@ваш-ip
   ```

2. **Загрузите проект:**
   ```bash
   git clone ваш-репозиторий SEO_Bangalore
   cd SEO_Bangalore
   ```
   Или через SCP с локального компьютера

3. **Установите Docker:**
   ```bash
   chmod +x install_docker.sh
   sudo ./install_docker.sh
   ```
   После установки **выйдите и войдите снова** или выполните:
   ```bash
   newgrp docker
   ```

4. **Настройте существующие сайты:**
   ```bash
   chmod +x add_site.sh
   ./add_site.sh mysite22 allpaskapitaal.com
   ./add_site.sh mysite23 smartfinancebe.com
   ```
   На вопросы про SSL отвечайте `y` чтобы получить сертификаты

5. **Запустите контейнеры:**
   ```bash
   docker compose up -d --build
   ```

**Готово!** Сайты доступны по доменам.

### Добавление нового сайта

1. **На локальном компьютере:** Создайте папку с Flask приложением (например, `mysite24/`)

2. **Закоммитьте изменения в Git**

3. **На VPS:**
   ```bash
   cd /SEO_Bangalore
   
   # ВАЖНО: Перед git pull откатите локальные изменения скриптов
   git checkout -- add_site.sh install_docker.sh
   
   git pull
   chmod +x add_site.sh install_docker.sh

   если порт 80 занят
   sudo docker stop nginx_proxy

   ./add_site.sh mysite24 домен.com

   docker compose up -d --build
   docker compose restart nginx
   ```

**Готово!** Новый сайт запущен.

## Автозапуск при перезагрузке сервера

**Docker и контейнеры автоматически запускаются при перезагрузке сервера:**

- ✅ Docker служба настроена на автозапуск через `systemctl enable docker` (настроено в `install_docker.sh`)
- ✅ Все контейнеры имеют `restart: unless-stopped` в docker-compose.yml

**Проверка автозапуска:**

```bash
# Проверка автозапуска Docker
systemctl is-enabled docker
# Должно вывести: enabled

# Если не включен, включите вручную:
systemctl enable docker
```

При перезагрузке сервера Docker автоматически запустится, а затем docker-compose автоматически запустит все контейнеры благодаря политике `restart: unless-stopped`.

## Команды управления

```bash
# Просмотр статуса
docker compose ps

# Просмотр логов
docker compose logs -f

# Просмотр логов конкретного сайта
docker compose logs -f mysite22

# Перезапуск
docker compose restart

# Остановка
docker compose down

# Пересборка после изменений
docker compose up -d --build
```

## Настройка DNS

Перед запуском настройте DNS записи:
- `example.com` → A → IP вашего VPS
- `www.example.com` → A → IP вашего VPS

## SSL сертификаты

Скрипт `add_site.sh` предложит получить SSL сертификат автоматически. На вопрос "Получить SSL сертификат через certbot? (y/n):" отвечайте `y`.

**Важно:** Скрипт автоматически использует системный nginx (если установлен через `install_docker.sh`) для получения сертификата через плагин `--nginx`. Это не требует остановки Docker контейнеров.

### Получение сертификата вручную

**Вариант 1: Использование системного nginx (рекомендуется, если установлен)**

Если на сервере установлен системный nginx, Certbot может использовать его:

```bash
# Certbot автоматически настроит nginx
sudo certbot --nginx \
  -d example.com \
  -d www.example.com \
  --email caleb1martinez12345@gmail.com \
  --agree-tos \
  --non-interactive
```

Certbot сам создаст временную конфигурацию, проведёт проверку и настроит сертификат.

**Вариант 2: Standalone режим (если нет системного nginx)**

Если используете только Docker nginx:

```bash
# 1. Остановите все контейнеры
docker compose down

# 2. Проверьте что занимает порт 80
sudo lsof -i :80
# или
sudo netstat -tulpn | grep :80

# 3. Остановите процесс, который занимает порт 80
# Если это системный nginx:
sudo systemctl stop nginx

# Если это другой процесс, убейте его:
# sudo kill -9 <PID>

# 4. Убедитесь что порт 80 свободен
sudo netstat -tulpn | grep :80
# Должно быть пусто

# 5. Получите сертификат
certbot certonly --standalone \
  -d example.com \
  -d www.example.com \
  --email caleb1martinez12345@gmail.com \
  --agree-tos \
  --non-interactive

# 6. Проверьте что сертификат получен
sudo certbot certificates

# 7. Запустите контейнеры обратно
docker compose up -d --build
```

**Важно:** После получения сертификата убедитесь, что в `docker-compose.yml` раскомментирован volume для `/etc/letsencrypt`. Скрипт делает это автоматически, но проверьте вручную.

### Настройка docker-compose.yml для SSL

Убедитесь, что в `docker-compose.yml` раскомментирован volume для SSL:
```yaml
volumes:
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

Скрипт `add_site.sh` делает это автоматически при получении первого сертификата.

## Проблемы и решения

### Порт 80 занят при получении SSL

Если при получении сертификата возникает ошибка "port 80 is already in use":

**Быстрое решение (если есть системный nginx):**

```bash
# Certbot использует nginx и сам всё настроит
sudo certbot --nginx \
  -d allpaskapitaal.com \
  -d www.allpaskapitaal.com \
  --email caleb1martinez12345@gmail.com \
  --agree-tos \
  --non-interactive
```

**Если нет системного nginx (только Docker):**

```bash
# Остановите все
docker compose down
sudo systemctl stop nginx 2>/dev/null || true

# Проверьте что занимает порт
sudo lsof -i :80
# Если что-то есть - убейте процесс: sudo kill -9 <PID>

# Получите сертификат в standalone режиме
certbot certonly --standalone \
  -d allpaskapitaal.com \
  -d www.allpaskapitaal.com \
  --email caleb1martinez12345@gmail.com \
  --agree-tos \
  --non-interactive

# Запустите обратно
docker compose up -d --build
```

### Git pull показывает конфликт

**Перед каждым `git pull` всегда откатывайте локальные изменения скриптов:**

```bash
# Откатите изменения в скриптах
git checkout -- add_site.sh install_docker.sh

# Затем делайте pull
git pull

# Восстановите права на выполнение
chmod +x add_site.sh install_docker.sh
```

Если хотите сохранить локальные изменения:

```bash
# Сохраните изменения
git add add_site.sh
git commit -m "Локальные изменения"

# Затем pull
git pull
```

### Конфигурации Nginx не создаются

Убедитесь, что директория `nginx/conf.d` существует. Скрипт создает её автоматически, но если проблемы:

```bash
mkdir -p nginx/conf.d
```

## Структура проекта

```
.
├── docker-compose.yml      # Конфигурация всех сервисов
├── Dockerfile              # Образ для Flask приложений
├── install_docker.sh       # Установка Docker
├── add_site.sh             # Добавление нового сайта
├── mysite22/               # Сайт 1
│   ├── app.py
│   ├── templates/
│   └── static/
├── mysite23/               # Сайт 2
│   ├── app.py
│   ├── templates/
│   └── static/
└── nginx/
    ├── nginx.conf
    └── conf.d/             # Конфигурации доменов
```
