from aiogram import Dispatcher

from .is_admin import AdminFilter
from .is_private import PrivateChatFilter
from .not_admin import NotAdminFilter
from .answer_to_user import AnswerToUserFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(NotAdminFilter)
    dp.filters_factory.bind(PrivateChatFilter)
    dp.filters_factory.bind(AnswerToUserFilter)
