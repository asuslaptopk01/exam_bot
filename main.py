import asyncio
import logging
import sys
from os import getenv
from pyexpat.errors import messages
from unicodedata import category

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from buttons.reply import make_reply_buttons
from buttons.inline import make_inline_buttons
from database.models import Categories, Foods

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    btns = [("🍽 Restoran menyusi", "main_menu"), ("📲 Biz bilan bog'lanish", "connect_us")] # noqa
    markup = make_inline_buttons(btns, repeat=True)
    await message.answer(f"Assalamu alaykum, {html.bold(message.from_user.full_name)}\nRestoranimiz rasmiy botiga xush kelibsiz!", reply_markup=markup)


@dp.callback_query(F.data == "connect_us")
async def connect_us_handler(callback:CallbackQuery) -> None:
    await callback.message.answer(f"📲 Biz bilan bog'lanish:\n\n📞 Telefon raqam: +998 99 111 11 01\n📧 Email: RestaurantOfficial@gmail.com\n🤖 Telegrarm bot: {html.link(value="Restaurant Bot", link="https://t.me/exam_restaurant_bot")}")


@dp.callback_query(F.data == "main_menu")
async def main_menu_handler(callback:CallbackQuery) -> None:
    categories : list[Categories] = Categories().get()
    btns = [(category.name, f"category_{category.id}") for category in categories] # noqa
    markup = make_inline_buttons(btns, size=[1], repeat=True)
    await callback.message.answer("🍽 Restoran menyusi\n🔽🔽🔽🔽🔽", reply_markup=markup)


@dp.callback_query(F.data.startswith("category_"))
async def category_handler(callback:CallbackQuery) -> None:
    category_id = int(callback.data.split("_")[1])
    category = Categories().get(category_id)
    foods : list[Foods] = Foods(category_id=category_id).get()
    btns = [(food.name, f"food_{food.id}") for food in foods] # noqa
    btns.append([("◀️ Back", "back_main_menu")]) # noqa
    markup = make_inline_buttons(btns, size=[1], repeat=True)
    await callback.message.answer(f"{category.name}", reply_markup=markup)


@dp.callback_query(F.data == "back_main_menu")
async def back_handler(callback:CallbackQuery) -> None:
    btns = [("🍽 Restoran menyusi", "main_menu"), ("📲 Biz bilan bog'lanish", "connect_us")]  # noqa
    markup = make_inline_buttons(btns, repeat=True)
    await callback.message.answer("🏠 Asosiy menyu", reply_markup=markup)


@dp.callback_query(F.data.startswith("food_"))
async def food_handler(callback:CallbackQuery) -> None:
    food_id = int(callback.data.split("_")[1])
    food : list[Foods] = Foods(food_id).get()
    caption = f"""{food.name}\n\n{food.description}\n\nSotuvda {food.quantity} ta bor\nNarxi: {food.price} so'm"""
    btn = [("◀️ Back", "back_categories")]
    markup = make_inline_buttons(btn)
    await callback.message.answer_photo(photo=food.photo, caption=caption, reply_markup=markup)


@dp.callback_query(F.data == "back_categories")
async def back_categories_handler(callback:CallbackQuery) -> None:
    category_id = int(callback.data.split("_")[1])
    category = Categories().get(category_id)
    foods: list[Foods] = Foods(category_id=category_id).get()
    btns = [(food.name, f"food_{food.id}") for food in foods]  # noqa
    btns.append([("◀️ Back", "back_main_menu")])  # noqa
    markup = make_inline_buttons(btns, size=[1], repeat=True)
    await callback.message.answer(f"{category.name}", reply_markup=markup)



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())