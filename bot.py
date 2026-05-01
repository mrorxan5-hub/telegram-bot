import telebot
import json
import random
import time
import threading
import requests



TOKEN = "8307363974:AAGtaAf1v4hyPso0ejFf8bFumDOTHi2hHrE"

DATA_FILE = "users.json"
CHAT_ID = None

# ---------- LOAD ----------
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# ---------- SAVE ----------
def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

# ---------- CHECK ----------
def check_instagram(username):
    url = f"https://www.instagram.com/{username}/"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return "active"
        elif r.status_code == 404:
            return "closed"
        else:
            return "unknown"
    except:
        return "unknown"

# ---------- COMMANDS ----------
def start(update, context):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    update.message.reply_text("Bot aktivdir ✅")

def add(update, context):
    username = " ".join(context.args)
    if username:
        users[username] = "unknown"
        save_users(users)
        update.message.reply_text(f"{username} əlavə olundu 👌")
    else:
        update.message.reply_text("Username yaz")

def list_users(update, context):
    if users:
        update.message.reply_text("\n".join(users.keys()))
    else:
        update.message.reply_text("Boşdur")

def remove(update, context):
    username = " ".join(context.args)
    if username in users:
        del users[username]
        save_users(users)
        update.message.reply_text("Silindi ❌")
    else:
        update.message.reply_text("Tapılmadı")

# ---------- BACKGROUND ----------
def checker(updater):
    time.sleep(10)
    while True:
        for username in users:
            status = check_instagram(username)

            if users[username] == "closed" and status == "active":
                if CHAT_ID:
                    updater.bot.send_message(
                        chat_id=CHAT_ID,
                        text=f"{username} AÇILDI 🔥"
                    )

            users[username] = status
            save_users(users)

            time.sleep(random.randint(5, 10))

        time.sleep(60)

# ---------- MAIN ----------
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_users))
    dp.add_handler(CommandHandler("remove", remove))

    threading.Thread(target=checker, args=(updater,), daemon=True).start()

    print("Bot işləyir...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
