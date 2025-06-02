from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboards.user_keyboards import get_main_menu
from app.database.models import User

async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    session = message.bot.get("db_session")()
    user = session.query(User).filter(User.tg_id == message.chat.id).first()
    
    if user:
        text = {'rus': 'Здравствуйте', 'tat': 'Исэнмесез'}
        await message.answer(f"{text[user.lang]}, {user.name} ✌️",
                           reply_markup=get_main_menu(user.lang))
    else:
        await message.answer(
            "Привет! 👋\nДля продолжения необходимо указать свои данные\n"
            "В следущем сообщении введите своё имя, фамилию и класс через пробел в формате *Иванов Иван 10А.*",
            parse_mode=types.ParseMode.MARKDOWN
        )
        await Login.login.set()

async def close_callback(callback: types.CallbackQuery):
    """Обработчик кнопки закрытия"""
    await callback.message.delete()

def register_common_handlers(dp: Dispatcher):
    """Регистрация общих обработчиков"""
    dp.register_message_handler(cmd_start, commands=["start"], state="*")
    dp.register_callback_query_handler(close_callback, lambda c: c.data == "close", state="*") 