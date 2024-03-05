from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

manage_users_btn = InlineKeyboardButton('📋 Список користувачів', callback_data='user_list_cb')
select_user_btn = InlineKeyboardButton('📍 Переглянути фото користувача', callback_data='select_user_cb')
add_admin_btn = InlineKeyboardButton('🔐 Додати адміністратора', callback_data='add_admin_cb')
remove_admin_btn = InlineKeyboardButton('🔒 Видалити адміністратора', callback_data='remove_admin_cb')
download_photos_btn = InlineKeyboardButton('🗄 Завантажити всі фотографії', callback_data='download_photos_cb')
remove_photos_btn = InlineKeyboardButton('🛑 Видалити всі фотографії', callback_data='remove_photos_cb')
action_choose_kb = InlineKeyboardMarkup()
action_choose_kb.add(manage_users_btn).add(select_user_btn).add(add_admin_btn).add(remove_admin_btn).add(download_photos_btn).add(remove_photos_btn)

confirm_btn = InlineKeyboardButton('✅ Підтвердити', callback_data='confirm_cb')
cancel_btn = InlineKeyboardButton('❌ Скасувати', callback_data='cancel_cb')
submit_kb = InlineKeyboardMarkup()
submit_kb.add(confirm_btn).add(cancel_btn)