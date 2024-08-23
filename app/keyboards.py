from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


langs = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="UZB"),
                KeyboardButton(text="RU"),
                KeyboardButton(text="ENG")
            ]
        ],
        resize_keyboard=True,
    )


chop_uz = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/chop"),
                    KeyboardButton(text="/sozlamalar"),
                ]
            ],
            resize_keyboard=True,
        )

chop_rus = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/печатать"),
                    KeyboardButton(text="/настройки"),
                ]
            ],
            resize_keyboard=True,
        )

chop_en = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/print"),
                    KeyboardButton(text="/settings"),
                ]
            ],
            resize_keyboard=True,
        )

orient_uzb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/Portret"),
                    KeyboardButton(text="/Albom"),
                ]
            ],
            resize_keyboard=True,
        )

orient_rus = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/Портрет"),
                    KeyboardButton(text="/Альбом"),
                ]
            ],
            resize_keyboard=True,
        )

orient_en = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/Portret"),
                    KeyboardButton(text="/Albom"),
                ]
            ],
            resize_keyboard=True,
        )

final_chop_uz = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='/Chop'),
                        KeyboardButton(text='/Bekor_qilish'),
                    ]
                ],
                resize_keyboard=True,
            )

final_chop_rus = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='Печатать'),
                        KeyboardButton(text='Отмена'),
                    ]
                ],
                resize_keyboard=True,
            )

final_chop_en = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='Print'),
                        KeyboardButton(text='Cancel')
                    ]
                ],
                resize_keyboard=True,
            )