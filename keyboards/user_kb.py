from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_btn = InlineKeyboardButton('🕹 Почати працювати з ботом', callback_data='start_cb')
start_kb = InlineKeyboardMarkup()
start_kb.add(start_btn)

submit_photo_btn = InlineKeyboardButton('📸 Надіслати фотографію', callback_data='submit_photo_cb')
send_kb = InlineKeyboardMarkup().add(submit_photo_btn)

cancel_photo_btn = InlineKeyboardButton('❌ Скасувати надсилання фотографії', callback_data='cancel_photo_cb')
cancel_kb = InlineKeyboardMarkup().add(cancel_photo_btn)