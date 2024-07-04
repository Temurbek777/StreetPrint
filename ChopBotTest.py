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
    file = State()
    copy = State()
    pages = State()
    page_per_sheet = State()


@form_router.message(Command("print"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.file)
    await message.answer(
        "Fileni yuboring",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(F.document, Form.file)
async def process_file(message: Message, state: FSMContext) -> None:
    await state.update_data(file=message.document.file_name)
    await state.set_state(Form.copy)
    await message.answer(
        f"Nechta nusxa chiqrish kerak?"
    )


@form_router.message(F.text, Form.copy)
async def process_copy(message: Message, state: FSMContext) -> None:
    await state.update_data(copy=message.text)
    await state.set_state(Form.pages)
    data = await state.get_data()
    await message.answer(
        "Betlarni tanlang",
        reply_markup=ReplyKeyboardRemove()
    )


@form_router.message(F.text, Form.pages)
async def process_pages(message: Message, state: FSMContext) -> None:
    await state.update_data(pages=message.text)
    await state.set_state(Form.page_per_sheet)
    #  data = await state.get_data()
    await message.answer("Pages per sheet", reply_markup=ReplyKeyboardRemove()
                         )


@form_router.message(F.text, Form.page_per_sheet)
async def process_pages(message: Message, state: FSMContext) -> None:
    await state.update_data(pages_per_sheet=message.text)
    data = await state.get_data()
    #await state.clear()
    await message.answer(f"Check the settings:\nFile: {data['file']},\nCopy: {data['copy']},\nPages: {data['pages']},\nPages per sheet: {data['pages_per_sheet']}")


async def main():
    bot = Bot(token='6908559354:AAG0PcDJfS0GQP91ScQpVL5Sh5HHxDbJmq4',
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(form_router)

    # Start event dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
