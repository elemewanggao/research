# -*- coding:utf-8 -*-
import jsonpickle
from flask import make_response, Response
from .exception import ResearchUserExc


def make_res(obj):
    if isinstance(obj, Response):
        return obj
    else:
        resp_dict = dict(code=200, msg='ok', result=obj)
        return make_response(jsonpickle.encode(resp_dict))


def make_exc_res(exc):
    if isinstance(exc, ResearchUserExc):
        exc_dict = dict(code=exc.code, msg=exc.msg)
        return make_response(jsonpickle.encode(exc_dict))
    else:
        return make_response(jsonpickle.encode(dict(
            code=100000,
            msg='老板，系统当前繁忙，请稍后再试哦!')))
