# -*- coding: utf-8 -*-
#----------------------------------------------------
# autor(s): Pavel Plotnikov (humanmashine)
#
# description: Модуль для работы с базой данных
#
# info: MIT License 
#       it-for-free 2014
#----------------------------------------------------
import postgresql
import time


class SQLError(Exception):
    pass


class SQLInjection(SQLError):
    pass


class DbIff():
    """
     Класс для работы с базой данных
    """

    def __init__(self, id_inst=0):
        """
        Constructor
        """
        self.id_instance = id_inst
        self.connection_status = False
        self.connection = None
        self.prepared_statements = []

    def connect(self, db_path):
        """
        Соединение с базой
        @param db_path: путь к базе
        """
        self.connection = postgresql.open(db_path)
        self.connection_status = True
        _prp = self.connection.prepare("SELECT * FROM vannonce WHERE anutctime>=$1 AND anutctime<$2")
        self.prepared_statements.append(_prp)  # p_s[0] - get near vnonce statement
        _prp = self.connection.prepare("SELECT * FROM vannonce WHERE timeutc=$1 AND anutctime=$2")
        self.prepared_statements.append(_prp)  # p_s[1] - get_vannonce_data_utc

    def disconect(self):
        """
        Отсоединение от базы
        """
        if self.connection_status:
            self.connection.close()
            self.connection_status = False

    def get_near_vanonce(self):
        """
        Функция получения ближайших к сегоднешнему дню анонса видеовстреч
        (тоесть, которые не дольше месяца в ожидании)
        """
        if not self.connection_status:
            raise SQLError("No Connection")
        _ntm = time.time()
        _ptm = _ntm - 54000
        _ftm = _ntm + 2678400
        _data = self.prepared_statements[0](_ptm, _ftm)
        return _data

    def get_vannonce_data_utc(self, tutc, antutc):
        """
        Функция получения видео анонса по времени публикации и времени проведения
        @param tutc: время создания (публикации)
        @param antutc: время проведения
        """
        if (type(tutc) is not int) or (type(antutc) is not int):
            raise SQLInjection("Might be injection in get_vannonce_data_utc")
        _data = self.prepared_statements[1](tutc, antutc)
        return _data

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
            "'", '"', ">", "<", "!", "(", ")", "{", "}", "[", "]", "=", "*", "/", "\\", "#", "?", "%", "$", "^",
            ";",
        }
        if set(expr) & _bad_sym:
            raise SQLInjection("simple sql injection filter detect bad symbol")
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
    db.connect("pq://iff_admin:ifface@localhost/ifface")
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
    print("--- Test get near vannonce----")
    data = db.get_near_vanonce()
    print(data)
    #--------------