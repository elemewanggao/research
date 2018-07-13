# -*- coding:utf-8 -*-
import traceback
import functools
from flask import request
from .response import make_res, make_exc_res
from .request import get_request_args
from research.log import get_logger


logger = get_logger(__name__)


def api_route(app, rule, **options):
    """自定义路由装饰器."""
    def deco(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            response = None
            try:
                req_params = get_request_args(request)
                kwargs.update(req_params)
                res = func(*args, **kwargs)
            except Exception as e:
                logger.exception('Exception!!! {}'.format(traceback.format_exc()))
                response = make_exc_res(e)
            else:
                response = make_res(res)
            finally:
                response.headers['Content-Type'] = 'application/json'
                return response
        endpoint = func.__module__ + '.' + func.__name__
        endpoint = endpoint.replace('.', '_')
        logger.info('{rule}=>{endpoint}=>{wrapper}'.format(
            rule=rule,
            endpoint=endpoint,
            wrapper=wrapper))
        app.add_url_rule(
            rule=rule,
            endpoint=endpoint,
            view_func=wrapper,
            **options)
        return wrapper
    return deco
