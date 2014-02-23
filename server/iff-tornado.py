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
import tornado.escape
import tornado.gen
import server.iffconfig.settings
import os
import server.common.asynclog
import server.asyncdb
import time


log = server.common.asynclog.Log(server.iffconfig.settings.iff_settings["log_dir"])
db = server.asyncdb.AsyncDb(dbpath=server.iffconfig.settings.iff_settings['db_path'])
TORNADOCACHE = dict()


#-----
class BaseHandler(tornado.web.RequestHandler):
    # def get_current_user(self):
    #     if self.get_secure_cookie("user"):
    #         u_cookie = self.get_secure_cookie("user")
    #         try:
    #             u_cookie = u_cookie.decode()
    #             cu = tr_auth.get_user_id(u_cookie)
    #             if LOG_MOD == "Debug":
    #                 TrackLog.async_write("current user: {0}".format(cu), LOG_PATH)
    #             return cu
    #         except server.auth.AccessError as _au_err:
    #             if LOG_MOD == "Debug":
    #                 TrackLog.err_write(_au_err, LOG_PATH)
    #             return None
    #     else:
    #         if LOG_MOD == "Debug":
    #             TrackLog.write("Access Denied unreadble secure cookie", LOG_PATH)
    #         return None

    def check_xsrf_cookie(self):
        token = (self.get_argument("_xsrf", None) or
                 self.request.headers.get("X-Xsrftoken") or
                 self.request.headers.get("X-Csrftoken"))
        if not token:
            raise tornado.web.HTTPError(403, "'_xsrf' argument missing from POST")
        else:
            try:
                token = tornado.escape.json_decode(token)
            except ValueError:
                token = token
        if self.xsrf_token != token:
            raise tornado.web.HTTPError(403, "XSRF cookie does not match POST argument")
#------


class MainHeader(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader("../static/html/")
        self.write(loader.load("mainpage.html").generate())


class VebinarHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        _ntm = time.time()
        try:
            vnoce, tm = TORNADOCACHE['avannoce']
            if abs(_ntm - tm) > 120:
                raise KeyError("time over")
        except KeyError:
            vnoce = yield tornado.gen.Task(db.get_near_vannonce)
            TORNADOCACHE['avannoce'] = (vnoce, _ntm)
        if vnoce is not None:
            if _ntm < vnoce[12]:
                _stat_auto = "Время этой встречи ещё не пришло..."
            elif abs(_ntm - vnoce[12]) > 7200:
                _stat_auto = "Время этой встречи прошло..."
            else:
                _stat_auto = "На встречу ещё можно успеть, наверное ;)"
            _parms = {
                'correct_values': True,
                'vtitle': vnoce[3],
                'vnumber': vnoce[4],
                'picurl': vnoce[6],
                'rimnumber': vnoce[5],
                'speaker': vnoce[7],
                'theme': vnoce[8],
                'descryption': vnoce[9],
                'date': vnoce[11],
                'status_bd': vnoce[10],
                'status_auto': _stat_auto,
            }
            self.render("video.html", **_parms)
        else:
            self.render("video.html", correct_values=False)


if __name__ == "__main__":
    print(r"TORNADO:: starting... pid:", os.getpid())
    log.write("Tornado Server Start")
    application = tornado.web.Application([
        (r"/", MainHeader),
        (r"/video/", VebinarHandler),
    ], **server.iffconfig.settings.app_settings)
    application.listen(8888)
    print("TORNADO:: I'm ready")
    log.write("ready.")
    tornado.ioloop.IOLoop.instance().start()
