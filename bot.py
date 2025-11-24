import os
import telebot
import openai

TOKEN = "8259302388:AAGXqgpZLSVDh_y7YlO3citWYyS8JVdzaSs"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_KEY

@bot.message_handler(content_types=['voice', 'text'])
def handle_message(message):
    bot.reply_to(message, "Бот подключён. Голос пока не обрабатываю.")

bot.polling(none_stop=True)
