import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "TOKEN"  # Railway-da env-dən gəlir (dəyişmə)

users = []

# START
def start(update, context):
    update.message.reply_text("Salam 👋 Bot aktivdir!\n\nKomandalar:\n/add username\n/list\n/remove username\n/yoxla username")

# HELP
def help_command(update, context):
    update.message.reply_text("Komandalar:\n/add username\n/list\n/remove username\n/yoxla username")

# ADD
def add(update, context):
    username = " ".join(context.args)
    if username:
        users.append(username)
        update.message.reply_text(f"{username} əlavə olundu ✅")
    else:
        update.message.reply_text("Username yaz!")

# LIST
def list_users(update, context):
    if users:
        update.message.reply_text("\n".join(users))
    else:
        update.message.reply_text("Siyahı boşdur")

# REMOVE
def remove(update, context):
    username = " ".join(context.args)
    if username in users:
        users.remove(username)
        update.message.reply_text(f"{username} silindi ❌")
    else:
        update.message.reply_text("Tapılmadı")

# YOXLA (aktivlik check)
def yoxla(update, context):
    username = " ".join(context.args)

    if not username:
        update.message.reply_text("Username yaz!")
        return

    url = f"https://www.instagram.com/{username}/"
    r = requests.get(url)

    if r.status_code == 200:
        update.message.reply_text(f"{username} aktivdir ✅")
    else:
        update.message.reply_text(f"{username} tapılmadı ❌")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_users))
    dp.add_handler(CommandHandler("remove", remove))
    dp.add_handler(CommandHandler("yoxla", yoxla))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
