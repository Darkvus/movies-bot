# bot_plex.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from search import search_mejortorrent
from qbittorrent import enviar_a_qbittorrent

# Configura tu token aquí
TELEGRAM_BOT_TOKEN = "7973004910:AAGJWuC9KrSNAJ0G_O1xOUWvZJp--jS6_pg"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Envíame el título de una película con /descargar y la descargaré para ti.")

# Comando /descargar
async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Debes escribir el nombre de la película: /descargar <nombre>")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Buscando '{query}' en MejorTorrent...")

    torrent_url = search_mejortorrent(query)
    if not torrent_url:
        await update.message.reply_text("❌ No encontré la película.")
        return

    await update.message.reply_text("🎬 Enviando a qBittorrent...")
    success = enviar_a_qbittorrent(torrent_url)

    if success:
        await update.message.reply_text("✅ ¡Película en descarga! Aparecerá en Plex en unos minutos.")
    else:
        await update.message.reply_text("⚠️ Hubo un problema al añadir el torrent.")

# Iniciar el bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("descargar", descargar))

    app.run_polling()
