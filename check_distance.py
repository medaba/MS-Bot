# -*- coding: utf-8 -*-

from geopy.distance import distance

from database import AioSQLiteWrapper


async def calculate_distance(user_coords):
    """
    Принимает координаты пользователя,
    Возвращает Дистанцию до ближайшего РСЦ из БД и его адрес.
    """
    mscenter_table = AioSQLiteWrapper("g35.sqlite", "mscenter")
    all_msc = await mscenter_table.fetch_all()  # список кортежей рс-центров из БД
    best_distance = 10 ** 10                    # "максимально невозможное" расстояние от юзера до рсц
    best_address = None

    for msc in all_msc:
        msc_coords = (msc[4], msc[5])             # координаты текущего рс-центра
        dist = distance(user_coords, msc_coords)  # получение расстояния от юзера, до рс-центра

        if dist < best_distance:
            best_distance = dist
            best_address = msc

    return best_distance, best_address