from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot.keyboards.admin_keyboards import (
    get_admin_main_keyboard,
    get_book_confirmation_keyboard,
    get_trade_confirmation_keyboard,
    get_return_confirmation_keyboard
)
from app.bot.states.user_states import AddBook
from app.database.models import User, Book, Trade
from config import load_config

import datetime
import requests
from bs4 import BeautifulSoup

async def process_admin_command(message: types.Message):
    """Обработка команды активации админских прав"""
    config = load_config()
    if message.text == config.admin_code:
        session = message.bot.get("db_session")()
        user = session.query(User).filter(User.tg_id == message.chat.id).first()
        user.role = 'admin'
        session.add(user)
        session.commit()
        
        await message.answer(
            "Доброе время суток, теперь у вас есть права админа",
            reply_markup=get_admin_main_keyboard()
        )

async def process_add_book_command(message: types.Message):
    """Обработка команды добавления книги"""
    if message.text == 'Добавить новую книгу 🔄':
        await message.answer(
            'Начинаем процесс добавления книги 📘\n'
            'Если вы допустили ошибку, продолжите, в конце вы можете отменить операцию\n'
            'Напишите только *название* книги или отправьте ссылку на литрес.',
            parse_mode=types.ParseMode.MARKDOWN
        )
        await AddBook.name.set()

async def process_book_name(message: types.Message, state: FSMContext):
    """Обработка ввода названия книги"""
    name = message.text
    if 'litres.ru' in name:
        # Получаем информацию о книге по ссылке
        data = await get_book_info_from_litres(name)
        async with state.proxy() as state_data:
            state_data.update(data)
        await AddBook.amount.set()
        await message.answer('Напишите пожалуйста *количество* книг',
                           parse_mode=types.ParseMode.MARKDOWN)
    else:
        async with state.proxy() as data:
            data['name'] = name
        await AddBook.genre.set()
        await message.answer('Напишите пожалуйста *жанр* книги',
                           parse_mode=types.ParseMode.MARKDOWN)

async def process_book_genre(message: types.Message, state: FSMContext):
    """Обработка ввода жанра книги"""
    async with state.proxy() as data:
        data['genre'] = message.text
    await AddBook.author.set()
    await message.answer('Напишите пожалуйста *автора* книги',
                        parse_mode=types.ParseMode.MARKDOWN)

async def process_book_author(message: types.Message, state: FSMContext):
    """Обработка ввода автора книги"""
    async with state.proxy() as data:
        data['author'] = message.text
    await AddBook.description.set()
    await message.answer('Напишите пожалуйста *небольшое описание* для книги',
                        parse_mode=types.ParseMode.MARKDOWN)

async def process_book_description(message: types.Message, state: FSMContext):
    """Обработка ввода описания книги"""
    async with state.proxy() as data:
        data['description'] = message.text
    await AddBook.amount.set()
    await message.answer('Напишите пожалуйста *количество* книг',
                        parse_mode=types.ParseMode.MARKDOWN)

async def process_book_amount(message: types.Message, state: FSMContext):
    """Обработка ввода количества книг"""
    async with state.proxy() as data:
        data['amount'] = message.text
    await AddBook.sog.set()
    
    data = await state.get_data()
    await message.answer(
        f'Название книги: {data["name"]}\n\n'
        f'Жанр: {data["genre"]}\n\n'
        f'Автор: {data["author"]}\n\n'
        f'Описание: {data["description"]}\n\n'
        f'Количество книг: {data["amount"]}',
        reply_markup=get_book_confirmation_keyboard()
    )

async def process_book_confirmation(message: types.Message, state: FSMContext):
    """Обработка подтверждения добавления книги"""
    if message.text == 'Да ✅':
        session = message.bot.get("db_session")()
        new_book = Book()
        data = await state.get_data()
        
        new_book.name = data['name']
        new_book.genre = f"{data['genre'][0].upper()}{data['genre'][1:]}"
        new_book.author = data['author']
        new_book.description = data['description']
        new_book.amount = data['amount']
        
        session.add(new_book)
        session.commit()
        
        config = load_config()
        # Отправляем сообщение в канал о новой книге
        message_text = (
            f'Добавлена новая книга! 🎉\n\n'
            f'*{new_book.name}*\n\n'
            f'{new_book.description}\n\n'
            f'*Автор*: {new_book.author}\n'
            f'*Жанр*: {new_book.genre}\n\n'
            f'Взять книгу можно по [этой ссылке](https://t.me/SchoolLibraryLi1_bot?start=take_book_{new_book.book_id})'
        )
        
        channel_message = await message.bot.send_message(
            config.channel_id,
            message_text,
            parse_mode=types.ParseMode.MARKDOWN
        )
        
        new_book.link = f"https://t.me/lyceum_library/{channel_message.message_id}"
        new_book.mes_id = channel_message.message_id
        session.add(new_book)
        session.commit()
        
        await message.answer('Операция успешно выполнена',
                           reply_markup=get_admin_main_keyboard())
    else:
        await message.answer('Операция успешно отменена',
                           reply_markup=get_admin_main_keyboard())
    await state.finish()

async def process_see_debtors(message: types.Message):
    """Обработка команды просмотра должников"""
    if message.text == 'Посмотреть должников 👀':
        session = message.bot.get("db_session")()
        trades = session.query(Trade).filter(Trade.status == 'working').all()
        
        if not trades:
            await message.answer("Пока нет должников 👍")
            return
            
        debtors_text = ""
        for i, trade in enumerate(trades, 1):
            user = session.query(User).filter(User.tg_id == trade.user_id).first()
            debtors_text += (
                f"{i}. {user.name} {user.surname} {user.clas} "
                f"должен вам книгу {trade.book_name} +{user.phone}\n"
            )
        
        await message.answer(debtors_text)

async def get_book_info_from_litres(url: str) -> dict:
    """Получение информации о книге с сайта ЛитРес"""
    headers = {
        'authority': 'www.litres.ru',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    return {
        'name': soup.find('h1', itemprop="name").text[:-5],
        'author': soup.find('a', class_="biblio_book_author__link").text,
        'genre': soup.find('a', class_="biblio_info__link").text,
        'description': soup.find('div', itemprop="description").text
    }

def register_admin_handlers(dp):
    """Регистрация обработчиков админских команд"""
    dp.register_message_handler(process_admin_command, lambda m: m.text == load_config().admin_code)
    dp.register_message_handler(process_add_book_command, lambda m: m.text == 'Добавить новую книгу 🔄', state=None)
    dp.register_message_handler(process_see_debtors, lambda m: m.text == 'Посмотреть должников 👀', state=None)
    
    # Обработчики состояний добавления книги
    dp.register_message_handler(process_book_name, state=AddBook.name)
    dp.register_message_handler(process_book_genre, state=AddBook.genre)
    dp.register_message_handler(process_book_author, state=AddBook.author)
    dp.register_message_handler(process_book_description, state=AddBook.description)
    dp.register_message_handler(process_book_amount, state=AddBook.amount)
    dp.register_message_handler(process_book_confirmation, state=AddBook.sog) 