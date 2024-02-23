from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import bot
import db_operations as db
from keyboards import user_kb
import os
from aiogram_media_group import media_group_handler
from typing import List, Union
import asyncio
from aiogram.types import ParseMode
from aiogram.utils.exceptions import MessageNotModified

class InstagramEntering(StatesGroup):
    instagram_nickname = State()

class InstagramChanging(StatesGroup):
    instagram_nickname = State()

class PhotoSending(StatesGroup):
    photo = State()

async def enter_instagram_nickname_command(callback : types.CallbackQuery):
    await remove_previous_kb(callback)
    if not db.check_user_instagram_existence(callback.from_user.id):
        await InstagramEntering.instagram_nickname.set()
    else:
        await InstagramChanging.instagram_nickname.set()

    await callback.message.answer("Введіть свій Instagram-нікнейм:")
    await callback.answer() 

async def process_instagram_nickname(message: types.Message, state: FSMContext):
    try:
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention':
                    instagram_nickname = message.text[1:][entity.offset:entity.offset + entity.length]
        else:
            instagram_nickname = message.text

        db.update_user_instagram(message.chat.id, instagram_nickname)
        await state.finish()
        await message.answer(f"✅ {message.from_user.full_name}, нікнейм '{instagram_nickname}' збережено успішно!")
        await message.answer('🔸 Оберіть наступну дію:', reply_markup=user_kb.action_choose_kb)

    except Exception as e:
        await message.answer("⚠️ Виникла помилка при обробці запиту.")
        await state.finish()
        await message.answer('⬇️ Для початку роботи з ботом потрібно вказати свій Instagram-нікнейм. Натисніть на кнопку нижче.',reply_markup=user_kb.enter_instagram_kb)
        
async def send_photo_command(callback : types.CallbackQuery):
    await remove_previous_kb(callback)
    await PhotoSending.photo.set()
    await callback.message.answer("Надішліть свою фотографію: (одну або декілька)")
    await callback.answer()

async def process_photo(message: types.Message, state: FSMContext):
    success = await check_photo(message, state)
    if success == 0:
        await message.answer("💾 Фотографію збережено.")
        await message.answer('🔸 Оберіть наступну дію:',reply_markup=user_kb.action_choose_kb)
    elif success == 1:
        await message.answer("🚫 Розмір фотографії перевищує 2МБ.")
        await message.answer('🔸 Оберіть наступну дію:',reply_markup=user_kb.action_choose_kb)
    elif success == 2:
        await message.answer("🚫 Будь ласка, надішліть фотографію в іншому форматі.")
        await message.answer('🔸 Оберіть наступну дію:',reply_markup=user_kb.action_choose_kb)
    await state.finish()  

@media_group_handler()
async def process_photo_group(messages: List[types.Message], state: FSMContext):
    for message in messages:
        success = await check_photo(message, state)
        if success != 0:
            if success == 1:
                await message.answer("🚫 Розмір фотографії перевищує 2МБ.")
                await message.answer('🔸 Оберіть наступну дію:',reply_markup=user_kb.action_choose_kb)
            elif success == 2:
                await message.answer("🚫 Будь ласка, надішліть фотографію в іншому форматі.")
                await message.answer('🔸 Оберіть наступну дію:',reply_markup=user_kb.action_choose_kb)
            break
    if success == 0:
        await message.answer("💾 Фотографії збережено.")
        await message.answer('🔸 Оберіть наступну дію:',reply_markup=user_kb.action_choose_kb)
    await state.finish() 

# return values: 0 = saved, 1 = too large, 2 = wrong format
async def check_photo(message: types.Message, state: FSMContext):
    if message.photo:
        if message.photo[-1].file_size > 2 * 1024 * 1024:
            return 1
        else:
            photo = message.photo[-1].file_id   
            await handle_user_photo(message.chat.id, photo)
            return 0
    elif message.document:
        if message.document.file_size > 2 * 1024 * 1024:
            return 1
        else:
            file_name = message.document.file_name.lower()
            allowed_formats = ('.png', '.jpg', '.jpeg') 
            if any(file_name.endswith(format) for format in allowed_formats):
                photo = message.document.file_id
                await handle_user_photo(message.chat.id, photo)
                return 0
            else:
                return 2
    else:
        return 2
    
async def handle_user_photo(user_id, photo):
    file_path = await bot.get_file(photo)
    downloaded_file = await bot.download_file(file_path.file_path)

    user_folder_path = os.path.join("photos", str(user_id))
    os.makedirs(user_folder_path, exist_ok=True)
    
    photo_path = os.path.join(user_folder_path, f"{photo}.jpg")

    with open(photo_path, 'wb') as new_file:
        new_file.write(downloaded_file.read())

async def manage_photos_command(callback : types.CallbackQuery):
    await remove_previous_kb(callback) 
    photos = await get_user_photos(callback.from_user.id)
    if photos:
        await callback.message.answer("📌 Всі ваші фотографії:")
        for photo_path in photos:
            with open(photo_path, 'rb') as photo_file:
                keyboard = user_kb.get_delete_photo_keyboard(str(os.path.basename(photo_path))[:58])
                await bot.send_photo(chat_id=callback.from_user.id, photo=photo_file, reply_markup=keyboard)
                await asyncio.sleep(1)
        await callback.message.answer("ℹ️ Ви можете видаляти фотографії за допомогою кнопки 'Видалити фотографію'.", reply_markup=user_kb.return_to_menu_kb)
    else:
        await callback.message.answer("❌ Ви не маєте жодної фотографії.", reply_markup=user_kb.return_to_menu_kb)
    await callback.answer()

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

async def delete_photo_command(callback: types.CallbackQuery):
    await remove_previous_kb(callback)
    action, photo_path = callback.data.split(',')

    user_photos = await get_user_photos(callback.from_user.id)
    try:
        for user_photo_path in user_photos:
            if photo_path in user_photo_path:
                os.remove(user_photo_path)
                success = True
                break
        if success:
            await callback.answer("✅ Фотографію видалено.")
        else:
            await callback.answer("❌ Фотографія видалена раніше.")
    except:
        await callback.answer("❌ Фотографія видалена раніше.")
    await callback.answer()

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
    await message.answer('🔸 Оберіть наступну дію:',reply_markup=user_kb.action_choose_kb)