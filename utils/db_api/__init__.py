# -*- coding: utf-8 -*-

from .database import Database

users_table = Database(db_path="data/g35.sqlite", table_name="users")
mscenter_table = Database(db_path="data/g35.sqlite", table_name="mscenter")