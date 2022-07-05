# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:38
# FILE    : tornado
# PROJECT : funfunc
# IDE     : PyCharm
import tornado.web


# 解决tornado-vue 跨域问题
class BaseTornadoWebHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    # 重写该方法
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有的域名访问
        self.set_header("Access-Control-Allow-Headers", "*")  # 允许携带所有的参数
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")  # 允许所有的请求方式
        self.set_header("Access-Control-Max-Age", "3600")  # 允许连接时，最大响应时间

    # 定义一个响应的方法，不需要实现什么功能
    def options(self):
        pass
