from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from additional_functions import remove_previous_kb
import db_operations as db
from create_bot import bot
from keyboards import admin_kb

class AdminAdding(StatesGroup):
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