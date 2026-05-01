import telebot
import json
import time
import threading
import requests

TOKEN = "8307363974:AAGtaAf1v4hyPso0ejFf8bFumDOTHi2hHrE"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"
CHAT_ID = None

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

@bot.message_handler(commands=['start'])
def start(message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    bot.reply_to(message, "Bot aktivdir ✅")

@bot.message_handler(commands=['add'])
def add(message):
    username = message.text.replace("/add ", "")
    if username:
        users[username] = "unknown"
        save_users(users)
        bot.reply_to(message, f"{username} əlavə olundu 👌")
    else:
        bot.reply_to(message, "Username yaz")

@bot.message_handler(commands=['list'])
def list_users(message):
    if users:
        bot.reply_to(message, "\n".join(users.keys()))
    else:
        bot.reply_to(message, "Boşdur")

@bot.message_handler(commands=['remove'])
def remove(message):
    username = message.text.replace("/remove ", "")
    if username in users:
        del users[username]
        save_users(users)
        bot.reply_to(message, "Silindi ❌")
    else:
        bot.reply_to(message, "Tapılmadı")

def checker():
    time.sleep(10)
    while True:
        for username in users:
            status = check_instagram(username)

            if users[username] == "closed" and status == "active":
                if CHAT_ID:
                    bot.send_message(CHAT_ID, f"{username} AÇILDI 🔥")

            users[username] = status
            save_users(users)

            time.sleep(5)

        time.sleep(60)

threading.Thread(target=checker, daemon=True).start()

print("Bot işləyir...")
bot.infinity_polling()
