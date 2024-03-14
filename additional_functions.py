from aiogram import types
from create_bot import bot
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher import FSMContext
from keyboards import user_kb, admin_kb
import db_operations as db
import os
import shutil
from urllib.parse import urlparse

import magic

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
        db.set_as_not_admin_by_user_id(message.chat.id)
    else:
        db.set_as_admin_by_user_id(message.chat.id)

    await message.answer('🔸 Оберіть наступну дію:', 
                         reply_markup=user_kb.action_choose_kb if is_admin
                         else admin_kb.action_choose_kb
                         )

async def download_and_process_photos(user_id):
    users = db.get_all_users()
    archive_number = 0
    temp_folder = "temp"

    for user in users:
        if await get_folder_size(temp_folder) > 100 * 1024 * 1024: 
                await archive_and_send(temp_folder, archive_number, user_id)
                archive_number = archive_number + 1

        file_ids = db.get_file_ids_by_user_id(user[1])
        
        if file_ids:
            user_folder = os.path.join(temp_folder, str(user[4]))
            os.makedirs(user_folder, exist_ok=True)

            for file_id in file_ids:
                file_info = await bot.get_file(file_id)

                downloaded_file = await bot.download_file(file_info.file_path)

                file_path = os.path.join(user_folder, os.path.basename(file_info.file_path))

                with open(file_path, 'wb') as file:
                    file.write(downloaded_file.read())
    
    if os.path.exists(temp_folder) and os.path.isdir(temp_folder):
        await check_files_type(temp_folder)
        await archive_and_send(temp_folder, archive_number, user_id)
        shutil.rmtree(temp_folder)
    else: 
        return -1

async def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size

async def archive_and_send(temp_folder, archive_number, user_id):
    archive_path = f"archive_{archive_number}"
    shutil.make_archive(archive_path, 'zip', temp_folder)

    with open(f"{archive_path}.zip", "rb") as archive_file:
        await bot.send_document(chat_id=user_id, document=archive_file)

    os.remove(f"{archive_path}.zip")
    shutil.rmtree(temp_folder)
    os.makedirs(temp_folder, exist_ok=True)

async def detect_file_type(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type

async def check_files_type(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            filename, file_extension = os.path.splitext(file_path)
            if not file_extension:
                new_extension = await detect_file_type(file_path)
                new_extension = new_extension.split('/')[-1]
                new_filename = f"{filename}.{new_extension}"
                os.rename(file_path, new_filename)