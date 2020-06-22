# -*- coding: utf-8 -*-


import aiosqlite
import asyncio


class AioSQL:
    """
    Класс для работы с БД sqlite3
    """

    @staticmethod
    async def create_table():
        async with aiosqlite.connect("g35.sqlite") as db:
            await db.execute(f"""CREATE TABLE IF NOT EXISTS users (
                                 user_id INTEGER UNIQUE NOT NULL DEFAULT 0,
                                 polls_page INTEGER DEFAULT 0)"""
                             )
            await db.execute("""CREATE TABLE IF NOT EXISTS mscenter(
                                country TEXT,
                                city TEXT,
                                title TEXT,
                                address TEXT,
                                latitude DECIMAL,
                                longitude DECIMAL)"""
                             )
            await db.commit()

    @staticmethod
    async def drop_table(table_name='users'):
        async with aiosqlite.connect("g35.sqlite") as db:
            await db.execute(f'DROP TABLE {table_name}')

    @staticmethod
    async def get_user_polls_page(user_id):
        async with aiosqlite.connect("g35.sqlite") as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f"SELECT * FROM users WHERE user_id = {user_id}") as cursor:
                row = await cursor.fetchone()
                return row['polls_page']

    @staticmethod
    async def add_user(user_id, polls_page):
        async with aiosqlite.connect("g35.sqlite") as db:
            await db.execute_insert(f"INSERT INTO users(user_id, polls_page) VALUES (?, ?)",
                                    parameters=[user_id, polls_page])
            await db.commit()

    @staticmethod
    async def update_user(user_id, polls_page):
        async with aiosqlite.connect("g35.sqlite") as db:
            await db.execute(f'UPDATE users SET polls_page = ? WHERE user_id = ?', parameters=[polls_page, user_id])
            await db.commit()

    @staticmethod
    async def get_all_msc():
        async with aiosqlite.connect("g35.sqlite") as db:
            all_msc = await db.execute_fetchall("SELECT * FROM mscenter")
            return all_msc


class AioSQLiteWrapper:
    """Класс для работы с aiosqlite
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


    async def fetch_one(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f"SELECT * FROM {self.table_name} WHERE user_id = {user_id}") as cursor:
                row = await cursor.fetchone()
                return dict(row)


    async def fetch_all(self):
        async with aiosqlite.connect(self.db_path) as db:
            return await db.execute_fetchall(f"""SELECT * FROM {self.table_name}""")


    async def fetch_all_ids(self):
        async with aiosqlite.connect(self.db_path) as db:
            return await db.execute_fetchall(f"""SELECT user_id FROM {self.table_name}""")


    async def get_all_users_ids(self) -> list:
        """
        Получить список всех user_id
        """
        users_ids = []
        try:
            all_users = await self.fetch_all()
            for user in all_users:
                users_ids.append(user[0])
        except Exception as e:
            print(e)
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


    async def set_user_active(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET active = 1 WHERE user_id = {user_id}')
            await db.commit()


    async def set_user_inactive(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET active = 0 WHERE user_id = {user_id}')
            await db.commit()


    @staticmethod
    async def get_user_polls_page(user_id):
        async with aiosqlite.connect("g35.sqlite") as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(f"SELECT * FROM users WHERE user_id = {user_id}") as cursor:
                row = await cursor.fetchone()
                return row['polls_page']


    async def set_user_polls_page(self, user_id, polls_page):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE {self.table_name} SET polls_page = {polls_page} WHERE user_id = {user_id}')
            await db.commit()


    async def drop_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""DROP TABLE IF EXISTS {self.table_name}""")




if __name__ == '__main__':
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    ids = asyncio.run(users_table.fetch_all_ids())
    print(ids[0][0])
