# -*- coding:utf-8 -*-
import jsonpickle


def get_request_args(request):
    """获取请求参数,request.values可以获取大部分参数除json形式传的参数,request.get_data()可以获取json中的参数."""
    params = dict()
    for key, value in request.values.iteritems():
        params[key] = value

    data = request.get_data()
    if data:
        params.update(jsonpickle.decode(data))
    return params
