import asyncio
import logging
import sys
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

form_router = Router()


class Form(StatesGroup):
    language = State()
    command = State()
    file = State()
    copy = State()
    pages = State()
    page_per_sheet = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.language)
    # await message.answer("Choose the language", reply_markup=ReplyKeyboardRemove())
    await message.answer("Choose the language", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="UZB"),
                KeyboardButton(text="RU"),
                KeyboardButton(text="ENG")
            ]
        ],
        resize_keyboard=True,
    ),

                         )


@form_router.message(F.text, Form.language)
async def process_language(message: Message, state: FSMContext) -> None:
    await state.update_data(lang=message.text)
    await state.set_state(Form.command)
    data = await state.get_data()
    if data['lang'] == "UZB":
        await message.answer("Tanlang", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/chop"),
                    KeyboardButton(text="/sozlamalar"),
                ]
            ],
            resize_keyboard=True,
        ),
                             )
    elif data['lang'] == "RU":
        await message.answer("Выберите команду", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/печатать"),
                    KeyboardButton(text="/настройки"),
                ]
            ],
            resize_keyboard=True,
        ),
                             )
    elif data['lang'] == "ENG":
        await message.answer("Choose the command", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/print"),
                    KeyboardButton(text="/settings"),
                ]
            ],
            resize_keyboard=True,
        ),
                             )


@form_router.message(Command("print"))
async def command_print(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.file)
    await state.update_data(command=message.text)
    await message.answer(
        "Send file",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command("chop"))
async def command_print(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.file)
    await state.update_data(command=message.text)
    await message.answer(
        "Faylni yuboring",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command("печатать"))
async def command_print(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.file)
    await state.update_data(command=message.text)
    await message.answer(
        "Выберите файл",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(F.document, Form.file)
async def process_file(message: Message, state: FSMContext) -> None:
    await state.update_data(file=message.document.file_name)
    await state.set_state(Form.copy)
    data = await state.get_data()
    if data['lang'] == 'UZB':
        await message.answer(
            f"Nusxalar sonini kiriting"
        )
    elif data['lang'] == 'RU':
        await message.answer(
            f"Введите количество копий"
        )
    elif data['lang'] == 'ENG':
        await message.answer(
            f"Enter the copy number"
        )


@form_router.message(F.text, Form.copy)
async def process_copy(message: Message, state: FSMContext) -> None:
    await state.update_data(copy=message.text)
    await state.set_state(Form.pages)
    data = await state.get_data()

    if data['lang'] == 'UZB':
        await message.answer(
            "Betlarni tanlang",
            reply_markup=ReplyKeyboardRemove()
        )
    elif data['lang'] == 'RU':
        await message.answer(
            "Выберите страниц",
            reply_markup=ReplyKeyboardRemove()
        )
    elif data['lang'] == 'ENG':
        await message.answer(
            "Choose pages",
            reply_markup=ReplyKeyboardRemove()
        )


@form_router.message(F.text, Form.pages)
async def process_pages(message: Message, state: FSMContext) -> None:
    await state.update_data(pages=message.text)
    await state.set_state(Form.page_per_sheet)
    data = await state.get_data()
    if data['lang'] == 'UZB':
        await message.answer("Betdagi varoqlar sonini kiriting", reply_markup=ReplyKeyboardRemove()
                             )
    elif data['lang'] == 'RU':
        await message.answer("Страниц в одном листе", reply_markup=ReplyKeyboardRemove()
                             )
    elif data['lang'] == 'ENG':
        await message.answer("Pages per sheet", reply_markup=ReplyKeyboardRemove()
                             )


@form_router.message(F.text, Form.page_per_sheet)
async def process_pages(message: Message, state: FSMContext) -> None:
    await state.update_data(pages_per_sheet=message.text)
    data = await state.get_data()
    #await state.clear()
    if data['lang'] == 'UZB':
        await message.answer(
            f"Tekshiring:\nFayl: {data['file']},\nNusxa soni: {data['copy']},\nBetlar: {data['pages']},\nBir betdagi varoqlar soni: {data['pages_per_sheet']}"
        )
    elif data['lang'] == 'RU':
        await message.answer(
            f"Проверьте:\nФайл: {data['file']},\nЧисло копий: {data['copy']},\nСтраницы: {data['pages']},\nЧисло страниц на одном листе: {data['pages_per_sheet']}"
        )
    elif data['lang'] == 'ENG':
        await message.answer(
            f"Check settings:\nFile: {data['file']},\nCopy: {data['copy']},\nPages: {data['pages']},\nPages per sheet: {data['pages_per_sheet']}"
        )


async def main():
    bot = Bot(token='6908559354:AAG0PcDJfS0GQP91ScQpVL5Sh5HHxDbJmq4',
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(form_router)

    # Start event dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
