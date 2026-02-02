import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://influenceai-minibot.onrender.com/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ====== START HANDLER ======
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    # TEXT 1
    await message.answer(
        "Текст 1\n\n"
        "Це приклад стартового тексту.\n"
        "Тут ти вставляєш свій контент."
    )

    # IMAGE 2
    await message.answer_photo(
        photo="https://placehold.co/600x400",
        caption="Картинка 2\n\nОпис картинки"
    )

    # VIDEO 3
    await message.answer_video(
        video="https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
        caption="Відео 3\n\nОпис відео"
    )

    # LINKS 4
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Telegram канал", url="https://t.me/telegram")],
            [InlineKeyboardButton(text="Сайт", url="https://google.com")]
        ]
    )

    await message.answer(
        "Посилання 4\n\nОбери потрібне:",
        reply_markup=keyboard
    )

# ====== WEBHOOK ======
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def handle_webhook(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()

def main():
    logging.basicConfig(level=logging.INFO)

    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    main()


