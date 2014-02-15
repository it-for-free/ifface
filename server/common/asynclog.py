# -*- coding: utf-8 -*-
#-------------------------------------------------------------------
# autor(s): Pavel Plotnikov (humanmashine)
#
# description: Модуль асинхронного логирования. Позволяет
#    осуществлять неблокирующую запись логов, взамен не гарантирует
#    жёсткой привязки ко времени, включает в себя также синхронные
#    методы логгирования для удобства.
# info: MIT License 
#       it-for-free 2014
#-------------------------------------------------------------------
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class Log():
    """
    Класс для удобной реализации логирования
    """

    def __init__(self, log_dir):
        """
        Конструктор
        @param log_dir: путь к файлу журнала
        """
        self._log_dir = log_dir
        self.executor = ThreadPoolExecutor(1)

    @staticmethod
    def __write(msg, logpath):
        """
        Внутренняя функция записи, работающая в асинхронном режиме
        @param logpath: путь к логу
        @param msg: сообщение
        """
        with open(logpath, mode='a') as _log:
            _log.write("\n" + msg)

    def write(self, msg):
        """
        Функция асинхронной записи в лог
        @param msg: сообщение
        """
        _msg = ">>> [{0}] {1} ::: {2}".format(os.getpgid(), datetime.now(), msg)
        self.executor.submit(self.__write, _msg, self._log_dir)