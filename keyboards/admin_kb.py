from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

manage_users_btn = InlineKeyboardButton('📋 Список користувачів', callback_data='manage_users_cb')
select_user_btn = InlineKeyboardButton('📍 Обрати користувача', callback_data='select_user_cb')
add_admin_btn = InlineKeyboardButton('🔐 Додати адміністратора', callback_data='add_admin_cb')
action_choose_kb = InlineKeyboardMarkup()
action_choose_kb.add(manage_users_btn).add(select_user_btn).add(add_admin_btn)