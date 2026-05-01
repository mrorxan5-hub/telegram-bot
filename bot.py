import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam 👋 Bot aktivdir!\n\nKomandalar:\n/add username\n/list\n/remove username"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        username = " ".join(context.args)
        users.append(username)
        await update.message.reply_text(f"{username} əlavə olundu ✅")
    else:
        await update.message.reply_text("Username yaz!")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if users:
        await update.message.reply_text("\n".join(users))
    else:
        await update.message.reply_text("Siyahı boşdur")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        username = " ".join(context.args)
        if username in users:
            users.remove(username)
            await update.message.reply_text(f"{username} silindi ❌")
        else:
            await update.message.reply_text("Tapılmadı")
    else:
        await update.message.reply_text("Username yaz!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_users))
app.add_handler(CommandHandler("remove", remove))

updater.start_polling()
    updater.idle()

if _name_ == "_main_":
    main()
