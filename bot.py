import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler


TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")

if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL is not configured")


telegram_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context):
    user = update.effective_user

    await update.message.reply_text(
        f"سلام {user.first_name} 👋\n\n"
        "به Investment Up خوش آمدید.\n\n"
        "⚠️ این نسخه آزمایشی است.\n"
        "موجودی و سودهای نمایش‌داده‌شده صرفاً شبیه‌سازی هستند."
    )


telegram_app.add_handler(CommandHandler("start", start))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await telegram_app.initialize()
    await telegram_app.start()

    await telegram_app.bot.set_webhook(
        url=f"{WEBHOOK_URL}/telegram"
    )

    yield

    await telegram_app.bot.delete_webhook()
    await telegram_app.stop()
    await telegram_app.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home():
    return {"status": "online"}


@app.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    update = Update.de_json(
        data,
        telegram_app.bot
    )

    await telegram_app.process_update(update)

    return {"ok": True}
