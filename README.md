# YandexGPT Telegram Bot

Telegram бот для автоматического создания SEO-карточек товаров через YandexGPT API.

## 🚀 Установка

```bash
# Клонирование
git clone git@github.com:StenTar/yandexgpt-telegram-bot.git /opt/ytb
cd /opt/ytb

# Настройка окружения
python3 -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env
# Отредактируйте .env с вашими ключами

# Systemd служба
sudo cp telegram-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-bot
📁 Структура проекта
text
/opt/ytb/
├── src/                    # Исходный код
│   ├── __init__.py
│   ├── bot.py
│   └── yandexgpt_marketer.py
├── logs/                  # Логи приложения
├── .env.example          # Шаблон конфигурации
├── requirements.txt      # Зависимости Python
├── telegram-bot.service # Конфиг systemd
├── README.md            # Эта документация
└── MAINTENANCE.md       # Инструкции по обслуживанию
🔧 Технологии
Python 3.12 + aiogram 3.x

YandexGPT API

Systemd для управления процессами

Виртуальное окружение для изоляции зависимостей

📊 Мониторинг
bash
# Статус службы
sudo systemctl status telegram-bot

# Логи в реальном времени
tail -f /opt/ytb/logs/bot.log

# Systemd логи
sudo journalctl -u telegram-bot -f
📝 Лицензия
MIT
