import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


LINK-ACCESSO= "LINK_ACCESSO"

# === Funzioni principali ===

def estrai_info(cf: str):
    try:
        anno = int(cf[6:8])
        mese = cf[8].upper()
        giorno = int(cf[9:11])

        # Calcolo anno completo
        anno_corrente = datetime.now().year
        anno += 1900 if anno > anno_corrente % 100 else 2000

        # Sesso
        sesso = "F" if giorno > 40 else "M"

        return anno, sesso
    except:
        return None, None



# === Bot Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Inviami il tuo codice fiscale per verificare se hai diritto all'accesso.")

async def verifica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cf = update.message.text.strip().upper()
    user_id = update.effective_user.id

    if len(cf) != 16:
        await update.message.reply_text("❌ Codice fiscale non valido.")
        return

    anno, sesso = estrai_info(cf)
    if not anno:
        await update.message.reply_text("⚠️ Impossibile estrarre i dati.")
        return

    eta = datetime.now().year - anno
    if eta <= 18:
        
        await update.message.reply_text(f"✅ Hai {eta} anni ({sesso}). Accesso consentito:\n"{LINK-ACCESSO}")
    else:
        await update.message.reply_text(f"🚫 Hai {eta} anni. Non hai diritto all'accesso.")

# === Setup bot ===

app = ApplicationBuilder().token("TOKEN_BOT").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verifica))
app.run_polling()
