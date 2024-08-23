from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
import app.keyboards as kb
from create_bot import TOKEN, bot
import requests
import cups
import os

#----------------------------CREATING CONNECTION FROM CUPS--------------------------------#
conn = cups.Connection()
printers = conn.getPrinters()
form_router = Router()
options = {}
route = ''
printer_name = list(printers.keys())[0]
print(printer_name)


#-------------------------------------------------------------------------------------------#


#---------------------------------CREATING CLASS FSM-----------------------------------------#
class Form(StatesGroup):
    language = State()
    command = State()
    file = State()
    copy = State()
    orientation = State()
    pages = State()
    page_per_sheet = State()
#--------------------------------------------------------------------------------------------#


#------------------------------------START COMMAND-------------------------------------------#
@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.language)
    # await message.answer("Choose the language", reply_markup=ReplyKeyboardRemove())
    await message.answer("Choose the language", reply_markup=kb.langs
                         )
#----------------------------------------------------------------------------------------------


#----------------------------------LANGUAGE PROCESS--------------------------------------
@form_router.message(F.text, Form.language)
async def process_language(message: Message, state: FSMContext) -> None:
    await state.update_data(lang=message.text)
    await state.set_state(Form.command)
    data = await state.get_data()
    if data['lang'] == "UZB":
        await message.answer("Tanlang", reply_markup=kb.chop_uz
                             )
    elif data['lang'] == "RU":
        await message.answer("Выберите команду", reply_markup=kb.chop_rus
                             )
    elif data['lang'] == "ENG":
        await message.answer("Choose the command", reply_markup=kb.chop_en
                             )
#---------------------------------------------------------------------------------------


#--------------------------------------------PRINT START(ENG)-----------------------------
@form_router.message(Command("print"))
async def command_print(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.file)
    await state.update_data(command=message.text)
    await message.answer(
        "Send file",
        reply_markup=ReplyKeyboardRemove(),
    )
#------------------------------------------------------------------------------------


#------------------------------CHOP(UZB)--------------------------------------------------
@form_router.message(Command("chop"))
async def command_print(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.file)
    await state.update_data(command=message.text)
    await message.answer(
        "Faylni yuboring",
        reply_markup=ReplyKeyboardRemove(),
    )
#-----------------------------------------------------------------------------------------


#-----------------------------ПЕЧАТАТЬ(RUS)----------------------------------------------------
@form_router.message(Command("печатать"))
async def command_print(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.file)
    await state.update_data(command=message.text)
    await message.answer(
        "Выберите файл",
        reply_markup=ReplyKeyboardRemove(),
    )
#-------------------------------------------------------------------------------------------


#--------------------------------DOCUMENT PROCESS------------------------------------------
@form_router.message(F.document, Form.file)
async def process_file(message: Message, state: FSMContext) -> None:
    await state.update_data(file=message.document.file_name)
    await state.set_state(Form.copy)

    data = await state.get_data()
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    print(file_path)
    download_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    print(download_url)
    res = requests.get(download_url)
    print(res)
    if res.status_code == 200:
        with open('File.pdf', 'wb') as file:
            file.write(res.content)
            print("File downloaded")
    else:
        print("Failed to download the file")
    global route
    route = os.path.abspath('File.pdf')
    #  print(route)
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
#-----------------------------------------------------------------------------------------------


#---------------------------------------COPIES PROCESS------------------------------------------
@form_router.message(F.text, Form.copy)
async def process_copy(message: Message, state: FSMContext) -> None:
    await state.update_data(copies=message.text)
    await state.set_state(Form.orientation)
    data = await state.get_data()
    if data['lang'] == 'UZB':
        await message.answer(f"Tanlang:", reply_markup=kb.orient_uzb
                             )
    if data['lang'] == 'RU':
        await message.answer("Выберите: ", reply_markup=kb.orient_rus
                             )

    if data['lang'] == 'ENG':
        await message.answer("Choose: ", reply_markup=kb.orient_en
                             )
#------------------------------------------------------------------------------------------


#---------------------------ORIENTATION PROCESS---------------------------------------------------
@form_router.message(F.text, Form.orientation)
async def process_orientation(message: Message, state: FSMContext) -> None:
    # await state.update_data(orienation=message.text)
    if message.text == '/Portret' or message.text == '/Портрет':
        await state.update_data(orientation=3)
    else:
        await state.update_data(orientation=4)
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
#-------------------------------------------------------------------------------------------------


#----------------------------------------PAGES PROCESS--------------------------------------------
@form_router.message(F.text, Form.pages)
async def process_pages(message: Message, state: FSMContext) -> None:
    await state.update_data(page_ranges=message.text)
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
#--------------------------------------------------------------------------------------------------


#---------------------------------------PAGE_PER_SHEET PROCESS-------------------------------------
@form_router.message(F.text, Form.page_per_sheet)
async def process_pages(message: Message, state: FSMContext) -> None:
    await state.update_data(pages_per_sheet=message.text)
    data = await state.get_data()
    #await state.clear()
    if data['lang'] == 'UZB':
        await message.answer(
            f"Tekshiring:\nFayl: {data['file']},\nNusxa soni: {data['copies']},\nBetlar: {data['page_ranges']},\nBir betdagi varoqlar soni: {data['pages_per_sheet']}",
            reply_markup=kb.final_chop_uz
        )
    elif data['lang'] == 'RU':
        await message.answer(
            f"Проверьте:\nФайл: {data['file']},\nЧисло копий: {data['copies']},\nСтраницы: {data['page_ranges']},\nЧисло страниц на одном листе: {data['pages_per_sheet']}",
            reply_markup=kb.final_chop_rus
        )
    elif data['lang'] == 'ENG':
        await message.answer(
            f"Check settings:\nFile: {data['file']},\nCopy: {data['copies']},\nPages: {data['page_ranges']},\nPages per sheet: {data['pages_per_sheet']}",
            reply_markup=kb.final_chop_en
        )

    data['orientation-requested'] = data['orientation']
    data['page-ranges'] = data['page_ranges']
    data['number-up'] = data['pages_per_sheet']

    del data['orientation'], data['page_ranges'], data['pages_per_sheet']

    print(data)
    options['copies'] = data['copies']
    options['media'] = 'A4'
    options['orientation-requested'] = data['orientation-requested']
    options['page-ranges'] = data['page-ranges']
    options['number-up'] = data['number-up']
    print(options)
    print(route)
    await state.clear()
#-------------------------------------------------------------------------------------------------


#----------------------------------CHOP QILISH-----------------------------------------------------
@form_router.message(Command('Chop'))
async def final_print(message: Message) -> None:
    await message.answer(
        f"Iltmos kuting{options}",
        reply_markup=ReplyKeyboardRemove(),
    )
    #print(route)
    job_id = conn.printFile(printer_name, route, "Test Print", {})
    print(job_id)
#--------------------------------------------------------------------------------------------------