# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:28
# FILE    : nlp
# PROJECT : funfunc
# IDE     : PyCharm
import re


class Validator:

    @classmethod
    def is_url(cls, url_string) -> bool:
        pat = re.compile(r"^(http|https)://[0-9a-zA-Z.]*")
        if pat.match(url_string):
            return True
        else:
            return False


if __name__ == '__main__':
    print(Validator.is_url('https://www.shit.com'))
