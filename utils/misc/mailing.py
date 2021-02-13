# -*- coding: utf-8 -*-

import asyncio
from time import time

from loader import bot
from utils.db_api import users_table


async def start_mailing(admin_id, users_ids, text):
    if text == "🚫 Отмена":
        await bot.send_message(admin_id, 'Рассылка отменена')
        return

    failed_users_ids = []
    mailing_report = {"end_time": None, "count": 0, "ok": 0, "fail": 0}

    start_time = time()
    for user_id in users_ids:
        mailing_report['count'] += 1
        await asyncio.sleep(0.1)
        try:
            await bot.send_message(
                user_id,
                text,
                parse_mode="HTML",
                disable_web_page_preview=True,
                disable_notification=True
            )
            mailing_report['ok'] += 1
        except Exception as e:
            print(f"{user_id}\n\n {e}\n\n")
            failed_users_ids.append(user_id)
            mailing_report['fail'] += 1

    end_time = time() - start_time
    end_time = round(end_time, 1)
    mailing_report["end_time"] = end_time

    await send_report_to_admin(admin_id, mailing_report)
    await process_inactive_users(failed_users_ids)


async def send_report_to_admin(admin_id, mailing_report):
    """
    Отправка админу отчета о проведенной рассылке
    """
    await bot.send_message(
        admin_id,
        f"Рассылка завершена за {mailing_report['end_time']} секунд\n\n"
        f"Всего попыток: {mailing_report['count']}\n"
        f"Успешно отправлено: {mailing_report['ok']}\n"
        f"Неудача: {mailing_report['fail']}")


async def process_inactive_users(failed_users_ids):
    """
    Принимает список user_id пользователей, которым не получилось отправить сообщение
    и устанавливает им в БД active=0
    """
    try:
        for user in failed_users_ids:
            await users_table.deactivate_user(user)
    except Exception as e:
        print(e)
