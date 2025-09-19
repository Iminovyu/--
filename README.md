# 5-bit Telegram Bot

Кодирует / раскодирует английский текст (A-Z, пробел) в 5-бит двоичную строку прямо в Telegram.

## Deploy on Render (quick)

1. Fork / upload this repo to GitHub  
2. [Render.com](https://render.com) → New **Web Service** → connect repo  
3. **Environment Variables** (Dashboard):
   - `BOT_TOKEN` = токен от [@BotFather](https://t.me/BotFather)  
   - `WEBHOOK_URL` = `https://your-service-name.onrender.com/webhook`  
4. Leave rest defaults (Python, pip install via requirements.txt) → Deploy  
5. В BotFather → `/setwebhook` → вставь ту же `WEBHOOK_URL`  
6. Готово – бот отвечает мгновенно.