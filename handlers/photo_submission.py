from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import bot
import db_operations as db

class PhotoSubmission(StatesGroup):
    photo = State()
    nickname = State()

async def submit_photo_command(message: types.Message):
    await PhotoSubmission.photo.set()
    await message.answer("Надішліть свою фотографію.")

async def process_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data['photo'] = message.photo[-1].file_id

    # file_path = await bot.get_file(photo_file_id)
    # downloaded_file = await bot.download_file(file_path.file_path)
    # photo_path = f"photos/{message.chat.id}_{photo_file_id}.jpg"  
    # with open(photo_path, 'wb') as new_file:
    #     new_file.write(downloaded_file.read())

    # db.update_user_photo_path(message.chat.id, photo_path)

    # await state.update_data(photo_path=photo_path)
    await message.answer("Фотографію збережено. Тепер введіть свій Instagram-нікнейм.")
    await PhotoSubmission.next()

async def process_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data['nickname'] = message.text
    await handle_user_sending(state, message.chat.id)
    await state.finish()
    await message.answer(f"{message.from_user.full_name}, фотографію надіслано успішно!")

async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Операція скасована.")

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