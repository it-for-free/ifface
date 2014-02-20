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
import queue
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from concurrent.futures import ThreadPoolExecutor


class AsyncDb():

    def __init__(self, io_loop=None, dbpath="db.db"):
        self.num_threads = 5  # количество потоков в пуле для работы с БД
        self.executor = ThreadPoolExecutor(self.num_threads)
        self.io_loop = io_loop or IOLoop.instance()
        self.db_queue = queue.Queue(maxsize=self.num_threads)
        for _num in range(0, self.num_threads):
            _db_o = server.common.dblib.DbIff(_num)
            _db_o.connect(dbpath)
            self.db_queue.put(_db_o)

    @run_on_executor
    def get_near_vannonce(self):
        """
        Получение ближайшего анонса по дате проведения
        """
        _db = self.db_queue.get(block=True, timeout=1)
        _data = _db.get_near_vanonce()
        self.db_queue.put(_db, block=True, timeout=1)
        #post processing:
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