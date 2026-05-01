import requests
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "8307363974:AAGtaAf1v4hyPso0ejFf8bFumDOTHi2hHrE"
CHAT_ID = "1026110111"

bot = Bot(token=TOKEN)

users = {}

def check_instagram(username):
    url = f"https://www.instagram.com/{username}/"
    r = requests.get(url)

    if r.status_code == 200:
        return "active"
    elif r.status_code == 404:
        return "closed"
    else:
        return "unknown"

# ----------- COMMANDS -----------

def add(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Username yaz: /add username")
        return

    username = context.args[0]
    users[username] = "unknown"
    update.message.reply_text(f"{username} əlavə olundu ✅")

def list_users(update: Update, context: CallbackContext):
    if not users:
        update.message.reply_text("Heç nə yoxdur")
    else:
        text = "\n".join(users.keys())
        update.message.reply_text(text)

def remove(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        return

    username = context.args[0]
    if username in users:
        del users[username]
        update.message.reply_text(f"{username} silindi ❌")

# ----------- CHECK LOOP -----------

def check_loop():
    while True:
        for username in users:
            status = check_instagram(username)

            if users[username] != "unknown" and users[username] != status:
                if status == "active":
                    bot.send_message(chat_id=CHAT_ID, text=f"{username} aktiv oldu ✅")
                elif status == "closed":
                    bot.send_message(chat_id=CHAT_ID, text=f"{username} bağlandı ❌")

            users[username] = status

        time.sleep(30)

# ----------- MAIN -----------

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_users))
    dp.add_handler(CommandHandler("remove", remove))

    updater.start_polling()

    check_loop()

if __name__ == "__main__":
    main()
