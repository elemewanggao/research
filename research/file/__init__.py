# -*- coding:utf-8 -*-
"""文件操作"""
from flask import request, Blueprint
from research.utils.route import api_route
from research.utils.request import get_request_args
from research.log import get_logger


logger = get_logger(__name__)
file = Blueprint('file', __name__)


@api_route(file, '/upload', methods=['POST'])
def upload(*args, **kwargs):
    data = get_request_args(request)
    file_path = '/Users/wanggao/mm/'
    logger.info('request.files:{}, data:{}'.format(
        request.files,
        data))
    file_handler = request.files['image']

    file_name = file_handler.filename
    file_store_path = file_path + file_name

    file_handler.save(file_store_path)
    return file_store_path
