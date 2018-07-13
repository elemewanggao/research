# -*- coding:utf-8 -*-
from .code import EXCE_CODE


class ResearchUserExc(Exception):
    """用户自定义异常."""

    def __init__(self, code, msg):
        super(ResearchUserExc, self).__init__(msg)
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'ResearchUserExc, code:{code}, msg:{msg}'.format(
            code=self.code,
            msg=self.msg)


def exception_raiser(exc):
    """异常生成器."""
    def wrapper(code, *args, **kwargs):
        if code in EXCE_CODE:
            icode = EXCE_CODE[code][0]
            msg = EXCE_CODE[code][1]

            if args:
                raise exc(icode, msg.format(*args))
            elif kwargs:
                raise exc(icode, msg.format(**kwargs))
            else:
                raise exc(icode, msg)
        else:
            raise Exception('unknow exception')

    return wrapper


raise_user_exc = exception_raiser(ResearchUserExc)
