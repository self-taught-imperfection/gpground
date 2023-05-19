import openai
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

openai.api_key = os.environ["TOKEN"]
telegram_token = '5485804927:AAF8bCIXghrwvvBInILxffWx_oZ9AIbp9zI'
max_token_count = 4000

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

messages = [
    {
        "role": "system",
        "content": "Ты Михаил Премудрый."
    }
]


def update(messages, role, content):
    """
    Функция обновления списка сообщений
    """
    messages.append({"role": role, "content": content})


def reset_messages():
    """
    Функция очистки истории сообщений контекста, чтобы избежать ошибки с токенами
    """
    messages.clear()
    messages.append({
        "role": "system",
        "content": "You are a programming assistant at Proghunter.ru, helping users with Python and JavaScript programming with popular frameworks."
    })


@dp.message_handler()
async def send(message: types.Message):
    try:
        update(messages, 'user', message.text)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=max_token_count,
        )
        if response['usage']['total_tokens'] >= max_token_count:
            await message.answer(
                f'В данный момент вы использовали максимум токенов в рамках контекста: {response["usage"]["total_tokens"]}, будет произведена очистка памяти')
            reset_messages()
        await message.answer(response['choices'][0]['message']['content'], parse_mode="markdown")
    except openai.OpenAIError as ex:
        await message.answer(ex.error)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)