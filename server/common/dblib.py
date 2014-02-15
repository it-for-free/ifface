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

    def __init__(self):
        """
        Constructor
        """
        self.connection_status = False
        self.connection = None

    def connect(self, db_path="simpdb.db"):
        """
        Соединение с базой
        @param db_path: путь к базе
        """
        self.connection = sqlite3.connect(db_path)
        self.connection_status = True

    #------------system functions----------------------
    def _authorization(self, user_id):
        """
        Проверка прав доступа для субъекта
        @param user_id: идентификатор пользователя в БД
        """
        _access = False
        if self.connection_status:
            pass
        return _access

    @staticmethod
    def _simple_sql_filter(expr):
        """
        Простой фильтр, предохраняющий от sql инъекций
        @param expr: выражение или параметр для фильтрации
        """
        pass