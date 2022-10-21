import logging
import markovify
import random

from aiogram import Bot, Dispatcher, executor, types

# Токен бота
API_TOKEN = ''

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# Модель маркова, которая непосредственно генерирует сообщения
model = None


@dp.message_handler(commands=['saySomething'])
async def send_welcome(message: types.Message):
    """
    На команду генерировать сообщение без ограничения по символам
    И отправить как ответ на исходное сообщение.
    """
    await message.reply(model.make_sentence(tries=100))


@dp.message_handler()
async def echo(message: types.Message):
    """
    Случайный ответ на случайное сообщение
    """

    # random() генерирует дробное число от 0 до 1, так мы указываем вероятность ответа на сообщение
    # 0.1 * 100% = 10%
    if random.random() < 0.1:
        await message.reply(model.make_short_sentence(280, tries=100))


if __name__ == '__main__':
    """
    Запуск бота
    """

    # Вычитываем корпус текста из файла corpus.txt
    with open('corpus.txt') as f:
        text = f.read()

    # Генерируем модель и компилируем ее для более быстрой работы
    model = markovify.NewlineText(text)
    model.compile()

    # Запускаем longpolling телеграмного бота
    executor.start_polling(dp, skip_updates=True)

