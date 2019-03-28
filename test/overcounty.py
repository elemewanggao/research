#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    1:获取所有海外国家信息
    2:遍历1信息，code从202开始，heading为此国家，father_code为此code，is_hot=0,label=Null, 插入数据库即可
"""
import sys
from research.model import get_session

reload(sys)
sys.setdefaultencoding('utf-8')

session = get_session('up')


def deal_overcounties():
    cs = session.execute('select * from PublicManage_city where father_code_id=2').fetchall()
    code = 202
    is_hot = 0
    for c in cs:
        heading = c.heading
        father_code_id = c.code
        session.execute(
            'insert into PublicManage_city(code, heading, father_code_id, is_hot) values({code}, "{heading}", {father_code_id}, {is_hot})'.format(
            code=code,
            heading=heading,
            father_code_id=father_code_id,
            is_hot=is_hot))
        code = code + 1
    session.commit()


if __name__ == '__main__':
    deal_overcounties()
