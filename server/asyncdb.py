# -*- coding: utf-8 -*-
#-------------------------------------------------------------------
# autor(s): Pavel Plotnikov (humanmashine)
#
# description: Модуль асинхронного доступа к БД
#
# info: MIT License 
#       it-for-free 2014
#-------------------------------------------------------------------
import server.common.dblib
import time
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from concurrent.futures import ThreadPoolExecutor


class AsyncDb():

    def __init__(self, io_loop=None, dbpath="db.db"):
        self.executor = ThreadPoolExecutor(5)
        self.io_loop = io_loop or IOLoop.instance()
        self.db = server.common.dblib.DbIff()
        self.db.connect(dbpath)

    @run_on_executor
    def get_near_vannonce(self):
        """
        Получение ближайшего анонса по дате проведения
        """
        _data = self.db.get_near_vanonce()
        _tm = time.time()
        if len(_data) > 0:
            _mind = abs(_data[0][12] - _tm)
            _minel = _data[0]
            for _el in _data:
                if abs(_tm - _el[12]) < _mind:
                    _minel = _el
            _data = _minel
        else:
            _data = None
        return _data