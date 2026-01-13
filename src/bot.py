# bot.py
import os
import sys
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F

# Добавляем путь к src для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.yandexgpt_marketer import YandexGPTMarketerDetailedCoT
    from src.universal_logger import universal_logger  # Импортируем универсальный логгер
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Текущая рабочая директория:", os.getcwd())
    print("Содержимое src/:", os.listdir('src') if os.path.exists('src') else "Папка src не существует")
    raise

# Загружаем .env
load_dotenv()

# Получаем токены - используем имена переменных ИЗ ВАШЕГО .env ФАЙЛА
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Было BOT_TOKEN, теперь TELEGRAM_BOT_TOKEN
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")    # Было FOLDER_ID, теперь YANDEX_FOLDER_ID

# Отладочная информация
print(f"DEBUG: TELEGRAM_BOT_TOKEN = {'***установлен***' if BOT_TOKEN else 'ОТСУТСТВУЕТ'}")
print(f"DEBUG: YANDEX_API_KEY = {'***установлен***' if YANDEX_API_KEY else 'ОТСУТСТВУЕТ'}")
print(f"DEBUG: YANDEX_FOLDER_ID = {'***установлен***' if FOLDER_ID else 'ОТСУТСТВУЕТ'}")

if not all([BOT_TOKEN, YANDEX_API_KEY, FOLDER_ID]):
    print("❌ Отсутствуют переменные окружения в .env")
    universal_logger.log("ERROR", "system", 0, "Отсутствуют переменные окружения в .env")
    raise ValueError("❌ Отсутствуют переменные окружения в .env")

# Инициализация
bot = Bot(token=BOT_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)
marketer = YandexGPTMarketerDetailedCoT(YANDEX_API_KEY, FOLDER_ID)

# Логируем запуск бота
print("✅ Бот инициализирован")
universal_logger.log("INFO", "system", 0, "🚀 Бот запущен!")

@router.message(F.text)
async def handle_message(message: Message):
    """Обработка входящих сообщений."""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "anonymous"
    user_text = message.text.strip()

    # Логируем полученное сообщение
    universal_logger.log("INFO", username, user_id, f"Получено сообщение от пользователя: {user_text}")

    try:
        # Отправляем "печатает..."
        await message.bot.send_chat_action(chat_id=user_id, action="typing")

        # Генерируем ответ через YandexGPT
        response = marketer.generate_product_card(user_text)

        # Отправляем ответ пользователю
        await message.answer(response)

        # Логируем успешную генерацию
        universal_logger.log("INFO", username, user_id, f"Карточка товара успешно создана, длина ответа: {len(response)} символов")

    except Exception as e:
        # Логируем ошибку
        error_msg = str(e)
        universal_logger.log("ERROR", username, user_id, "Ошибка при генерации карточки товара", error_msg)
        
        # Отправляем сообщение об ошибке пользователю
        await message.answer("❌ Произошла ошибка при обработке вашего запроса. Попробуйте позже.")

async def main():
    """Основная функция запуска бота."""
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        universal_logger.log("INFO", "system", 0, "Бот остановлен пользователем")
        universal_logger.close()
    except Exception as e:
        universal_logger.log("ERROR", "system", 0, "Критическая ошибка при работе бота", str(e))
        universal_logger.close()
