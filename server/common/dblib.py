# -*- coding: utf-8 -*-
#----------------------------------------------------
# autor(s): Pavel Plotnikov (humanmashine)
#
# description: Модуль для работы с базой данных
#
# info: MIT License 
#       it-for-free 2014
#----------------------------------------------------
import sqlite3


class DbIff():
    """
     Класс для работы с базой данных
    """

    def __init__(self, db_path="simpdb.db"):
        """
        Constructor
        @param db_path: путь к базе данных
        """
        self.connection_status = False
        self.conn = sqlite3.connect(db_path)