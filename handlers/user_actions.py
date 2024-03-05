from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import bot
import db_operations as db
from keyboards import user_kb
import os
from aiogram_media_group import media_group_handler
from typing import List
import asyncio
from aiogram.utils.exceptions import MessageNotModified
from additional_functions import remove_previous_kb

class InstagramEntering(StatesGroup):
    instagram_nickname = State()

class InstagramChanging(StatesGroup):
    instagram_nickname = State()

class PhotoSending(StatesGroup):
    photo = State()

async def enter_instagram_nickname_command(callback : types.CallbackQuery):
    if callback.data == 'enter_instagram_cb':
        await InstagramEntering.instagram_nickname.set()
    else:
        is_existing_user = True
        await InstagramChanging.instagram_nickname.set()
    await remove_previous_kb(callback)
    await callback.message.answer("Введіть свій Instagram-нікнейм:")
    if is_existing_user:
        await callback.message.answer('* Ви можете скасувати обрану дію, написавши "скасувати"')
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
    await callback.message.answer('* Ви можете скасувати обрану дію, написавши "скасувати"')
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
            db.add_photo(message.chat.id, photo)
            return 0
    elif message.document:
        if message.document.file_size > 2 * 1024 * 1024:
            return 1
        else:
            file_name = message.document.file_name.lower()
            allowed_formats = ('.png', '.jpg', '.jpeg') 
            if any(file_name.endswith(format) for format in allowed_formats):
                photo = message.document.file_id
                db.add_photo(message.chat.id, photo)
                return 0
            else:
                return 2
    else:
        return 2
    
async def manage_photos_command(callback : types.CallbackQuery):
    await remove_previous_kb(callback) 
    photos = db.get_file_ids_by_user_id(callback.from_user.id)
    if photos:
        await callback.message.answer("📌 Всі ваші фотографії:")
        for file_id in photos:
            keyboard = user_kb.get_delete_photo_keyboard(str(os.path.basename(file_id))[:58])
            try:
                await bot.send_photo(chat_id=callback.from_user.id, photo=file_id, reply_markup=keyboard)
            except:
                await bot.send_document(chat_id=callback.from_user.id, document=file_id, reply_markup=keyboard)
            await asyncio.sleep(1)
        await callback.message.answer("ℹ️ Ви можете видаляти фотографії за допомогою кнопки 'Видалити фотографію'.", reply_markup=user_kb.return_to_menu_kb)
    else:
        await callback.message.answer("❌ Ви не маєте жодної фотографії.", reply_markup=user_kb.return_to_menu_kb)
    await callback.answer()    

async def delete_photo_command(callback: types.CallbackQuery):
    await remove_previous_kb(callback)
    await mark_photo_deleted(callback)

    action, photo_path = callback.data.split(',')

    user_photos = db.get_file_ids_by_user_id(callback.from_user.id)
    try:
        for file_id in user_photos:
            if photo_path in file_id:
                db.delete_photo_by_file_id(file_id)
                success = True
                break
        if success:
            await callback.answer("✅ Фотографію видалено.")
        else:
            await callback.answer("❌ Фотографія видалена раніше.")
    except:
        await callback.answer("❌ Фотографія видалена раніше.")
    await callback.answer()

async def mark_photo_deleted(callback: types.CallbackQuery):
    try:
        await bot.edit_message_caption(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id,
            caption="❎ Фотографія видалена."
            )
    except MessageNotModified:
        pass