import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.stream.read().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(data)])
    return "ok", 200

@app.route("/")
def index():
    return "Bot running", 200

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Бот работает.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
