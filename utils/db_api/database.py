# -*- coding: utf-8 -*-


import aiosqlite
import asyncio


class Database:
    """Класс для работы с aiosqlite
       Принимает путь в файлу БД и имя таблицы.
       Возвращает объект для работы с этой таблицей.
    """

    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name


    async def create_table(self, arguments):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name}{arguments}""")
            await db.commit()


    async def add_user(self, user_id, fullname, username, active=1):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                f"""INSERT INTO {self.table_name}(user_id, fullname, username, active) 
                VALUES(?, ?, ?, ?)""", parameters=(user_id, fullname, username, active))
            await db.commit()


    async def update_user(self, arg, value, where_arg, where_value):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"UPDATE {self.table_name} SET {arg}=? WHERE {where_arg}=?",
                             parameters=(value, where_value))
            await db.commit()


    async def fetch_user_by_id(self, user_id):
        """
        Получить данные юзера по user_id
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f"SELECT * FROM {self.table_name} WHERE user_id=?", parameters=(user_id,)) as cursor:
                row = await cursor.fetchone()
                return dict(row)


    async def fetch_all(self):
        async with aiosqlite.connect(self.db_path) as db:
            return await db.execute_fetchall(f"""SELECT * FROM {self.table_name}""")


    async def fetch_all_active_users(self):
        async with aiosqlite.connect(self.db_path) as db:
            lst_ids_tuples = await db.execute_fetchall(f"""SELECT user_id FROM users WHERE active=1""")
            ids = [user_id[0] for user_id in lst_ids_tuples]
            return ids


    async def fetch_all_ids(self):
        async with aiosqlite.connect(self.db_path) as db:
            return await db.execute_fetchall(f"""SELECT user_id FROM {self.table_name}""")


    async def save_location(self, user_id, lat_lon: iter):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"UPDATE {self.table_name} SET latitude=? WHERE user_id=?",
                             parameters=(lat_lon[0], user_id))
            await db.execute(f"UPDATE {self.table_name} SET longitude=? WHERE user_id=?",
                             parameters=(lat_lon[1], user_id))
            await db.commit()


    async def save_phone(self, user_id, phone):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET phone=? WHERE user_id=?', parameters=(phone, user_id))
            await db.commit()


    async def save_last_msg_id(self, user_id, message_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET msg_id=? WHERE user_id=?',
                             parameters=(message_id, user_id))
            await db.commit()


    async def get_saved_message_id(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f"SELECT msg_id FROM {self.table_name} WHERE user_id=?",
                                  parameters=(user_id,)) as cursor:
                msg_id = await cursor.fetchone()
                return msg_id[0]


    async def activate_user(self, user_id):
        await self.update_user(arg="active", value=1, where_arg="user_id", where_value=user_id)


    async def deactivate_user(self, user_id):
        await self.update_user(arg="active", value=0, where_arg="user_id", where_value=user_id)


    async def get_user_polls_page(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f"SELECT polls_page FROM {self.table_name} WHERE user_id=?",
                                  parameters=(user_id,)) as cursor:
                polls_page = await cursor.fetchone()
                return polls_page[0]


    async def set_user_polls_page(self, user_id, polls_page):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET polls_page=? WHERE user_id=?',
                             parameters=(polls_page, user_id))
            await db.commit()



if __name__ == '__main__':
    users_table = Database("data/g35.sqlite", "users")
    print(asyncio.run(users_table.fetch_all_active_users()))
