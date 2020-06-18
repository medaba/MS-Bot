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


if __name__ == '__main__':
    pass
