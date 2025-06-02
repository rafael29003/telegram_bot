from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_main_menu(lang: str = 'rus') -> InlineKeyboardMarkup:
    """Главное меню"""
    prof = {
        'rus': InlineKeyboardButton('🏠 Профиль', callback_data='prof'),
        'tat': InlineKeyboardButton('🏠 Профиль', callback_data='prof')
    }
    inline_btn_1 = {
        'rus': InlineKeyboardButton('📚 Список всех книг', callback_data='list_of_all'),
        'tat': InlineKeyboardButton('📚 Барлык китаплар исемлеге', callback_data='list_of_all')
    }
    inline_btn_3 = {
        'rus': InlineKeyboardButton('🔎 Книги по жанрам', callback_data='genres'),
        'tat': InlineKeyboardButton('🔎 Жанр буенча китаплар', callback_data='genres')
    }
    close = {
        'rus': InlineKeyboardButton('❌ Закрыть', callback_data='close'),
        'tat': InlineKeyboardButton('❌ Ябырга', callback_data='close')
    }

    return InlineKeyboardMarkup(row_width=1).add(
        prof[lang],
        inline_btn_1[lang],
        inline_btn_3[lang],
        close[lang]
    )

def get_book_keyboard(book_id: int, amount: int, lang: str = 'rus') -> InlineKeyboardMarkup:
    """Клавиатура для книги"""
    more = {
        'rus': InlineKeyboardButton('Подробнее 🧐', callback_data=f'more_{book_id}'),
        'tat': InlineKeyboardButton('Тәфсилле 🧐', callback_data=f'more_{book_id}')
    }
    take = {
        'rus': InlineKeyboardButton('🤲🏻 Взять', callback_data=f'date_choose_{book_id}'),
        'tat': InlineKeyboardButton('🤲🏻 Алырга', callback_data=f'date_choose_{book_id}')
    }
    hurry = {
        'rus': InlineKeyboardButton('🚴‍♀️ Поторопить', callback_data=f"date_choose_{book_id}"),
        'tat': InlineKeyboardButton('🚴‍♀️ Ашыктыру', callback_data=f"date_choose_{book_id}")
    }

    kb = InlineKeyboardMarkup(row_width=2)
    if amount > 0:
        kb.add(take[lang], more[lang])
    else:
        kb.add(hurry[lang], more[lang])
    return kb

def get_phone_request_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура запроса телефона"""
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton('Поделиться своим номером ☎️', request_contact=True)
    )

def get_navigation_keyboard(lang: str = 'rus') -> ReplyKeyboardMarkup:
    """Клавиатура навигации по списку книг"""
    if lang == 'rus':
        return ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
            KeyboardButton('⬅️ Назад'),
            KeyboardButton('Дальше ➡️'),
            KeyboardButton('Вернуться в главное меню 🏘')
        )
    else:
        return ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
            KeyboardButton('⬅️ Артка'),
            KeyboardButton('Алга ➡️'),
            KeyboardButton('Баш менюне ачырга 🏘')
        ) 