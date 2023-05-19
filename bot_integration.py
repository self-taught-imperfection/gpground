import openai
import telebot
import logging
import os
import time
import mishatokens
#from dotenv import load_dotenv

#load_dotenv()

openai.api_key = mishatokens.chatgpt_api_key
bot = mishatokens.telegram_api_key

# Логирование
if not os.path.exists('/tmp/bot_log/'):
    os.makedirs('/tmp/bot_log/')

logging.basicConfig(filename='/tmp/bot_log/log.txt', level=logging.ERROR,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет!\nЯ ChatGPT Telegram Bot\U0001F916\nЗадай мне любой вопрос и я постараюсь на него ответиь')

# Функция генерации ответа используя OpenAI API
def generate_response(prompt):
        completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": prompt}
  ]
)
        return completion.choices[0].message.content

# Обработчик команды /bot
@bot.message_handler(commands=['bot'])
def command_message(message):
    prompt = message.text
    response = generate_response(prompt)
    bot.reply_to(message, text=response)

# Обработчик остальных сообщений
@bot.message_handler(func = lambda _: True)
def handle_message(message):
    prompt = message.text
    response = generate_response(prompt)
    bot.send_message(chat_id=message.from_user.id, text=response)

# Запуск бота    
print('ChatGPT Bot is working')

while True:
    try:
        bot.polling()
    except (telebot.apihelper.ApiException, ConnectionError) as e:
        logging.error(str(e))
        time.sleep(5)
        continue