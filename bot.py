import os
import telebot
import openai

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_KEY

@bot.message_handler(content_types=['voice', 'text'])
def handle_message(message):
    bot.reply_to(message, "Бот подключён. Голос пока не обрабатываю.")

bot.polling(none_stop=True)
