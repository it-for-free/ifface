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
import tornado.httpclient
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
                'timeutc': vnoce[1],
                'antimeutc': vnoce[12],
            }
            self.render("video.html", **_parms)
        else:
            self.render("video.html", correct_values=False)


class InDevelop(BaseHandler):
    def get(self):
        """
        Заглушка для выдачи страницы с информацией о разработке
        """
        self.render("indev.html")


class ApiHandler(BaseHandler):
    """
    Это api сайта, для различных "гибких" нужд, скажем для проксирования к BBB
    """
    @tornado.gen.coroutine
    def get(self, api_param):
        """
        Обработчик переадресации запроса к bbb
        @param api_param: api запрос к  bbb
        """
        try:
            _meetingid = self.get_argument("meetingID")
            _cs = self.get_argument("checksum")
        except tornado.web.MissingArgumentError:
            log.write("in API Missing Argument Error")
            raise tornado.web.MissingArgumentError("Invalid Argument")
        http_client = tornado.httpclient.AsyncHTTPClient()
        _url = "http://conference.main.vsu.ru/{0}?meetingID={1}&checksum={2}".format(api_param, _meetingid, _cs)
        responce = yield tornado.gen.Task(http_client.fetch, _url)
        self.write(responce.body)

    @tornado.gen.coroutine
    def post(self, api_param):
        """
        отдаём данные по анонсу
        @param api_param: api запрос к  iff
        """
        if api_param == "videovnoncestat":
            _args = self.get_argument("data")
            _args = tornado.escape.json_decode(_args)
            try:
                _vnoce = yield tornado.gen.Task(db.get_vannonce_data_utc, int(_args["utc"]), int(_args["anutc"]))
            except Exception as _err:
                log.write("Error in api post/ get annonce by utc + " + str(_err))
                raise tornado.web.HTTPError(500, "API SERVER ERROR")
            if _vnoce is not None:
                _ansv = {"status": _vnoce[10]}
                _ansv = tornado.escape.json_encode(_ansv)
                self.write(_ansv)
            else:
                raise tornado.web.HTTPError(204, "No content")
        else:
            raise tornado.web.HTTPError(405, "No Api method!")


if __name__ == "__main__":
    print(r"TORNADO:: starting... pid:", os.getpid())
    log.write("Tornado Server Start")
    application = tornado.web.Application([
        (r"/", MainHeader),
        (r"/video/", VebinarHandler),
        (r"/indev/", InDevelop),
        (r"/api/(.+)", ApiHandler),
    ], **server.iffconfig.settings.app_settings)
    application.listen(8888)
    print("TORNADO:: I'm ready")
    log.write("ready.")
    tornado.ioloop.IOLoop.instance().start()
