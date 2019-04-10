#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据库操作."""
import functools
from contextlib import contextmanager
from collections import Iterable
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from research.settings import MYSQL

engines = {}
Base = declarative_base()


def init_engines():
    """初始化数据库连接"""
    for k, v in MYSQL.iteritems():
        mysql_url = ("mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}"
                     "?charset=utf8".format(**v))
        engines[k] = create_engine(mysql_url,
                                   pool_size=10,
                                   max_overflow=-1,
                                   pool_recycle=1000,
                                   echo=False)


init_engines()


def get_session(db):
    """获取session"""
    return scoped_session(sessionmaker(
        bind=engines[db],
        expire_on_commit=False))


@contextmanager
def Db_session(db='research', commit=True):
    """db session封装.

    :params db:数据库名称
    :params commit:进行数据库操作后是否进行commit操作的标志
                   True：commit, False:不commit
    """
    session = get_session(db)
    try:
        yield session
        if commit:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        if session:
            session.close()


def class_dbsession(commit=True):
    """用于BaseModel中进行数据库操作前获取dbsession操作.

    :param commit:进行数据库操作后是否进行commit操作的标志，True：commit, False:不commit
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            cls = args[0]
            new_args = args[1:]
            with Db_session(cls._db_name, commit) as session:
                return func(cls, session, *new_args, **kwargs)
        return inner
    return wrapper


class BaseModel(object):
    u"""基础模型."""

    _db_name = 'research'

    @class_dbsession(True)
    def add(self, session):
        u"""增.

        eg: a = MerchantBillDetail(id=1)
            a.add()
        """
        session.add(self)

    @classmethod
    @class_dbsession(True)
    def batch_add(cls, session, objs):
        """批量增加.

        eg: a = [MerchantBillDetail(id=1), MerchantBillDetail(id=2)]
            MerchantBillDetail.batch_add(a)
        """
        return session.add_all(objs)

    @classmethod
    @class_dbsession(True)
    def delete(cls, session, conditions=[]):
        u"""删.

        eg: BaseModel.delete([BaseModel.a>1, BaseModel.b==2])
        """
        session.query(cls).filter(*conditions).delete(
            synchronize_session='fetch')

    @classmethod
    @class_dbsession(True)
    def update(cls, session, update_dict, conditions=[]):
        u"""更新.

        eg: BaseModel.update({'name': 'jack'}, [BaseModel.id>=1])
        """
        return session.query(cls).filter(*conditions).update(
            update_dict,
            synchronize_session='fetch')

    @classmethod
    @class_dbsession(True)
    def join(cls, session, other_model, join_condition):
        u"""
        两表连接查询
        """
        return session.query(cls, other_model).join(
            other_model, *join_condition)

    @classmethod
    @class_dbsession(False)
    def query(cls, session, params, **conditions):
        u"""查询.

        eg: BaseModel.query([BaseModel.id, BaseModel.name],
                filter=[BaseModel.id>=1],
                group_by=[BaseModel.id, BaseModel.name]
                order_by=BaseModel.id.desc(), limit=10, offset=0)
        """
        if not conditions:
            if not set(conditions.keys()).issubset(
                    {'filter', 'group_by', 'order_by', 'limit', 'offset'}):
                raise Exception('input para error!')
        cfilter = conditions.pop('filter', None)
        group_para = conditions.pop('group_by', None)
        order_para = conditions.pop('order_by', None)
        limit = conditions.pop('limit', None)
        offset = conditions.pop('offset', None)
        query_first = conditions.get('query_first', False)

        if not isinstance(params, Iterable):
            params = [params]
        squery = session.query(*params)
        if cfilter is not None:
            squery = squery.filter(*cfilter)
        if group_para is not None:
            squery = squery.group_by(*group_para)
        if order_para is not None:
            squery = squery.order_by(order_para)
        if limit is not None:
            squery = squery.limit(limit)
        if offset is not None:
            squery = squery.offset(offset)
        if query_first:
            return squery.first()
        return squery.all()

    @classmethod
    @class_dbsession(False)
    def __aggregate(cls, session, aggr_fun, params, conditions=[]):
        u"""对参数进行聚合函数(sum, avg, max, min)计算.

        BaseModel.__aggregate(func.sum,
                            [BaseModel.id, BaseModel.num], [BaseModel.id==1])
        """
        if not isinstance(params, Iterable):
            params = [params]
        aggr_list = [aggr_fun(param) for param in params]
        re = session.query(*aggr_list).filter(*conditions).one()
        if len(re) == 1:
            return re[0] or 0
        return [i or 0 for i in re]

    @classmethod
    def sum(cls, params, conditions=[]):
        u"""求和.

        eg: BaseModel.sum([BaseModel.id], [BaseModel.id==1])
        """
        return cls.__aggregate(func.sum, params, conditions)

    @classmethod
    def max(cls, params, conditions=[]):
        u"""求最大值.

        eg: BaseModel.max([BaseModel.num], [BaseModel.id==2])
        """
        return cls.__aggregate(func.max, params, conditions)

    @classmethod
    @class_dbsession(False)
    def count(cls, session, params, conditions=[], distinct=False):
        u"""计数.

        eg: BaseModel.count([BaseModel.id, BaseModel.XXX], [BaseModel.id==2])
            BaseModel.count(BaseModel.id, [BaseModel.id==2], True)
        """
        if distinct:
            if isinstance(params, Iterable) and len(params) >= 2:
                re = session.query(func.count(
                    func.distinct(func.concat(*params))))\
                    .filter(*conditions).one()[0]
            elif isinstance(params, Iterable):
                qp = params[0]
                re = session.query(func.count(func.distinct(qp))).filter(
                    *conditions).one()[0]
            else:
                re = session.query(func.count(func.distinct(
                    params))).filter(*conditions).one()[0]
        else:
            if not isinstance(params, Iterable):
                params = [params]
            re = session.query(*params).filter(*conditions).count()
        return re

    @classmethod
    @class_dbsession(False)
    def simple_paging_query(cls, session, params, conditions, page_size=100):
        """简单分页查询
        """
        total_count = cls.count([cls.id], conditions)
        rv = []
        for offset in range(0, total_count, page_size):
            rv.extend(cls.query(
                params, filter=conditions, offset=offset, limit=page_size
            ))
        return rv

    @classmethod
    def execute(cls, sql_str):
        with Db_session(cls._db_name, commit=True) as session:
            return session.execute(sql_str)
