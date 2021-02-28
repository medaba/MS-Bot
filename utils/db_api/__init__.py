# -*- coding: utf-8 -*-

from .database import Database, fetch_all_city_names

users_table = Database(db_path="data/g35.sqlite", table_name="users")
mscenter_table = Database(db_path="data/g35.sqlite", table_name="mscenter")

all_city_names = fetch_all_city_names()
