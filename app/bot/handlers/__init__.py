from aiogram import Dispatcher

from .admin_handlers import register_admin_handlers
from .user_handlers import register_user_handlers
from .common_handlers import register_common_handlers

def register_all_handlers(dp: Dispatcher):
    handlers = (
        register_common_handlers,
        register_user_handlers,
        register_admin_handlers,
    )
    for handler in handlers:
        handler(dp) 