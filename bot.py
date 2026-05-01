import telebot
import json
import time
import threading
import requests

TOKEN = "8307363974:AAGtaAf1v4hyPso0ejFf8bFumDOTHi2hHrE"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"
CHAT_IDS = set()

# ---------- USER SAVE ----------
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
        "User-Agent": "Mozilla/5.0"
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
@bot.message_handler(commands=['start'])
def start(message):
    CHAT_IDS.add(message.chat.id)
    bot.reply_to(message, "Bot aktivdir ✅")

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, "Bot işləyir 🔥")

@bot.message_handler(commands=['add'])
def add(message):
    username = message.text.replace("/add ", "").strip()
    if username:
        users[username] = "unknown"
        save_users(users)
        bot.reply_to(message, f"{username} əlavə olundu ✅")
    else:
        bot.reply_to(message, "Username yaz ❗")

@bot.message_handler(commands=['list'])
def list_users(message):
    if users:
        bot.reply_to(message, "\n".join(users.keys()))
    else:
        bot.reply_to(message, "Boşdur")

@bot.message_handler(commands=['remove'])
def remove(message):
    username = message.text.replace("/remove ", "").strip()
    if username in users:
        del users[username]
        save_users(users)
        bot.reply_to(message, "Silindi ❌")
    else:
        bot.reply_to(message, "Tapılmadı")

# 🔥 BURDA SƏN İSTƏDİYİN /check
@bot.message_handler(commands=['check'])
def check_user(message):
    try:
        username = message.text.split(" ")[1]

        status = check_instagram(username)

        if status == "active":
            bot.reply_to(message, f"{username} aktivdir ✅")
        elif status == "closed":
            bot.reply_to(message, f"{username} bağlıdır ❌")
        else:
            bot.reply_to(message, f"{username} yoxlanmadı ⚠️")

    except:
        bot.reply_to(message, "Düz yaz: /check username")

# ---------- BACKGROUND CHECK ----------
def checker():
    time.sleep(10)
    while True:
        for username in users:
            status = check_instagram(username)

            if users[username] == "closed" and status == "active":
                for chat_id in CHAT_IDS:
                    bot.send_message(chat_id, f"{username} AÇILDI 🔥")

            users[username] = status
            save_users(users)

            time.sleep(5)

        time.sleep(60)

# ---------- RUN ----------
threading.Thread(target=checker, daemon=True).start()

print("Bot işləyir...")
bot.infinity_polling()
