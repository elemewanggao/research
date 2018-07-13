# -*- coding:utf-8 -*-
import logging
import logging.config
from research.settings import LOGGING


logging.config.dictConfig(LOGGING)


def get_logger(__name__):
    return logging.getLogger(__name__)
