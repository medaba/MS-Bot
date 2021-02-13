from aiogram.dispatcher.filters.state import StatesGroup, State


class MailingForm(StatesGroup):
    mail_msg = State()


class MsgToAdminForm(StatesGroup):
    msg_to_admin = State()


class AnswerToUserForm(StatesGroup):
    answer = State()