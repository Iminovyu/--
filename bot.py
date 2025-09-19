#!/usr/bin/env python3
import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

BOT_TOKEN   = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]        # полный URL вида https://mybot.onrender.com/webhook
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 10000))      # Render ставит порт в переменную PORT

TABLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
REV   = {ch: i for i, ch in enumerate(TABLE)}

def encode(text: str) -> str:
    text = text.upper()
    if not all(ch in REV for ch in text):
        return None
    return "".join(f"{REV[ch]:05b}" for ch in text)

def decode(bits: str) -> str | None:
    if not bits or len(bits) % 5 or any(ch not in "01" for ch in bits):
        return None
    return "".join(TABLE[int(bits[i:i+5], 2)] for i in range(0, len(bits), 5))

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp  = Dispatcher()

@dp.message(CommandStart())
async def start(msg: types.Message):
    await msg.answer(
        "Привет! Пришли:\n"
        "• текст из A–Z и пробелов – получишь 5-битный двоичный код;\n"
        "• двоичную строку (0/1, длина кратна 5) – расшифрую обратно."
    )

@dp.message(F.text)
async def main_handler(msg: types.Message):
    txt = msg.text.strip()
    if all(ch in "01" for ch in txt) and len(txt) % 5 == 0:
        dec = decode(txt)
        await msg.answer(f"Расшифровка: <b>{dec}</b>" if dec else "Неверная двоичная строка.")
        return
    enc = encode(txt)
    await msg.answer(f"Код: <code>{enc}</code>" if enc else "Можно только A–Z и пробелы.")

async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)

def create_app() -> web.Application:
    app = web.Application()
    setup_application(app, dp, bot=bot)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.router.add_get("/", lambda req: web.Response(text="5-bit TG bot OK"))
    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(create_app(), host="0.0.0.0", port=PORT)