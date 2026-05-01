import os
import json
import random
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "SENIN_TOKEN"

DATA_FILE = "users.json"
CHAT_ID = None

# ---------- LOAD / SAVE ----------
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

# ---------- INSTAGRAM CHECK ----------
def check_instagram(username):
    url = f"https://www.instagram.com/{username}/"

    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0",
            "Chrome/120.0",
            "Safari/537.36"
        ])
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code == 200:
            return "active"
        elif r.status_code == 404:
            return "closed"
        else:
            return "unknown"
    except:
        return "unknown"

# ---------- COMMANDS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    await update.message.reply_text("Bot aktivdir ✅")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = " ".join(context.args)

    if username:
        users[username] = "unknown"
        save_users(users)
        await update.message.reply_text(f"{username} əlavə olundu 👌")
    else:
        await update.message.reply_text("Username yaz")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if users:
        text = "\n".join(users.keys())
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("Boşdur")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = " ".join(context.args)

    if username in users:
        del users[username]
        save_users(users)
        await update.message.reply_text(f"{username} silindi ❌")
    else:
        await update.message.reply_text("Tapılmadı")

# ---------- CHECK LOOP ----------
async def checker(app):
    await asyncio.sleep(10)

    while True:
        for username in users:
            status = check_instagram(username)

            if users[username] == "closed" and status == "active":
                if CHAT_ID:
                    await app.bot.send_message(
                        chat_id=CHAT_ID,
                        text=f"{username} AÇILDI 🔥"
                    )

            users[username] = status
            save_users(users)

            await asyncio.sleep(random.randint(5, 10))  # gizli delay

        await asyncio.sleep(60)

# ---------- MAIN ----------
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_users))
    app.add_handler(CommandHandler("remove", remove))

    app.create_task(checker(app))

    print("Bot işləyir...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
