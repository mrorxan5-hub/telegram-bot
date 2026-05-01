import os
from telegram.ext import Updater, CommandHandler

TOKEN = os.getenv("TOKEN")

users = []

def start(update, context):
    update.message.reply_text("Salam 👋 Bot aktivdir!")

def add(update, context):
    username = " ".join(context.args)
    if username:
        users.append(username)
        update.message.reply_text(f"{username} əlavə olundu ✅")
    else:
        update.message.reply_text("Username yazmadın ❌")

def list_users(update, context):
    if users:
        update.message.reply_text("\n".join(users))
    else:
        update.message.reply_text("List boşdur")

def remove(update, context):
    username = " ".join(context.args)
    if username in users:
        users.remove(username)
        update.message.reply_text(f"{username} silindi ❌")
    else:
        update.message.reply_text("Tapılmadı")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_users))
    dp.add_handler(CommandHandler("remove", remove))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
