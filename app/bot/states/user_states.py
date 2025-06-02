from aiogram.dispatcher.filters.state import StatesGroup, State

class Login(StatesGroup):
    login = State()
    phone = State()

class AddBook(StatesGroup):
    name = State()
    genre = State()
    author = State()
    description = State()
    amount = State()
    sog = State()

class SeeBook(StatesGroup):
    al = State()
    genre = State() 