from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_btn = InlineKeyboardButton('🖼Почати працювати з ботом', callback_data='start_cb')
start_kb = InlineKeyboardMarkup()
start_kb.add(start_btn)