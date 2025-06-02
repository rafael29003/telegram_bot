from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура администратора"""
    see_debtor = KeyboardButton('Посмотреть должников 👀')
    add_book = KeyboardButton('Добавить новую книгу 🔄')
    return ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(see_debtor, add_book)

def get_book_confirmation_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура подтверждения добавления книги"""
    return ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
        KeyboardButton('Да ✅'),
        KeyboardButton('Нет ❌')
    )

def get_trade_confirmation_keyboard(trade_id: int) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения выдачи книги"""
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton('✅ Выдать книгу', callback_data=f'tradeyes_{trade_id}'),
        InlineKeyboardButton('❌ Отказать', callback_data=f'tradeno_{trade_id}')
    )
    return kb

def get_return_confirmation_keyboard(trade_id: int) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения возврата книги"""
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton('✅ Принять книгу', callback_data=f'tradefinish_{trade_id}_yes'),
        InlineKeyboardButton('❌ Отказать', callback_data=f'tradefinish_{trade_id}_no')
    )
    return kb 