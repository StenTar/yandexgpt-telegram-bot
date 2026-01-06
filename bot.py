# bot.py
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
from yandexgpt_marketer import YandexGPTMarketerDetailedCoT

# Загружаем .env
load_dotenv()

# Получаем токены
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

if not all([BOT_TOKEN, YANDEX_API_KEY, YANDEX_FOLDER_ID]):
    raise ValueError("❌ Отсутствуют переменные окружения в .env")

# Инициализация
bot = Bot(token=BOT_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)
marketer = YandexGPTMarketerDetailedCoT(YANDEX_API_KEY, YANDEX_FOLDER_ID)

@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! 📦 Опишите товар — и я создам карточку для маркетплейса.")

@router.message(F.text)
async def handle_message(message: Message):
    user_text = message.text.strip()
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"

    if not user_text:
        print(f"📩 [{username} ({user_id})]: Пустое сообщение")
        await message.answer("⚠️ Пожалуйста, опишите товар текстом.")
        return

    print(f"📩 [{username} ({user_id})]: {user_text}")
    await message.answer("⏳ Анализирую и создаю карточку...")

    try:
        response = marketer.create_product_card(user_text)
        print(f"✅ Ответ для {username} ({user_id}) готов (длина: {len(response)} символов)")
        await message.answer(response)
    except Exception as e:
        error_msg = f"❌ Ошибка при обработке запроса от {username} ({user_id}): {str(e)}"
        print(error_msg)
        await message.answer("⚠️ Произошла ошибка при генерации карточки. Попробуйте позже.")

async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
