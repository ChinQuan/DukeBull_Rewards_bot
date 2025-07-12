import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Dummy winner list – to będzie uzupełniane przez lottery.py
WINNERS = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Witaj w loterii $BuLL!\n\n"
        "🎁 Każdy, kto kupi token $BuLL bierze udział w codziennej loterii.\n"
        "🕒 Losowanie codziennie o 21:00 UTC!\n"
        "💰 Nagroda: 10 000 $BuLL\n\n"
        "Sprawdź: /stats /winners"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Obecnie aktywnych graczy: funkcja w trakcie wdrażania 🔧")

async def winners(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if WINNERS:
        reply = "🏆 Ostatni zwycięzcy:\n"
        for date, addr in WINNERS[-5:][::-1]:
            reply += f"📅 {date} → {addr}\n"
    else:
        reply = "Brak jeszcze zwycięzców. Bądź pierwszy!"
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("winners", winners))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
# Placeholder – will be filled with functional bot logic
