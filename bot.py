import re
from datetime import datetime

import requests
import asyncio

from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = '6851752685:AAEnoB0jNVKzchHNC4zcWeRmhvlQRpMfaEE'
API_URL = "http://51.250.126.124:8094/api"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}


class ApplicationCreate(StatesGroup):
    enter_name = State()
    choosing_municipality = State()
    choosing_school = State()
    enter_child_name = State()
    choosing_child_gender = State()
    enter_child_age = State()
    application_send = State()
    choosing_duration = State()


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
            applications_data = response.json()['results']
            if applications_data:
                keyboard = ReplyKeyboardBuilder()
                for application in applications_data:
                    id = application['id']
                    fio_applicant = application['full_name']
                    fio_child = application['child_full_name']
                    created_at = datetime.strptime(application['created_at'], '%Y-%m-%dT%H:%M:%S.%f').strftime(
                        '%d.%m.%Y')
                    button_text = f"Заявка №{id}  {fio_applicant} - {fio_child} от {created_at}"
                    keyboard.row(types.KeyboardButton(text=button_text))

                keyboard.row(types.KeyboardButton(text="Вернуться в главное меню"))

                await message.answer("Выберите заявку:", reply_markup=keyboard.as_markup())
            else:
                await message.answer("У вас нет заявок.")
        else:
            await message.answer("Произошла ошибка при получении данных о заявках.")

    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")
        print(e)


async def show_application_details(message: types.Message, application_id: int):
    try:
        api_url = f'{API_URL}/applications/{application_id}/'
        response = requests.get(api_url, headers=HEADERS)

        if response.status_code == 200:
            application_data = response.json()

            created_at = datetime.strptime(application_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            formatted_created_at = created_at.strftime('%H:%M %d.%m.%Y')

            formatted_text = f"Информация о заявке №{application_id}:\n"
            formatted_text += f"ФИО Заявителя: {application_data['full_name']}\n"
            formatted_text += f"ФИО Ребенка: {application_data['child_full_name']}\n"
            formatted_text += f"Пол ребенка: {application_data['child_gender']}\n"
            formatted_text += f"Возраст ребенка: {application_data['child_age']} лет\n"
            formatted_text += f"Получено предложение: {'Да' if application_data['received_offer'] else 'Нет'}\n"
            formatted_text += f"Срок пребывания: {application_data['duration']}\n"
            formatted_text += f"Время создания заявки: {formatted_created_at}\n"

            await message.answer(formatted_text)
        else:
            await message.answer("Произошла ошибка при получении информации о заявке.")

    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")


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
        response = requests.get(api_url_check, headers=HEADERS)
        data = response.json()

        if data['results']:
            await show_main_menu(message)
        else:
            api_url_create = f'{API_URL}/applicants/'
            data = {'phone_number': phone_number, 'telegram_id': chat_id}

            response_create = requests.post(api_url_create, json=data, headers=HEADERS)

            if response_create.status_code == 201:
                await show_main_menu(message)
            else:
                await message.answer("Произошла ошибка при добавлении данных.")
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")


@dp.message(lambda message: message.text == "Мои заявки")
async def show_applications(message: types.Message):
    await show_applications_menu(message)


@dp.message(lambda message: message.text == "Вернуться в главное меню")
async def return_to_main_menu(message: types.Message):
    await show_main_menu(message)


@dp.message(lambda message: re.match(r"^Заявка №\d+", message.text))
async def process_application_selection(message: types.Message):
    try:
        application_id_match = re.search(r"\d+", message.text)
        if application_id_match:
            application_id = int(application_id_match.group())
            await show_application_details(message, application_id)
        else:
            raise ValueError("Application ID not found in message text.")
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")
        print(e)


@dp.message(StateFilter(None),
            lambda message: message.text.startswith("Создать новую заявку") if message.text else None)
async def start_application_creation(message: types.Message, state: FSMContext):
    try:
        await message.answer("Введите ФИО заявителя:")
        await state.set_state(ApplicationCreate.enter_name)
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")
        print(e)


@dp.message(ApplicationCreate.enter_name, F.text)
async def name_entering(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await message.answer("Спасибо")

    api_url = f'{API_URL}/municipalities/'
    response = requests.get(api_url, headers=HEADERS)
    municipalities_data = response.json()['results']

    keyboard = ReplyKeyboardBuilder()
    for municipality in municipalities_data:
        keyboard.row(types.KeyboardButton(text=municipality['name']))
    await message.answer("Выберите муниципальное образование:", reply_markup=keyboard.as_markup())
    await state.set_state(ApplicationCreate.choosing_municipality)


@dp.message(ApplicationCreate.choosing_municipality, F.text)
async def municipality_chosen(message: types.Message, state: FSMContext):
    api_url = f'{API_URL}/municipalities/?name={message.text}'
    response = requests.get(api_url, headers=HEADERS)
    municipality = response.json()['results'].first()

    if municipality:
        await state.update_data(municipality=municipality['id'])

    api_url = f'{API_URL}/schools/?municipality={municipality["id"]}'
    response = requests.get(api_url, headers=HEADERS)
    school_data = response.json()['results']

    keyboard = ReplyKeyboardBuilder()
    for school in school_data:
        keyboard.row(types.KeyboardButton(text=school['name']))
    await message.answer("Выберите школу:", reply_markup=keyboard.as_markup())

    await state.set_state(ApplicationCreate.choosing_school)


@dp.message(ApplicationCreate.choosing_school, F.text)
async def school_chosen(message: types.Message, state: FSMContext):
    #await state.set_state(ApplicationCreate.choosing_school)
    print('hello')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
