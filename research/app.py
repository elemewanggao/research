# -*- coding:utf-8 -*-
import time
from flask import Flask, request
from research.vote.server import vote
from research.feedback import feedback
from research.notice import notice
from research.file import file
from research.weixin import wx
from research.log import get_logger


logger = get_logger(__name__)
app = Flask(__name__)


@app.before_request
def before_request():
    logger.info('request come, {method}:{url}'.format(
        method=request.method,
        url=request.url))
    request.begin_time = time.time()


@app.after_request
def after_request(response):
    timing = (time.time() - request.begin_time) * 1000  # 精确到ms
    logger.info('request end, {method}:{url}=>response code:{code}, timing:{timing}ms'.format(
        method=request.method,
        url=request.url,
        code=response.status_code,
        timing=timing))
    return response


@app.route('/haha')
def haha():
    return 'haha'


app.register_blueprint(vote, url_prefix='/vote')
app.register_blueprint(feedback, url_prefix='/feedback')
app.register_blueprint(notice, url_prefix='/notice')
app.register_blueprint(file, url_prefix='/file')
app.register_blueprint(wx, url_prefix='/weixin')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
