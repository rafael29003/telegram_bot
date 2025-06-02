from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from app.bot.keyboards.user_keyboards import (
    get_main_menu, get_book_keyboard, 
    get_phone_request_keyboard, get_navigation_keyboard
)
from app.bot.states.user_states import Login, SeeBook
from app.database.models import User, Book, Trade

import datetime

async def process_login(message: types.Message, state: FSMContext):
    """Обработка ввода имени и класса при регистрации"""
    login = message.text.split()
    
    if len(login) != 3 or not login[0].isalpha() or not login[1].isalpha():
        await message.answer(
            'Видимо вы ошиблись в введённых данных. 😔\n'
            'Напоминаю, что необходимо ввести своё имя, фамилию и класс через пробел в формате *Иван Иванов 10А.*',
            parse_mode=types.ParseMode.MARKDOWN
        )
        return

    async with state.proxy() as data:
        data['login'] = login
    
    await message.answer(
        f"Отлично, {login[1]}️. ☺\n"
        "Осталось отправить свой номер телефона. Для этого нажмите кнопку ниже.️",
        reply_markup=get_phone_request_keyboard()
    )
    await Login.phone.set()

async def process_phone(message: types.Message, state: FSMContext):
    """Обработка получения номера телефона при регистрации"""
    if not message.contact:
        await message.answer("Пожалуйста, воспользуйтесь кнопкой для отправки номера телефона.")
        return

    data = await state.get_data()
    login = data.get('login')
    
    session = message.bot.get("db_session")()
    new_user = User()
    new_user.tg_id = message.chat.id
    new_user.name = login[1]
    new_user.surname = login[0]
    new_user.clas = login[2]
    new_user.phone = message.contact.phone_number
    new_user.role = 'user'
    new_user.hurry = 0
    new_user.xp = 0
    
    session.add(new_user)
    session.commit()
    
    await state.finish()
    text = {'rus': 'Здравствуйте', 'tat': 'Исэнмесез'}
    await message.answer(
        f"{text[new_user.lang]}, {new_user.name} ✌️",
        reply_markup=get_main_menu(new_user.lang)
    )

async def process_book_list(callback: types.CallbackQuery):
    """Обработка кнопки просмотра списка книг"""
    await callback.answer('Выберете тип книг из списка ниже ⬇️')
    
    session = callback.bot.get("db_session")()
    user = session.query(User).filter(User.tg_id == callback.message.chat.id).first()
    
    text = {
        'rus': 'Какие книги вы хотите увидеть?',
        'tat': 'Нинди китаплар сез күрергә теләсәгез?'
    }
    
    # Создаем клавиатуру для выбора типа книг
    kb = types.InlineKeyboardMarkup(row_width=1)
    buttons = {
        'rus': [
            ('📖 Свободные книги', 'fr_book'),
            ('🔓 Все книги', 'al_book'),
            ('🏘 Вернуться в главное меню', 'menu')
        ],
        'tat': [
            ('📖 Ирекле китаплар', 'fr_book'),
            ('🔓 Барлык китаплар', 'al_book'),
            ('🏘 Баш менюне ачырга', 'menu')
        ]
    }
    
    for text, callback_data in buttons[user.lang]:
        kb.add(types.InlineKeyboardButton(text, callback_data=callback_data))
    
    await callback.message.edit_text(
        text[user.lang],
        reply_markup=kb,
        parse_mode=types.ParseMode.MARKDOWN
    )

async def show_books(message: types.Message, books: list, user: User):
    """Вспомогательная функция для отображения списка книг"""
    count = 0
    text = {
        'rus': 'Используйте клавиатуру для перелистывания 😉',
        'tat': 'Эзләү өчен клавиатураны кулланыгыз 😉'
    }
    
    main_message = await message.answer(
        text[user.lang],
        reply_markup=get_navigation_keyboard(user.lang)
    )
    
    for book in books[:3]:  # Показываем только первые 3 книги
        count += 1
        book_message = await message.answer(
            f"{count} - *Название:* {book.name}\n"
            f"*      Жанр:* {book.genre}\n"
            f"*      Автор:* {book.author}",
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=get_book_keyboard(book.book_id, int(book.amount), user.lang)
        )
        
        # Сохраняем ID сообщений для последующей навигации
        if count == 1:
            user.one = book_message.message_id
        elif count == 2:
            user.two = book_message.message_id
        elif count == 3:
            user.three = book_message.message_id
    
    user.mainMes = main_message.message_id
    user.ziro = str(count)
    user.page = '1'

async def process_free_books(callback: types.CallbackQuery):
    """Обработка кнопки просмотра свободных книг"""
    await callback.answer('Загружаем свободные книги 🔍')
    
    session = callback.bot.get("db_session")()
    user = session.query(User).filter(User.tg_id == callback.message.chat.id).first()
    books = session.query(Book).filter(Book.amount != 0).filter(Book.amount != '0').all()
    
    user.fre = True
    await callback.message.delete()
    await show_books(callback.message, books, user)
    
    session.add(user)
    session.commit()

async def process_all_books(callback: types.CallbackQuery):
    """Обработка кнопки просмотра всех книг"""
    await callback.answer('Загружаем список всех книг 🔎')
    
    session = callback.bot.get("db_session")()
    user = session.query(User).filter(User.tg_id == callback.message.chat.id).first()
    books = session.query(Book).all()
    
    user.fre = False
    await callback.message.delete()
    await show_books(callback.message, books, user)
    
    session.add(user)
    session.commit()

def register_user_handlers(dp):
    """Регистрация обработчиков пользовательских команд"""
    dp.register_message_handler(process_login, state=Login.login)
    dp.register_message_handler(process_phone, content_types=ContentType.CONTACT, state=Login.phone)
    dp.register_callback_query_handler(process_book_list, lambda c: c.data == "list_of_all")
    dp.register_callback_query_handler(process_free_books, lambda c: c.data == "fr_book")
    dp.register_callback_query_handler(process_all_books, lambda c: c.data == "al_book") 