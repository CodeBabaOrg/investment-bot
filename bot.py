import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"سلام {user.first_name} 👋\n"
        "به Investment Up خوش آمدید.\n\n"
        "برای شروع روی گزینه‌های ربات استفاده کنید."
    )


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
