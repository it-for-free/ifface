# -*- coding: utf-8 -*-
"""
This is the settings for iff tornado server
Edit this to configure tornado
Default values you can find in settings.py.config.default
"""
import os.path

#Tornado Web Application Settings (See Tornado Docs):
app_settings = {
    #----General:-------
    'autoreload': True,
    'debug': True,
    'gzip': False,
    'serve_traceback': True,  # True, if Debug
    #'log_function': SOME_LOG_Function,
    #'default_handler_class': SOME_VALUE,
    #'default_handler_args': SOME_VALUE,
    #----Security:------
    'cookie_secret': "DebuG)--(Cokie_123738277829450324712757",
    #'login_url': "SOME_LOGIN_URL",
    'xsrf_cookies': True,
    #----Template:------
    #'autoescape': None,
    'compiled_template_cache': False,  # False, if Debug
    'template_path': os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, "templates"),
    #'template_loader': SOME_VALUE,
    #----Static Files:--
    'static_hash_cache': False,  # False, if Debug
    'static_path': os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, "static"),
    'static_url_prefix': "/static/",
}

#iff app settings:
iff_settings = {
    #DB PATH or url:
    'db_path': "pq://iff_admin:ifface@localhost/ifface",
    #Log Path:
    'log_dir': os.path.join(os.path.dirname(__file__), os.path.pardir, "ifftornado.log"),
}
