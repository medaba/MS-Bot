# -*- coding: utf-8 -*-


import aiosqlite
import asyncio


class AioSQLiteWrapper:
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


    async def add_row(self, arguments, values):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""INSERT INTO {self.table_name}{arguments} VALUES {values}""")
            await db.commit()


    async def update_row(self, arg, new_value, where_arg, where_value):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET {arg} = {new_value} WHERE {where_arg} = {where_value}')
            await db.commit()


    async def fetch_user_by_id(self, user_id):
        """
        Получить данные юзера по user_id
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f"SELECT * FROM {self.table_name} WHERE user_id = {user_id}") as cursor:
                row = await cursor.fetchone()
                return dict(row)


    async def fetch_all(self):
        async with aiosqlite.connect(self.db_path) as db:
            return await db.execute_fetchall(f"""SELECT * FROM {self.table_name}""")


    async def fetch_all_active_users(self):
        async with aiosqlite.connect(self.db_path) as db:
            return await db.execute_fetchall(f"""SELECT * FROM users WHERE active=1""")


    async def fetch_all_ids(self):
        async with aiosqlite.connect(self.db_path) as db:
            return await db.execute_fetchall(f"""SELECT user_id FROM {self.table_name}""")


    async def get_all_users_ids(self, all_users) -> list:
        """
        Получить список всех user_id
        """
        users_ids = [x[0] for x in all_users]
        return users_ids


    async def save_location(self, user_id, lat_lon):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"UPDATE {self.table_name} SET latitude = {lat_lon[0]} WHERE user_id = {user_id}")
            await db.execute(f"UPDATE {self.table_name} SET longitude = {lat_lon[1]} WHERE user_id = {user_id}")
            await db.commit()


    async def save_phone(self, user_id, phone):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET phone = {phone} WHERE user_id = {user_id}')
            await db.commit()


    async def save_last_msg_id(self, user_id, message_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET msg_id = {message_id} WHERE user_id = {user_id}')
            await db.commit()


    async def get_saved_message_id(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f"SELECT * FROM {self.table_name} WHERE user_id = {user_id}") as cursor:
                row = await cursor.fetchone()
                return row['msg_id']

    async def set_user_active(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET active = 1 WHERE user_id = {user_id}')
            await db.commit()


    async def set_user_inactive(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET active = 0 WHERE user_id = {user_id}')
            await db.commit()


    async def get_user_polls_page(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f"SELECT * FROM {self.table_name} WHERE user_id = {user_id}") as cursor:
                row = await cursor.fetchone()
                return row['polls_page']


    async def set_user_polls_page(self, user_id, polls_page):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET polls_page = {polls_page} WHERE user_id = {user_id}')
            await db.commit()



if __name__ == '__main__':
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    ids = asyncio.run(users_table.fetch_all_active_users())
    print(ids)
