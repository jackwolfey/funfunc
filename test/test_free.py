# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/8/18 18:16
# FILE    : test_free
# PROJECT : funfunc
# IDE     : PyCharm
import funfunc
from funfunc import get_args_info, get_methods
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', type=str)
parser.add_argument('-m', '--method', type=str)
args = parser.parse_args()

print(get_args_info('default_args', args))


class New(object):
    def __init__(self):
        pass

    def foo(self):
        pass

    def bar(self):
        pass

    def sample(self):
        pass


n = New()
n.new_shit = 'a'


@funfunc.try_except_print
def random_func():
    raise RuntimeError("this is a funfunc test")


n.func = random_func
print(get_methods(n))

n.func()
