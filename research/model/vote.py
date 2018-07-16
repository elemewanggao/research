# -*- coding:utf-8 -*-
from datetime import datetime
from . import Base, BaseModel
from sqlalchemy import (
    Column, BigInteger, DateTime, String, Text, SmallInteger
)


class Vote(Base, BaseModel):
    """投票主题."""
    __tablename__ = 'vote'
    _db_name = 'research'

    id = Column(BigInteger, primary_key=True)
    topic = Column(String(128))
    desc = Column(String(255), default='')
    pic = Column(String(128), default='')
    deadline_time = Column(DateTime)
    is_anonymous = Column(SmallInteger, default=0)
    sel_type = Column(SmallInteger, default=1)
    is_open = Column(SmallInteger, default=1)
    wx_nick_name = Column(String(32))
    wx_open_id = Column(String(32))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)


class Options(Base, BaseModel):
    """选项"""
    __tablename__ = 'options'
    _db_name = 'research'

    id = Column(BigInteger, primary_key=True)
    desc = Column(String(255), default='')
    pic = Column(String(128), default='')
    vote_id = Column(BigInteger)
    is_deleted = Column(SmallInteger, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)


class ResultVote(Base, BaseModel):
    """投票结果"""
    __tablename__ = 'result_vote'
    _db_name = 'research'

    id = Column(BigInteger, primary_key=True)
    vote_id = Column(BigInteger)
    option_id = Column(BigInteger)
    wx_nick_name = Column(String(32))
    wx_open_id = Column(String(32))
    avatar_url = Column(String(128), default='')
    is_deleted = Column(SmallInteger, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)


class Feedback(Base, BaseModel):
    """反馈"""
    __tablename__ = 'feedback'
    _db_name = 'research'

    id = Column(BigInteger, primary_key=True)
    content = Column(Text)
    wx_nick_name = Column(String(32))
    wx_open_id = Column(String(32))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)


class Notice(Base, BaseModel):
    """通知"""
    __tablename__ = 'notice'
    _db_name = 'research'

    id = Column(BigInteger, primary_key=True)
    content = Column(Text)
    is_open = Column(SmallInteger, default=1)
    wx_nick_name = Column(String(32), default='')
    wx_open_id = Column(String(32), default='')
    is_read = Column(SmallInteger, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
