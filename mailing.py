# -*- coding: utf-8 -*-

import asyncio
from time import time

from main import bot, logger
from database import AioSQLiteWrapper

async def start_mailing(admin_id, users_ids, text):
    ok = 0
    fail = 0
    failed_users_ids = []
    start_time = time()

    for user_id in users_ids:
        await asyncio.sleep(0.1)
        try:
            await bot.send_message(
                user_id,
                text,
                disable_web_page_preview=True
            )
            ok += 1
        except:
            failed_users_ids.append(user_id)
            logger.error(f"{user_id} MAILING FAILED")
            fail += 1

    end_time = time() - start_time
    end_time = round(end_time, 1)

    await bot.send_message(
        admin_id,
        f"Рассылка завершена за {end_time} секунд\n\n"
        f"Успешно отправлено: {ok}\nНеудача: {fail}"
    )

    users_table = AioSQLiteWrapper("db.db", "users")

    for user in failed_users_ids:
        await users_table.set_user_inactive(user)
