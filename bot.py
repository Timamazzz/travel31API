import requests
import asyncio
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = '6851752685:AAEnoB0jNVKzchHNC4zcWeRmhvlQRpMfaEE'
API_URL = "http://51.250.126.124:8094/api"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Поделиться номером телефона", request_contact=True),
    )
    await message.answer(
        "Поделиться",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(F.contact)
async def shared_contact(message: types.Message):
    try:
        phone_number = message.contact.phone_number
        chat_id = message.chat.id

        api_url = f'{API_URL}/applications/applicants/'
        data = {'phone_number': phone_number, 'telegram_id': chat_id}

        response = requests.post(api_url, json=data, headers=HEADERS)

        if response.status_code == 200:
            await message.answer("Данные успешно добавлены.")
        elif response.status_code == 404:
            await message.answer("Ошибка: не найден адрес API.")
        else:
            await message.answer("Произошла ошибка при добавлении данных.")
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
