from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import bot
import db_operations as db
from keyboards import user_kb

class PhotoSubmission(StatesGroup):
    photo = State()
    nickname = State()

async def submit_photo_command(callback : types.CallbackQuery):
    await PhotoSubmission.photo.set()
    await callback.message.answer("Надішліть свою фотографію.")
    await callback.answer()

async def process_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            if message.photo:
                if message.photo[-1].file_size > 2 * 1024 * 1024:
                    await message.answer("🚫 Розмір фотографії перевищує 2МБ.")
                    await message.answer(
                        f"🖇 Якщо Ви бажаєте надіслати іншу фотографію, натисніть на кнопку нижче.", 
                        reply_markup=user_kb.send_kb
                        )
                else:
                    data['photo'] = message.photo[-1].file_id
                    await message.answer("Фотографію збережено. Тепер введіть свій Instagram-нікнейм.")
                    await PhotoSubmission.next()
            elif message.document:
                if message.document.file_size > 2 * 1024 * 1024:
                    await message.answer("🚫 Розмір фотографії перевищує 2МБ.")
                    await message.answer(
                        f"🖇 Якщо Ви бажаєте надіслати іншу фотографію, натисніть на кнопку нижче.", 
                        reply_markup=user_kb.send_kb
                        )
                else:
                    file_name = message.document.file_name.lower()
                    allowed_formats = ('.png', '.jpg', '.jpeg') 
                    if any(file_name.endswith(format) for format in allowed_formats):
                        data['photo'] = message.document.file_id
                        await message.answer("Фотографію збережено. Тепер введіть свій Instagram-нікнейм.")
                        await PhotoSubmission.next()
                    else:
                        await message.answer("🚫 Будь ласка, надішліть фотографію в іншому форматі.")
                        await message.answer(
                            f"🖇 Якщо Ви бажаєте надіслати іншу фотографію, натисніть на кнопку нижче.", 
                            reply_markup=user_kb.send_kb
                            )
            else:
                await message.answer("🚫 Будь ласка, надішліть фотографію в іншому форматі.")
                await message.answer(
                    f"🖇 Якщо Ви бажаєте надіслати іншу фотографію, натисніть на кнопку нижче.", 
                    reply_markup=user_kb.send_kb
                    )

async def process_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data['nickname'] = message.text
    await handle_user_sending(state, message.chat.id)
    await state.finish()
    await message.answer(f"✅ {message.from_user.full_name}, фотографію надіслано успішно!")
    await message.answer(
         f"ℹ️ Якщо Ви бажаєте скасувати надсилання фотографії, натисніть на кнопку нижче.", 
         reply_markup=user_kb.cancel_kb
         )

async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("🗑 Операція скасована.")
    await message.answer(
         f"🖇 Якщо Ви бажаєте надіслати іншу фотографію, натисніть на кнопку нижче.", 
         reply_markup=user_kb.send_kb
         )
    
async def cancel_photo_command(callback : types.CallbackQuery):
    db.delete_user_photo(callback.from_user.id)
    await callback.message.answer("🗑 Фотографію видалено успішно.")
    await callback.message.answer(
         f"🖇 Якщо Ви бажаєте надіслати іншу фотографію, натисніть на кнопку нижче.", 
         reply_markup=user_kb.send_kb
         )
    await callback.answer()

async def handle_user_sending(state, user_id):
    async with state.proxy() as data:
        file_path = await bot.get_file(data['photo'])
        print(file_path)
        downloaded_file = await bot.download_file(file_path.file_path)
        photo_path = f"photos/{user_id}_{data['photo']}.jpg"  
        with open(photo_path, 'wb') as new_file:
            new_file.write(downloaded_file.read())

        db.update_user_photo_path(user_id, photo_path)
        db.update_user_nickname(user_id, data['nickname'])
