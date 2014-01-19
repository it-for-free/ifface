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
import tornado.template
import tornado.web
import iffconfig.settings


class MainHeader(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader("../static/html/")
        self.write(loader.load("mainpage.html").generate())


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHeader),
    ], **iffconfig.settings.app_settings)
    application.listen(8888)
    print("I'm ready")
    tornado.ioloop.IOLoop.instance().start()