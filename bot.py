import os

from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")


telegram_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"سلام {user.first_name} 👋\n\n"
        "به Investment Up خوش آمدید.\n\n"
        "⚠️ این نسخه آزمایشی است و موجودی‌ها و سودها "
        "صرفاً شبیه‌سازی هستند."
    )


telegram_app.add_handler(CommandHandler("start", start))

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "ok", "bot": "online"}


@app.post("/telegram")
async def telegram_webhook(update_data: dict):
    update = Update.de_json(update_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
