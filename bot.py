# bot.py  – DukeBull Rewards Bot
# ---------------------------------------------
# zgodny z python-telegram-bot 20.x (API asyncio)

import logging
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ──────────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# lista zwycięzców będzie uzupełniana przez lottery.py
WINNERS: list[tuple[str, str]] = []  # (data, adres)


# ──────────  handlers  ──────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Przywitanie i instrukcja."""
    msg = (
        "👋 Witaj w loterii **$BuLL**!\n\n"
        "🎁 Każdy, kto *kupi* token $BuLL bierze udział w codziennym losowaniu.\n"
        "🕒 **Losowanie**: codziennie o 21:00 UTC\n"
        "💰 **Nagroda**: 10 000 $BuLL\n\n"
        "Sprawdź /staty lub /winners, by zobaczyć poprzednich zwycięzców."
    )
    await update.message.reply_markdown(msg)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ile adresów bierze udział (placeholder – uzupełni watcher)."""
    # docelowo watcher będzie zapisywał liczbę graczy do pliku/bazy
    players = context.bot_data.get("players_count", 0)
    await update.message.reply_text(f"📊 Obecnie w grze: {players} adresów.")


async def winners(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista ostatnich zwycięzców."""
    if not WINNERS:
        await update.message.reply_text("Brak zwycięzców – pierwsze losowanie dziś o 21:00 UTC!")
        return

    lines = [f"🏆 **Ostatni zwycięzcy:**"]
    for date, addr in WINNERS[-5:][::-1]:
        lines.append(f"• {date} → `{addr[:4]}...{addr[-4:]}`")
    await update.message.reply_markdown("\n".join(lines))


# ──────────  main  ──────────
def main() -> None:
    logging.basicConfig(
        format="%(asctime)s  %(levelname)s  %(name)s  %(message)s",
        level=logging.INFO,
    )

    application: Application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("winners", winners))

    logging.info("🤖 DukeBull bot uruchomiony – czekam na komendy")
    application.run_polling(stop_signals=None)  # Render sam restartuje przy potrzebie


# punkt wejścia
if __name__ == "__main__":
    main()
