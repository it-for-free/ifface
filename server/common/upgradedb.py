# -*- coding: utf-8 -*-
#-----------------------------------------
# autor(s): Pavel Plotnikov (humanmashine)
#
# description: Модуль (утилита) для
#     создания и обновления базы данных.
# info: MIT License 
#       it-for-free 2014
#-----------------------------------------
import sqlite3

from server.iffconfig.settings import iff_settings

conn = sqlite3.connect(iff_settings['db_path'])
cur = conn.cursor()
#-----Create notes table-------
cur.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
timeutc INTEGER NOT NULL,
date TEXT NOT NULL,
title TEXT NOT NULL,
msg TEXT NOT NULL);''')
cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS time_id_notes ON notes (timeutc ASC);')
#-----Create some annonces table-------
cur.execute('''CREATE TABLE IF NOT EXISTS sannonce (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
timeutc INTEGER NOT NULL,
date TEXT NOT NULL,
title TEXT NOT NULL,
picname TEXT NOT NULL,
andate TEXT NOT NULL,
msg TEXT NOT NULL);''')
cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS time_id_sannonce ON sannonce (timeutc ASC);')
#-----Create news table-------
cur.execute('''CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
timeutc INTEGER NOT NULL,
date TEXT NOT NULL,
title TEXT NOT NULL,
picname TEXT NOT NULL,
msg TEXT NOT NULL);''')
cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS time_id_news ON news (timeutc ASC);')
#-----Create video annonces table-------
cur.execute('''CREATE TABLE IF NOT EXISTS vannonce (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
timeutc INTEGER NOT NULL,
date TEXT NOT NULL,
title TEXT NOT NULL,
number INTEGER NOT NULL,
rimnumber TEXT,
picname TEXT,
speaker TEXT NOT NULL,
theme TEXT NOT NULL,
description TEXT,
status TEXT,
andate TEXT NOT NULL,
anutctime INTEGER NOT NULL);''')
cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS time_id_vannonce ON vannonce (timeutc ASC);')
cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS antime_id_vannonce ON vannonce (anutctime ASC);')
#-----Create all news table-------
cur.execute('''CREATE TABLE IF NOT EXISTS allnews (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
tablename TEXT NOT NULL,
timeutc INTEGER NOT NULL,
record_id INTEGER NOT NULL);''')
cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS timeutc_id_allnews ON allnews (timeutc ASC);')
#-----Create authentication table-------
# cur.execute('''CREATE TABLE IF NOT EXISTS auth (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# timeutc INTEGER NOT NULL,
# date TEXT NOT NULL,
# title TEXT NOT NULL,
# msg TEXT NOT NULL);''')
# cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS time_id_auth ON auth (timeutc ASC);')

conn.commit()
conn.close()
