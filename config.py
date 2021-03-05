# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

BOTUSERNAME = os.getenv("BOTUSERNAME")
TOKEN = os.getenv("TOKEN")
CREATOR = os.getenv("CREATOR")
MAIN_ADMIN = os.getenv("MAIN_ADMIN")

ADMINS = os.getenv("ADMINS").split(':')
ADMINS = [int(user_id) for user_id in ADMINS]

MS_CENTERS = "https://telegra.ph/Spisok-RS-Centrov-03-05"
