from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

manage_users_btn = InlineKeyboardButton('📋 Перейти до списку користувачів', callback_data='manage_users_cb')
add_admin_btn = InlineKeyboardButton('🔐 Додати адміністратора', callback_data='add_admin_cb')
action_choose_kb = InlineKeyboardMarkup()
action_choose_kb.add(manage_users_btn).add(add_admin_btn)