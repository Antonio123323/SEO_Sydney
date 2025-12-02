#!/bin/bash
# Скрипт установки Docker и Docker Compose на Linux
# Использование: sudo ./install_docker.sh

set -e

echo "=========================================="
echo "Установка Docker и Docker Compose"
echo "=========================================="

# Обновление системы
echo "Обновление системы..."
apt update
apt upgrade -y

# Установка необходимых пакетов
echo "Установка зависимостей..."
apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Проверка Docker
if command -v docker &> /dev/null; then
    echo "Docker уже установлен"
    docker --version
else
    echo "Установка Docker..."
    # Добавление репозитория Docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io
fi

# Проверка Docker Compose
if command -v docker compose &> /dev/null || command -v docker-compose &> /dev/null; then
    echo "Docker Compose уже установлен"
    docker compose version 2>/dev/null || docker-compose --version
else
    echo "Установка Docker Compose..."
    apt install -y docker-compose-plugin
fi

# Добавление пользователя в группу docker
if [ -n "$SUDO_USER" ]; then
    echo "Добавление пользователя $SUDO_USER в группу docker..."
    usermod -aG docker $SUDO_USER
fi

# Настройка Firewall
echo "Настройка Firewall..."
apt install -y ufw
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Включение автозапуска Docker
systemctl enable docker
systemctl start docker

# Установка системного nginx (для использования certbot --nginx)
echo "Установка системного nginx..."
apt install -y nginx

# Остановка системного nginx (будет использоваться только для certbot)
systemctl stop nginx
systemctl disable nginx

echo ""
echo "=========================================="
echo "Установка завершена!"
echo "=========================================="
echo ""
echo "Установлено:"
echo "  - Docker и Docker Compose"
echo "  - Системный nginx (для использования с certbot --nginx)"
echo ""
echo "ВАЖНО: Выйдите и войдите снова, чтобы изменения группы docker вступили в силу"
echo "Или выполните: newgrp docker"
echo ""

