import json
import random
import time
import threading
import requests
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "SENIN_TOKEN"

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
async def start(update, context):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text("Bot aktivdir ✅")

async def add(update, context):
    username = " ".join(context.args)

    if username:
        users[username] = "unknown"
        save_users(users)
        await update.message.reply_text(f"{username} əlavə olundu 👌")
    else:
        await update.message.reply_text("Username yaz")

async def list_users(update, context):
    if users:
        await update.message.reply_text("\n".join(users.keys()))
    else:
        await update.message.reply_text("Boşdur")

async def remove(update, context):
    username = " ".join(context.args)

    if username in users:
        del users[username]
        save_users(users)
        await update.message.reply_text("Silindi ❌")
    else:
        await update.message.reply_text("Tapılmadı")

# ---------- BACKGROUND ----------
def checker(app):
    time.sleep(10)

    while True:
        for username in users:
            status = check_instagram(username)

            if users[username] == "closed" and status == "active":
                if CHAT_ID:
                    app.bot.send_message(
                        chat_id=CHAT_ID,
                        text=f"{username} AÇILDI 🔥"
                    )

            users[username] = status
            save_users(users)

            time.sleep(random.randint(5, 10))

        time.sleep(60)

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_users))
    app.add_handler(CommandHandler("remove", remove))

    threading.Thread(target=checker, args=(app,), daemon=True).start()

    print("Bot işləyir...")
    app.run_polling()

if __name__ == "__main__":
    main()
