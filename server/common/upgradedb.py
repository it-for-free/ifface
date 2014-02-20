# -*- coding: utf-8 -*-
#-----------------------------------------
# autor(s): Pavel Plotnikov (humanmashine)
#
# description: Модуль (утилита) для
#     создания и обновления базы данных.
#     For posgresql and py-postgresql
# info: MIT License 
#       it-for-free 2014
#-----------------------------------------
import postgresql

from server.iffconfig.settings import iff_settings

db = postgresql.open(iff_settings['db_path'])
#cur = conn.cursor()
#-----Create notes table-------
db.execute('''CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY NOT NULL,
timeutc BIGINT NOT NULL,
date TIMESTAMP NOT NULL,
title TEXT NOT NULL,
description TEXT NOT NULL);''')
db.execute('CREATE UNIQUE INDEX time_id_notes ON notes (timeutc DESC);')
#-----Create some annonces table-------
db.execute('''CREATE TABLE IF NOT EXISTS sannonce (id SERIAL PRIMARY KEY NOT NULL,
timeutc BIGINT NOT NULL,
date TIMESTAMP NOT NULL,
title TEXT NOT NULL,
picname TEXT,
andate TIMESTAMP NOT NULL,
description TEXT NOT NULL);''')
db.execute('CREATE UNIQUE INDEX time_id_sannonce ON sannonce (timeutc DESC);')
#-----Create news table-------
db.execute('''CREATE TABLE IF NOT EXISTS news (id SERIAL PRIMARY KEY NOT NULL,
timeutc BIGINT NOT NULL,
date TIMESTAMP NOT NULL,
title TEXT NOT NULL,
picname TEXT,
description TEXT NOT NULL);''')
db.execute('CREATE UNIQUE INDEX time_id_news ON news (timeutc DESC);')
#-----Create video annonces table-------
db.execute('''CREATE TABLE IF NOT EXISTS vannonce (id SERIAL PRIMARY KEY NOT NULL,
timeutc BIGINT NOT NULL,
date TIMESTAMP NOT NULL,
title TEXT NOT NULL,
number INTEGER NOT NULL,
rimnumber TEXT,
picname TEXT,
speaker TEXT NOT NULL,
theme TEXT NOT NULL,
description TEXT,
status VARCHAR(30),
andate TIMESTAMP NOT NULL,
anutctime BIGINT NOT NULL);''')
db.execute('CREATE UNIQUE INDEX time_id_vannonce ON vannonce (timeutc DESC, anutctime ASC);')
#-----Create all news table-------
db.execute('''CREATE TABLE IF NOT EXISTS allnews (id SERIAL PRIMARY KEY NOT NULL,
tablename TEXT NOT NULL,
timeutc BIGINT NOT NULL,
record_id INTEGER NOT NULL);''')
#-----Create authentication table-------
# cur.execute('''CREATE TABLE IF NOT EXISTS auth (id SERIAL PRIMARY KEY NOT NULL,
# timeutc BIGINT NOT NULL,
# date TEXT NOT NULL,
# title TEXT NOT NULL,
# msg TEXT NOT NULL);''')
# cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS time_id_auth ON auth (timeutc ASC);')
#-----Create meta table-------
db.execute('''CREATE TABLE IF NOT EXISTS meta (id SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL,
value TEXT NOT NULL);''')
db.execute('CREATE UNIQUE INDEX meta_name ON meta (name);')

#conn.commit()
#conn.close()
