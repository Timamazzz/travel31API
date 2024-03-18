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


async def show_main_menu(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Мои заявки"),
        types.KeyboardButton(text="Создать новую заявку")
    )
    await message.answer(
        "Главное меню",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


async def show_applications_menu(message: types.Message):
    try:
        chat_id = message.chat.id

        api_url = f'{API_URL}/applications/?telegram_id={chat_id}'
        response = requests.get(api_url, headers=HEADERS)

        if response.status_code == 200:
            applications_data = response.json()

            if applications_data:
                keyboard = ReplyKeyboardBuilder()
                for application in applications_data:
                    keyboard.row(types.KeyboardButton(text=f"Заявка {application['id']}"))

                keyboard.row(types.KeyboardButton(text="Вернуться в главное меню"))

                await message.answer("Выберите заявку:", reply_markup=keyboard.as_markup())
            else:
                await message.answer("У вас нет заявок.", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("Произошла ошибка при получении данных о заявках.",
                                 reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.", reply_markup=types.ReplyKeyboardRemove())


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

        api_url_check = f'{API_URL}/applicants/?phone_number={phone_number}&telegram_id={chat_id}'
        response_check = requests.get(api_url_check, headers=HEADERS)

        if response_check.status_code == 200:
            await show_main_menu(message)
        elif response_check.status_code == 404:
            api_url_create = f'{API_URL}/applicants/'
            data = {'phone_number': phone_number, 'telegram_id': chat_id}

            response_create = requests.post(api_url_create, json=data, headers=HEADERS)

            if response_create.status_code == 201:
                await show_main_menu(message)
            else:
                await message.answer("Произошла ошибка при добавлении данных.")
        else:
            await message.answer("Произошла ошибка при проверке данных.")
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")


@dp.message(text="Мои заявки")
async def show_applications(message: types.Message):
    await show_applications_menu(message)


@dp.message(text="Вернуться в главное меню")
async def return_to_main_menu(message: types.Message):
    await show_main_menu(message)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
