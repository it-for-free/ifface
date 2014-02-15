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
import re


class SQLInjection(Exception):
    pass


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

    #------
    @staticmethod
    def _simple_sql_filter(expr):
        """
        Простой фильтр, предохраняющий от sql инъекций
        @param expr: выражение или параметр для фильтрации
        """
        _bad_sym = {
            "'", '"', ">", "<", "!", "(", ")", "{", "}", "[", "]", "=", "*",
        }
        if set(expr) & _bad_sym:
            raise SQLInjection("simple sql filter detect bad symbol")
        return True

    @staticmethod
    def ssqlfiltered(func):
        """
        Декоратор простой sql фильтрации
        @param func: function
        """
        def sqlfilterdecorator(*args, **kwargs):
            """wrapper"""
            for el in args:
                if type(el) == str:
                    DbIff._simple_sql_filter(el)
            for el in kwargs:
                if type(kwargs[el]) == str:
                    DbIff._simple_sql_filter([el])
            func(*args, **kwargs)
        return sqlfilterdecorator
    #------


if __name__ == "__main__":
    db = DbIff()
    #--------------
    print("---- Test Simple SQL Filter Decorator -----")

    @DbIff.ssqlfiltered
    def test_fun(one, two, tree="ololo"):
        print(one, two, tree)
    test_fun("lovalova", two="mega")
    test_fun("lovalova", "mega", "trololo")
    test_fun("lovalova", "mega",  tree=5)
    test_fun(4, "mega",  tree=5)
    try:
        test_fun(4, "ha'po'",  tree=5)
    except SQLInjection as _err:
        print(str(_err))
        print("Test Fine")
    #--------------