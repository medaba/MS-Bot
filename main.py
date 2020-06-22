# -*- coding: utf-8 -*-

import asyncio
import logging

from geopy.distance import distance

from aiogram import types
from aiogram.types import Message, ChatType
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import utils
import keyboards
import mailing
from form import Form
from database import AioSQLiteWrapper
from polls_ids import polls_id


logging.basicConfig(
    level=logging.INFO,
    filename='logger.log',
    filemode='a',
    format='%(asctime)s | %(name)s | %(levelname)-4s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

logger = logging.getLogger()

bot = Bot(token=config.token, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def startup(*args):
    try:
        await bot.send_message(chat_id=config.main_admin, text="База, я на связи ✅")
    except Exception as e:
        print(e)


async def shutdown(*args):
    try:
        await bot.send_message(chat_id=config.main_admin, text="Бот остановлен ❌")
    except Exception as e:
        print(e)


async def main_menu(m: Message):
    await m.answer(
        "Главное меню",
        reply_markup=keyboards.main_menu()
    )

    # Добавление юзера, или обнуление страниц.
    # Включение статуса active
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    try:
        await users_table.fetch_one(m.from_user.id)
        await users_table.set_user_active(m.from_user.id)
        await users_table.set_user_polls_page(m.from_user.id, 0)
    except:
        await users_table.add_row("(user_id, first_name, last_name, username)",
                                  f"({m.from_user.id}, '{m.from_user.first_name}', '{m.from_user.last_name}', '{m.from_user.username}')")
        print("Добавлен новый пользователь")



@dp.message_handler(ChatType.is_private, commands=['start'])
async def start(m: Message):
    await main_menu(m)


# @dp.message_handler(content_types=["any"])
# async def send_json(m: Message):
#     print("ok")
#     print(str(m.as_json()))
#     # answer = json.dumps(m, indent=2, ensure_ascii=False)
#     # print(answer)
#     await bot.send_message(
#         m.chat.id,
#         str(m.as_json())
#     )


@dp.message_handler(ChatType.is_private, text="👑 Главное меню")
async def show_main_menu(m: Message):
    await main_menu(m)


@dp.message_handler(ChatType.is_private, text=['🤖 О Боте'])
async def info(m: Message):
    await m.answer(
        "*Подробнее о боте* \n\n",
        reply_markup=keyboards.about_bot()
    )


@dp.message_handler(ChatType.is_private, text=["QR - ссылка на Бота"])
async def qr(m: Message):
    await m.answer_photo(
        photo="AgACAgIAAxkBAAIajF7nfZzd3qFJrxCXAgAB3AkcIwEJSwACtKwxG1rQQEst6R9PHqKCxin-HJUuAAMBAAMCAAN4AAN3bAACGgQ",
        caption=r"https://t.me/g35_robot",
        parse_mode="HTML"
    )


@dp.message_handler(ChatType.is_private, text=["Исходный код"])
async def source_code(m: Message):
    await m.answer(
        "https://github.com/medaba/MS-Bot"
    )


@dp.message_handler(ChatType.is_private, text=['🔗 Ссылки'])
async def links(m: Message):
    await m.answer(
        "*Полезные ссылки* 🍀 \n\n"
        "*Telegram-каналы*: \n\n"
        "🔸 [Библиотека склерозника](https://t.me/biblioteka_skleroznika), "
        "куда регулярно выкладываются статьи, книги и видео по РС и о здоровье в целом.\n\n"
        "🔸 [Рассеянный склероз](https://t.me/msneurol) - телеграм-энциклопедия по РС.\n\n"
        "*Прочее*: \n\n"
        "🔸 [Калькулятор EDSS](http://edss.neurol.ru/edss_ru/) - онлайн калькулятор "
        "для оценки степени инвалидизации больных РС. Версия для врачей неврологов.\n\n"
        "🔸 [МосОРС](http://mosors.ru/) - сайт московского РС-сообщества.\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(ChatType.is_private, text=['♥️ Реабилитация'])
async def rehab(m: Message):
    await m.answer(
        "*Упражнения для реабилитации. Курс молодого бойца* ️🤺️\n\n"
        "Упражнения, рекомендуемые при рассеянном склерозе, "
        "позволяют замедлить прогрессирование процесса и заметно улучшить общее состояние. \n\n\n"
        "🔸 Упражнение с веревкой: "
        "[Пошаговая инструкция (YouTube)](https://www.youtube.com/watch?v=isWWtIwdiQE)\n\n"
        "🔸 Развитие мелкой моторики пальцев: "
        "[YouTube/ENG](https://www.youtube.com/watch?v=sB4lXUhRfMU&feature=youtu.be)\n\n"
        "🔸 10 упражнений для стоп: [сайт/текст с картинками](https://mednew.site/sport/10-uprazhnenij-dlya-stop)\n\n"
        "🔸 Упражнения на координацию из программы подготовки летчиков: [видео](https://t.me/mscler/39573)\n\n"
        "🔸 Курс упражнений для вестибулярного аппарата: "
        "[сайт/текст с картинками](https://vladmedicina.ru/persons/p52698.htm)\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(ChatType.is_private, text=['📜 Опросы'])
async def polls(m: Message):
    await m.answer(
        "⚠️ ВНИМАНИЕ. Далее идёт блок опросов для пациентов c Рассеянным склерозом \n\n"
        "Если болеете не вы, а ваш близкий, то допускается голосование от его лица. \n\n"
        "Вы всегда можете отменить свой голос и переголосовать заново\n\n\n"
        "Для перехода к началу опросов нажмите 'Вперед >>'",
        reply_markup=keyboards.polls_navigation()
    )


@dp.message_handler(ChatType.is_private, text=['🧑‍⚕️ РС-Центры'])
async def main_msc(m: Message):
    await m.answer(
        "Данное меню поможет вам найти ближайший медицинский центр",
        reply_markup=keyboards.msc()
    )


@dp.message_handler(ChatType.is_private, text=['🌍 Все центры'])
async def show_all_msc(m: Message):
    await m.answer(
        "*Список Центров Рассеянного Склероза* \n\n"
        '[telegra.ph](https://telegra.ph/Spisok-RS-Centrov-06-08-19) | '
        '[зеркало](https://tgraph.io/Spisok-RS-Centrov-06-08-19)'
    )


# TODO переписать ф-ю. Вынести вычисление расстояния в отдельный модуль

@dp.message_handler(ChatType.is_private, content_types=['location'])
async def proc_location(m: Message):
    user_coords = (m.location.latitude, m.location.longitude)  # координаты пользователя
    try:
        users_table = AioSQLiteWrapper("g35.sqlite", table_name="users")
        await users_table.save_location(m.from_user.id, user_coords)
    except Exception as e:
        print(e)

    mscenter_table = AioSQLiteWrapper("g35.sqlite", "mscenter")
    all_msc = await mscenter_table.fetch_all()   # список кортежей рс-центров из БД
    best_distance = 1000000                      # "максимально невозможное" расстояние от юзера до рсц
    best_address = None

    for msc in all_msc:
        msc_coords = (msc[4], msc[5])            # координаты текущего рс-центра
        dist = distance(user_coords, msc_coords) # получение расстояния от юзера, до рс-центра

        if dist < best_distance:
            best_distance = dist
            best_address = msc

    await bot.delete_message(
        m.chat.id,
        m.message_id
    )

    await bot.send_venue(
        m.chat.id,
        best_address[4],
        best_address[5],
        best_address[3],
        best_address[2]
    )

    await asyncio.sleep(1)

    answer = ", ".join(best_address[:4])
    await m.answer(
        "Ближайший от вас Центр Рассеянного Cклероза находится по адресу: \n\n"
        f"{answer} \n"
        f"Расстояние: {round(best_distance.km, 1)} км."
    )


@dp.message_handler(content_types=['contact'])
async def contact_proc(m: Message):
    users_table = AioSQLiteWrapper("g35.sqlite", table_name="users")
    await users_table.save_phone(m.from_user.id, m.contact.phone_number)


@dp.message_handler(ChatType.is_private, text=["Вперед >>"])
async def info(m: Message):
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    current_polls_page = await users_table.get_user_polls_page(m.from_user.id)
    next_page = current_polls_page + 1
    if next_page <= len(polls_id):
        poll_id = polls_id[next_page]
        await bot.forward_message(m.from_user.id, config.main_admin, poll_id)
        await users_table.set_user_polls_page(m.from_user.id, next_page)
    elif next_page > len(polls_id):
        await m.answer(
            "Конец блока опросов"
        )


@dp.message_handler(ChatType.is_private, text=["<< Назад"])
async def info(m: Message):
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    current_polls_page = await users_table.get_user_polls_page(m.from_user.id)
    previous_page = current_polls_page - 1
    if previous_page > 0:
        poll_id = polls_id[previous_page]
        await bot.forward_message(m.from_user.id, config.main_admin, poll_id)
        await users_table.set_user_polls_page(m.from_user.id, previous_page)


@dp.message_handler(ChatType.is_private, text=["⏮️ Начало опросов"])
async def info(m: Message):
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    await users_table.set_user_polls_page(m.from_user.id, 0)
    await polls(m)


@dp.message_handler(ChatType.is_private, commands=['mailing'])
async def start_mailing(m: Message):
    if m.from_user.id in config.admins:
        await Form.message_template.set()
        await m.answer(
            "Отправьте мне сообщение для рассылки",
            reply_markup=ReplyKeyboardRemove()
        )


@dp.message_handler(state=Form.message_template)
async def process_msg_template(m: Message, state: FSMContext):
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    all_users_ids = await users_table.get_all_users_ids()
    await mailing.start_mailing(admin_id=m.from_user.id,
                                users_ids=all_users_ids,
                                text=m.text)
    await state.finish()


@dp.message_handler(commands=['g35'])
async def say_to_g35(m: Message):
    """
    Сказать от имени бота в G35
    """
    text = utils.edit_cmd(m.text)
    await bot.send_message(
        config.matests,
        text
    )
    await bot.send_animation(
        chat_id=config.matests,
        animation="AAMCAgADGQEAAhqvXueMLoIs36dZrmU_cI1hrYoRBoQAAkMGAAKdpiFJRp2_h30a5ePbScoOAAQBAAdtAAO2fAACGgQ"
    )


@dp.message_handler(commands=['myid'])
async def my_id(m: Message):
    """
    Отправляет пользователю его ID в телеграме
    """
    await m.answer(
        "Ваш ID 👇 \n\n"
        f"`{m.from_user.id}`"
    )


@dp.message_handler(content_types=['animation'])
async def anima(m: Message):
    """
    Возвращает админу бота ID отправленного фото.
    """
    if m.from_user.id in config.admins:
        await m.answer(
            f"`{m}`",
            parse_mode=None
        )


@dp.message_handler(content_types=['photo'])
async def get_photo_id(m: Message):
    """
    Возвращает админу бота ID отправленного фото.
    """
    if m.from_user.id in config.admins:
        await m.answer(
            f"`{m.photo[-1]['file_id']}`",
            parse_mode=None
        )


async def i_am_alive(sleep_for=28800):
    """
    Периодическая ф-я.
    Добавляется в loop и запускается каждые 'sleep_for' секунд.
    Отправляет админу сообщение о своей работоспособности каждые 'sleep_for' секунд.
    """
    while True:
        await asyncio.sleep(sleep_for)  # Пауза. Цикл замирает на sleep_for секунд
        await bot.send_message(
            config.main_admin,
            "I am alive ",
            disable_notification=True
        )


if __name__ == '__main__':
    dp.loop.create_task(i_am_alive())

    if config.webhook is False:
        executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown, relax=0.5)
