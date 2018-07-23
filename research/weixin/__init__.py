# -*- coding:utf-8 -*-
import requests
import json
from flask import Blueprint
from research.utils.route import api_route
from research.settings import APP_ID, APP_SECRET, wx_check


wx = Blueprint('wx', __name__)


@api_route(wx, '/login/check')
def get_wx_login(*args, **kwargs):
    js_code = kwargs['js_code']
    grant_type = 'authorization_code'

    res = requests.get(
        url=wx_check,
        params={
            'app_id': APP_ID,
            'secret': APP_SECRET,
            'js_code': js_code,
            'grant_type': grant_type
        })
    print res.content
    res_dict = json.loads(res.content)
    return res_dict
