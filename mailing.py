# -*- coding: utf-8 -*-

import asyncio
from time import time

from main import bot, logger
from database import AioSQLiteWrapper


async def start_mailing(admin_id, users_ids, text):
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
                disable_web_page_preview=True
            )
            mailing_report['ok'] += 1
        except:
            failed_users_ids.append(user_id)
            logger.error(f"{user_id} MAILING FAILED")
            mailing_report['fail'] += 1

    end_time = time() - start_time
    end_time = round(end_time, 1)
    mailing_report["end_time"] = end_time

    await send_report_to_admin(admin_id, mailing_report)



async def send_report_to_admin(admin_id, mailing_report):
    """
    Отправка отчета админу о проведенной рассылке
    """
    await bot.send_message(
        admin_id,
        f"Рассылка завершена за {mailing_report['end_time']} секунд\n\n"
        f"Всего попыток: {mailing_report['count']}\n"
        f"Успешно отправлено: {mailing_report['ok']}\n"
        f"Неудача: {mailing_report['fail']}"
    )


async def inactive_users(failed_users_ids):
    """
    Принимает список user_id пользователей, которым не получилось отправить сообщение
    и устанавливает им в БД active=0
    """
    try:
        users_table = AioSQLiteWrapper("db.db", "users")
        for user in failed_users_ids:
            await users_table.set_user_inactive(user)
    except Exception as e:
        print(e)
        logger.error(e)