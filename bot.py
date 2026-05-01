import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8307363974:AAGtaAf1v4hyPso0ejFf8bFumDOTHi2hHrE"

users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam 👋 Bot aktivdir!")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = " ".join(context.args)
    if username:
        users.append(username)
        await update.message.reply_text(f"{username} əlavə olundu ✅")
    else:
        await update.message.reply_text("Username yazmadın ❌")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if users:
        await update.message.reply_text("\n".join(users))
    else:
        await update.message.reply_text("List boşdur")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = " ".join(context.args)
    if username in users:
        users.remove(username)
        await update.message.reply_text(f"{username} silindi ❌")
    else:
        await update.message.reply_text("Tapılmadı")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_users))
    app.add_handler(CommandHandler("remove", remove))

    app.run_polling()

if __name__ == "__main__":
    main()
