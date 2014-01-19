# -*- coding: utf-8 -*-
#----------------------------------------------------
# autor(s): Pavel Plotnikov (humanmashine)
#
# description: Основной модуль сервера ifface
#              Является tornado web-приложением
#
# info: MIT License
#       it-for-free 2014
#----------------------------------------------------
import tornado.ioloop
import tornado.web
import iffconfig.settings


class MainHeader(tornado.web.RequestHandler):
    def get(self):
        pass


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHeader),
    ], **iffconfig.settings.app_settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()