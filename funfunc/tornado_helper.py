# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:38
# FILE    : tornado
# PROJECT : funfunc
# IDE     : PyCharm
import tornado.web


class BaseTornadoWebHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")
        self.set_header("Access-Control-Max-Age", "3600")

    def options(self):
        pass
