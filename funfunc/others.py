# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:38
# FILE    : others
# PROJECT : funfunc
# IDE     : PyCharm
try:
    from tornado.web import RequestHandler
except ImportError:
    pass


class BaseTornadoWebHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")
        self.set_header("Access-Control-Max-Age", "3600")

    def options(self):
        pass


def pywebio_set_footer(content):
    from pywebio.session import run_js

    run_js(f'$(".footer").text("{content}")')
