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


    # @staticmethod
    # async def migrate_mcs_table_from_site_to_db():
    #     """Заполняет таблицу
    #     """
    #     bs = BS()
    #     site_table = bs.create_mscenters_list()
    #
    #     async with aiosqlite.connect("g35.sqlite") as db:
    #         for item in site_table:
    #             await db.execute("""INSERT INTO mscenter(country, city, title, address) VALUES (?, ?, ?, ?)""",
    #                              parameters=item)
    #         await db.commit()



class AioSQLiteWrapper:
    """Класс для работы с aiosqlite
    """

    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name

    async def create_table(self, arguments: tuple):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name}{arguments}""")

    async def add_new_row(self, arguments: tuple, values: tuple):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""INSERT INTO {self.table_name}{arguments} VALUES {values}""")
            await db.commit()

    async def fetch_one(self):
        pass

    async def fetch_all(self):
        async with aiosqlite.connect(self.db_path) as db:
            return await db.execute_fetchall(f"""SELECT * FROM {self.table_name}""")




if __name__ == '__main__':
    a = AioSQLiteWrapper("matest.db", "tests")


    loop = asyncio.get_event_loop()
    # print(loop.run_until_complete(a.get_all_msc()))
    # loop.run_until_complete(a.create_table(("one", "two", "three")))
    r = loop.run_until_complete(a.fetch_all())
    print(r)
    # loop.run_until_complete(a.add_new_row(("one", "two", "three"), ("boom", "bam", "bom")))

