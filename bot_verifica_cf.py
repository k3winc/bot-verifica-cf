from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# === Recupero variabili d'ambiente ===
TOKEN = os.getenv("BOT_TOKEN")
LINK_ACCESSO = os.getenv("LINK_ACCESSO")

if not TOKEN:
    raise ValueError("❌ Variabile BOT_TOKEN mancante.")
if not LINK_ACCESSO:
    raise ValueError("❌ Variabile LINK_ACCESSO mancante.")

# === Funzioni principali ===

def estrai_info(cf: str):
    try:
        anno = int(cf[6:8])
        giorno = int(cf[9:11])
        anno_corrente = datetime.now().year
        anno += 1900 if anno > anno_corrente % 100 else 2000
        sesso = "F" if giorno > 40 else "M"
        return anno, sesso
    except:
        return None, None

# === Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Inviami il tuo codice fiscale per verificare l'accesso.")

async def verifica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cf = update.message.text.strip().upper()

    if len(cf) != 16:
        await update.message.reply_text("❌ Codice fiscale non valido.")
        return

    anno, sesso = estrai_info(cf)
    if not anno:
        await update.message.reply_text("⚠️ Errore nell'elaborazione del codice.")
        return

    eta = datetime.now().year - anno
    if eta <= 18:
        await update.message.reply_text(f"✅ Hai {eta} anni ({sesso}). Accesso consentito:\n{LINK_ACCESSO}")
    else:
        await update.message.reply_text(f"🚫 Hai {eta} anni. Non hai diritto all'accesso.")

# === Avvio bot ===

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verifica))
app.run_polling()
