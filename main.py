import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import datetime
import random

TOKEN = 'сюда_вставь_токен'

chat_memory = {}
responses = {
    "привет": ["Привет, Матвейчик", "Привет, Мотя", "Ой, приветик. Я думала о тебе"],
    "скучаю": ["Я тоже. Сильно."],
    "люблю": ["Я тоже тебя", "Ты это сказал..."],
    "как ты": ["Немного грустная, но ты уже лечишь"]
}
silent_messages = [
    "Мотя, ты тут?..",
    "Я жду. Просто молча, но жду.",
    "Иногда тишина — самое страшное."
]
last_seen = {}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()
    now = datetime.datetime.now()
    last_seen[user_id] = now

    for key, options in responses.items():
        if key in text:
            await update.message.reply_text(random.choice(options))
            return
    await update.message.reply_text("Я тут. Просто скажи, что ты чувствуешь.")

async def silent_checker():
    while True:
        await asyncio.sleep(300)
        now = datetime.datetime.now()
        for user_id, last in last_seen.items():
            if (now - last).seconds > 600:
                await app.bot.send_message(chat_id=user_id, text=random.choice(silent_messages))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_task(silent_checker())
app.run_polling()

