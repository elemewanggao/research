# -*- coding:utf-8 -*-
from sqlalchemy import or_
from flask import Blueprint, request
from research.utils.route import api_route
from research.utils.request import get_request_args
from research.model.vote import Notice

notice = Blueprint('notice', __name__)


@api_route(notice, '/', methods=['POST', 'GET'])
def add_notice(*args, **kwargs):
    params = get_request_args(request)
    content = params['content']
    is_open = params['is_open']
    wx_nick_name = params['wx_nick_name']
    wx_open_id = params['wx_open_id']

    if request.method == 'POST':
        Notice(
            content=content,
            is_open=is_open,
            wx_nick_name=wx_nick_name,
            wx_open_id=wx_open_id
        ).add()
    elif request.method == 'GET':
        notices = Notice.query(
            Notice,
            filter=or_[
                Notice.wx_open_id == wx_open_id,
                Notice.is_open == 1])
        return [{
            'content': notice.content,
            'is_read': notice.is_read,
        }for notice in notices]


@api_route(notice, '/tap', methods=['PUT'])
def tap_notice(*args, **kwargs):
    params = get_request_args(request)
    notice_id = params['notice_id']
    Notice.update(
        {'is_read': 1},
        filter=[Notice.id == notice_id])
