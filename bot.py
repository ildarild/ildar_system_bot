import os
import telebot
import openai
import requests

TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_KEY


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_text = message.text

    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}]
    )

    answer = completion.choices[0].message["content"]
    bot.reply_to(message, answer)


# Обработка голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        # Получаем файл от Telegram
        file_info = bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        # Скачиваем ogg
        ogg_path = "voice.ogg"
        r = requests.get(file_url)
        with open(ogg_path, "wb") as f:
            f.write(r.content)

        # Whisper — расшифровка
        with open(ogg_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )

        text = transcript["text"]

        # Отправляем текст в ChatGPT
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        )

        answer = completion.choices[0].message["content"]

        # Ответ: сначала текст расшифровки
        bot.reply_to(message, f"📝 Расшифровка:\n{text}\n\n💬 Ответ:\n{answer}")

        os.remove(ogg_path)

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")


bot.polling(none_stop=True)
