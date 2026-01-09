from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_buttons(btns, size=[1], repeat=False): # noqa
    ikb = InlineKeyboardBuilder()

    ikb.add(*[InlineKeyboardButton(text=text, callback_data=callback)
        for text, callback in btns])

    ikb.adjust(*size, repeat=repeat)
    return ikb.as_markup()