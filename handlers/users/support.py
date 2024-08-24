# from aiogram import types
# from aiogram.dispatcher.filters import Command
# from aiogram.dispatcher import FSMContext
# from data.config import ADMINS
# from keyboards.inline.support import support_keyboard, support_callback
# from loader import dp, bot


# @dp.message_handler(Command("chat"))
# async def ask_support(message: types.Message):
#     if message.from_user.id in ADMINS:
#         await message.answer("Assalom alaykum boss!")
#         return
#     text = "Xabar yubormoqchimisiz? Quyidagi tugmani bosing!"
#     keyboard = await support_keyboard(messages="one") 
#     await message.answer(text, reply_markup=keyboard)
    
# @dp.callback_query_handler(support_callback.filter(messages="one"))
# async def send_to_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
#     await call.answer()
#     user_id = int(callback_data.get("user_id"))

#     await call.message.answer("Yubormoqchi bo'lgan xabaringizni yozing")
#     await state.set_state("wait_for_support_message")
#     await state.update_data(second_id=user_id)
    
# @dp.message_handler(state="wait_for_support_message", content_types=types.ContentType.ANY)
# async def get_support_message(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     second_id = data.get("second_id")
    
#     await bot.send_message(second_id,
#                            f"Sizga xat! Quyidagi tugmani bosish orqali javob berishingiz mumkin.,\n\nYuboruvchi: {message.from_user.full_name}\nUsername:  @{message.from_user.username}")
#     keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)
#     await message.copy_to(second_id, reply_markup=keyboard)
    
#     await message.answer("Sizni xabarnigiz yuborildi!")
#     await state.reset_state()
    


from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.inline.support import support_keyboard, support_callback
from loader import dp, bot


@dp.message_handler(Command("chat"))
async def ask_support(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer("Assalom alaykum boss!")
        return
    text = "Xabar yubormoqchimisiz? Quyidagi tugmani bosing!"
    keyboard = await support_keyboard(messages="one")
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="one"))
async def send_to_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    user_id = int(callback_data.get("user_id"))

    await call.message.answer("Yubormoqchi bo'lgan xabaringizni yozing")
    await state.set_state("wait_for_support_message")
    await state.update_data(second_id=user_id)


@dp.message_handler(state="wait_for_support_message", content_types=types.ContentType.ANY)
async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    # Check if the recipient is an admin
    if second_id in ADMINS:
        info_message = (
            f"Sizga xat! Quyidagi tugmani bosish orqali javob berishingiz mumkin.,\n\n"
            f"Yuboruvchi: {message.from_user.full_name}\n"
            f"Username: @{message.from_user.username}"
        )
    else:
        info_message = "Sizga xat! Quyidagi tugmani bosish orqali javob berishingiz mumkin."

    # Send the appropriate message to the recipient
    await bot.send_message(second_id, info_message)

    # Send the user's message along with a keyboard to the recipient
    keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    # Inform the user that their message has been sent
    await message.answer("Sizning xabaringiz yuborildi!")
    
    # Reset the state
    await state.reset_state()
