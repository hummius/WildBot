from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_kb = [
    [types.KeyboardButton(text='Получить информацию по товару<')],
    [types.KeyboardButton(text='Остановить уведомления')],
    [types.KeyboardButton(text='Получить информацию из БД')],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=start_kb, resize_keyboard=True)

inline_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Подписаться 🛎', callback_data='True'),]
    ]
)

