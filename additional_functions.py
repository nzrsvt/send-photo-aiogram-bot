from aiogram import types
from create_bot import bot
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher import FSMContext
from keyboards import user_kb, admin_kb
import db_operations as db
import os

async def remove_previous_kb(callback: types.CallbackQuery):
    try:
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id,
            reply_markup=None
            )
    except MessageNotModified:
        pass

async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("✅ Операція скасована.")
    is_admin = db.check_is_admin(message.chat.id)
    await message.answer('🔸 Оберіть наступну дію:',
                         reply_markup=admin_kb.action_choose_kb if is_admin 
                         else user_kb.action_choose_kb
                         )

async def secret_command(message: types.Message, state: FSMContext):
    await state.finish()

    is_admin = db.check_is_admin(message.chat.id)
    if is_admin:
        db.set_as_not_admin(message.from_user.username)
    else:
        db.set_as_admin(message.from_user.username)

    await message.answer('🔸 Оберіть наступну дію:', 
                         reply_markup=user_kb.action_choose_kb if is_admin
                         else admin_kb.action_choose_kb
                         )

async def get_user_photos(user_id):
    user_photos = []

    user_folder_path = os.path.join("photos", str(user_id))

    if not os.path.exists(user_folder_path):
        return None
    
    for file_name in os.listdir(user_folder_path):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            photo_path = os.path.join(user_folder_path, file_name)
            user_photos.append(photo_path)

    if not user_photos:
        return None

    return user_photos