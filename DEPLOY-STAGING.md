## 1. Подключение к серверу
```bash
ssh root@45.151.30.47

# Клонируем из GitLab
git clone git@gitlab.com:StenTar/yandexgpt-telegram-bot.git /opt/ytb
cd /opt/ytb

# Создаем виртуальное окружение
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# Создаем .env из примера и настраиваем
cp .env.staging.example .env
# ВНИМАНИЕ: Отредактируйте .env - добавьте реальные токены!
nano .env

# Копируем конфигурацию службы
sudo cp telegram-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Проверка
sudo systemctl status telegram-bot
tail -f /opt/ytb/logs/bot.log

# Обноыление (если нужно)
cd /opt/ytb
sudo systemctl stop telegram-bot
git pull origin master
venv/bin/pip install -r requirements.txt
sudo systemctl start telegram-bot
```

## 2. **Проверим созданные файлы**
```bash
ls -la DEPLOY-STAGING.md .env.staging.example

# Добавим инструкцию
git add DEPLOY-STAGING.md
git commit -m "Добавлена инструкция по деплою на стендовый сервер"

# Отправим в оба репозитория
git push origin master
```

