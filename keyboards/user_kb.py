from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_btn = InlineKeyboardButton('🕹 Почати працювати з ботом', callback_data='start_cb')
start_kb = InlineKeyboardMarkup()
start_kb.add(start_btn)

enter_instagram_btn = InlineKeyboardButton('🏷 Ввести Instagram', callback_data='enter_instagram_cb')
enter_instagram_kb = InlineKeyboardMarkup()
enter_instagram_kb.add(enter_instagram_btn)

send_photo_btn = InlineKeyboardButton('📸 Надіслати фотографію', callback_data='send_photo_cb')
manage_photos_btn = InlineKeyboardButton('📋 Керувати надісланими фотографіями', callback_data='manage_photos_cb')
change_instagram_btn = InlineKeyboardButton('🏷 Змінити Instagram-нікнейм', callback_data='enter_instagram_cb')
action_choose_kb = InlineKeyboardMarkup()
action_choose_kb.add(send_photo_btn).add(manage_photos_btn).add(change_instagram_btn)

def get_delete_photo_keyboard(photo_path):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🗑 Видалити фотографію", callback_data = f"del,{photo_path}")
    )
    return keyboard

return_to_menu_btn = InlineKeyboardButton('◀️ Повернутись в меню', callback_data='return_to_menu_cb')
return_to_menu_kb = InlineKeyboardMarkup()
return_to_menu_kb.add(return_to_menu_btn)