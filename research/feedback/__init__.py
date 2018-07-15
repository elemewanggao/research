# -*- coding:utf-8 -*-
from flask import Blueprint, request
from research.utils.route import api_route
from research.utils.request import get_request_args
from research.model.vote import Feedback

feedback = Blueprint('feedback', __name__)


@api_route(feedback, '/', methods=['POST'])
def commit_feedback():
    params = get_request_args(request)
    content = params['content']
    wx_nick_name = params['wx_nick_name']
    wx_open_id = params['wx_open_id']

    Feedback(
        content=content,
        wx_nick_name=wx_nick_name,
        wx_open_id=wx_open_id
    ).add()
