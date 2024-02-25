from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import asyncio

from additional_functions import remove_previous_kb, get_user_photos
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
    
# async def manage_users_command(callback : types.CallbackQuery):
#     await remove_previous_kb(callback) 
#     users = db.get_all_users()
#     if users:
#         await callback.message.answer("📌 Всі ваші фотографії:")
#         for photo_path in photos:
#             with open(photo_path, 'rb') as photo_file:
#                 keyboard = user_kb.get_delete_photo_keyboard(str(os.path.basename(photo_path))[:58])
#                 await bot.send_photo(chat_id=callback.from_user.id, photo=photo_file, reply_markup=keyboard)
#                 await asyncio.sleep(1)
#         await callback.message.answer("ℹ️ Ви можете видаляти фотографії за допомогою кнопки 'Видалити фотографію'.", reply_markup=user_kb.return_to_menu_kb)
#     else:
#         await callback.message.answer("❌ Ви не маєте жодної фотографії.", reply_markup=user_kb.return_to_menu_kb)
#     await callback.answer()

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
            photos = await get_user_photos(db.get_user_id_by_username(username))
            if photos:
                await message.answer("📌 Усі фотографії обраного користувача:")
                for photo_path in photos:
                    with open(photo_path, 'rb') as photo_file:
                        await bot.send_document(chat_id=message.chat.id, document=photo_file)
                        await asyncio.sleep(1)
            else:
                await message.answer("❌ Користувач не завантажив фотографії.", reply_markup=user_kb.return_to_menu_kb)
            await message.answer('🔸 Оберіть наступну дію:', reply_markup=admin_kb.action_choose_kb)
        else:
            await message.answer(f"❌ Користувач {username} ще не працював з ботом.")
            await message.answer('🔸 Оберіть наступну дію:', reply_markup=admin_kb.action_choose_kb)
        await state.finish()
    except Exception as e:
        await message.answer(f"⚠️ Виникла помилка {e} при обробці запиту.")
        await state.finish()