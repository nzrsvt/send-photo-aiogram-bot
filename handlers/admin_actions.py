from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import asyncio

from additional_functions import remove_previous_kb
import db_operations as db
from create_bot import bot
from keyboards import admin_kb

class AdminAdding(StatesGroup):
    username = State()

class UserSelecting(StatesGroup):
    username = State()

async def add_admin_command(callback : types.CallbackQuery):
    await AdminAdding.username.set()
    await remove_previous_kb(callback)
    await callback.message.answer("Введіть ім'я користувача якому потрібно надати права адміністратора: (наприклад @nzrsvt)")
    await callback.answer() 

async def process_username(message: types.Message, state: FSMContext):
    try:
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention':
                    username = message.text[1:][entity.offset:entity.offset + entity.length]
        else:
            username = message.text
        if db.check_user_existence_by_username(username):
            if db.check_is_admin_by_username(username):
                await message.answer(f"❌ Користувач {username} вже є адміністратором.")
                await message.answer('🔸 Оберіть наступну дію:', reply_markup=admin_kb.action_choose_kb)
            else:
                db.set_as_admin(username)
                await message.answer(f"✅ Користувача {username} успішно встановлено адміністратором!")
                await message.answer('🔸 Оберіть наступну дію:', reply_markup=admin_kb.action_choose_kb)
        else:
            await message.answer(f"❌ Користувач {username} ще не працював з ботом.")
            await message.answer('🔸 Оберіть наступну дію:', reply_markup=admin_kb.action_choose_kb)
        await state.finish()
    except Exception as e:
        await message.answer(f"⚠️ Виникла помилка {e} при обробці запиту.")
        await state.finish()
    
async def user_list_command(callback : types.CallbackQuery):
    await remove_previous_kb(callback) 
    users = db.get_all_users()
    if users:
        user_list = ""
        for user in users:
            if len(user_list) > 4000:
                await callback.message.answer(user_list)
                user_list = ""
            user_list = user_list + f"tg: @{user[2]} - inst: @{user[4]}\n"
        await callback.message.answer(user_list)
    else:
        await callback.message.answer("❌ Неможливо отримати список користувачів.")
    await callback.message.answer('🔸 Оберіть наступну дію:', reply_markup=admin_kb.action_choose_kb)
    await callback.answer()

async def select_user_command(callback : types.CallbackQuery):
    await UserSelecting.username.set()
    await remove_previous_kb(callback)
    await callback.message.answer("Введіть ім'я користувача фотографії якого потрібно переглянути: (формату @username)")
    await callback.answer() 

async def send_user_photos(message: types.Message, state: FSMContext):
    try:
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention':
                    username = message.text[1:][entity.offset:entity.offset + entity.length]
        else:
            username = message.text
        if db.check_user_existence_by_username(username):
            photos = db.get_file_ids_by_user_id(db.get_user_id_by_username(username))
            if photos:
                instagram_nickname = db.get_instagram_nickname_by_username(username)
                await message.answer(f"📌 Усі фотографії обраного користувача: (inst: {instagram_nickname})")
                for file_id in photos:
                    if len(file_id) == 82:
                        await bot.send_photo(chat_id=message.chat.id, photo=file_id)
                    else:
                        await bot.send_document(chat_id=message.chat.id, document=file_id)
                    await asyncio.sleep(1)
            else:
                await message.answer("❌ Користувач не завантажив жодної фотографії.")
            await message.answer('🔸 Оберіть наступну дію:', reply_markup=admin_kb.action_choose_kb)
        else:
            await message.answer(f"❌ Користувач @{username} ще не працював з ботом.")
            await message.answer('🔸 Оберіть наступну дію:', reply_markup=admin_kb.action_choose_kb)
        await state.finish()
    except Exception as e:
        await message.answer(f"⚠️ Виникла помилка {e} при обробці запиту.")
        await state.finish()