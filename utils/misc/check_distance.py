# -*- coding: utf-8 -*-

from geopy.distance import distance

from utils.db_api import mscenter_table


async def calculate_distance(user_coords):
    """
    Принимает координаты пользователя,
    Возвращает Дистанцию от пользователя до ближайшего РСЦ из БД и адрес этого РСЦ.
    """
    all_msc = await mscenter_table.fetch_all()  # список кортежей рс-центров из БД
    best_distance = 999999999999999             # "максимально невозможное" расстояние от юзера до рсц
    best_address = None

    for msc in all_msc:
        msc_coords = (msc[4], msc[5])             # координаты текущего рс-центра
        dist = distance(user_coords, msc_coords)  # получение расстояния от юзера, до рс-центра

        if dist < best_distance:
            best_distance = dist
            best_address = msc

    return best_distance, best_address
