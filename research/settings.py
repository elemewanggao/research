# -*- coding:utf-8 -*-
"""app全局配置和全局变量"""
import socket


if 'local' in socket.gethostname():
    log_file_path = '/Users/wanggao/git/research/research.log'
    host = 'gz-cdb-oi7jr91l.sql.tencentcdb.com'
    port = 62337
else:
    log_file_path = '/data/log/ves/research/research.log'
    host = '172.16.16.14'
    port = 3306

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['all', 'console'],
        'level': 'INFO'
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'uniform',
        },
        'all': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'uniform',
            'filename': log_file_path,
            'mode': 'a',
            'maxBytes': 262144000,  # 200M
            'backupCount': 10,
        },
    },
    'formatters': {
        'uniform': {
            'format': '%(asctime)s %(levelname)-6s %(name)s[%(process)d]: '
                      '%(module)s => %(funcName)s ##  %(message)s',
        }
    }
}

# 数据库配置
MYSQL = {
    'research': {
        'user': 'root',
        'passwd': '19900201wg!@',
        'host': host,
        'port': port,
        'db': 'research',
    }
}

# 小程序配置
APP_ID = 'wx531fbd69492dcdbb'
APP_SECRET = 'fd4b7260208b8127cc792d590fde5db7'
wx_check = 'https://api.weixin.qq.com/sns/jscode2session'
