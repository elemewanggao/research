# -*- coding:utf-8 -*-
from datetime import datetime
from flask import Blueprint, request
from research.utils.request import get_request_args
from research.utils.route import api_route
from research.model.vote import Vote, Options, ResultVote, Feedback, Notice


vote = Blueprint('vote', __name__)


def add_vote(*args, **kwargs):
    """增加投票详情."""
    options = kwargs.pop('options')
    v = Vote(**kwargs)
    v.add()

    vote_id = v.id
    option_objs = []
    for option in options:
        option.update({
            'vote_id': vote_id})
        option_objs.append(Options(**option))
    Options.batch_add(option_objs)


def get_vote(vote_id=None, creater_open_id=None, voter_open_id=None):
    """获取投票详情."""
    result = []
    conditions = []
    if vote_id:
        conditions.append(Vote.id == vote_id)
    if creater_open_id:
        conditions.append(Vote.wx_open_id == creater_open_id)
    if conditions:
        votes = Vote.query(Vote, filter=conditions)
        vote_ids = [vote.id for vote in votes]
    if voter_open_id:
        revotes = ResultVote.query(ResultVote, filter=[
            ResultVote.voter_open_id == voter_open_id])
        revote_ids = [revote.id for revote in revotes]

    common_vote_ids = list(set(vote_ids) & set(revote_ids))

    votes = Vote.query(Vote, filter=[Vote.id.in_(common_vote_ids)])
    for vote in votes:
        vid = vote.id
        vote_result = {
            'vote_id': vid,
            'topic': vote.topic,
            'desc': vote.desc,
            'pic': vote.pic,
            'dealine': vote.dealine_time,
            'is_anonymous': vote.is_anonymous,
            'sel_type': vote.sel_type,
            'is_open': vote.is_open,
            'status': 1 if datetime.now() < vote.dealine_time else 2,
            'creater_nick_name': vote.wx_nick_name,
            'creater_open_id': vote.wx_open_id}
        options = Options.query(Options, filter=[
            Options.vote_id == vid,
            Options.is_deleted == 0])
        ops = [{
            'option_id': o.id,
            'desc': o.desc,
            'pic': o.pic
        } for o in options]
        vote_result['options'] = ops
        result.append(vote_result)
    return result


def edit_vote(*args, **kwargs):
    """修改投票详情"""
    vote_id = kwargs.pop('vote_id')
    option_list = kwargs.pop('option')

    Vote.update(kwargs, [Vote.id == vote_id])

    options = Options.query(Options, filter=[Options.vote_id == vote_id])
    for option in options:
        opid = option.id
        find_flag = False
        for option_dict in option_list:
            if opid == option_dict['id']:
                option.desc = option_dict['desc']
                option.pic = option_dict['pic']
                find_flag = True
                break
        if not find_flag:
            option.is_deleted = 1


@api_route(vote, '/', methods=['GET', 'POST', 'PUT'])
def handler():
    params = get_request_args(request)
    if request.method == 'GET':
        return get_vote(**params)
    elif request.method == 'POST':
        return add_vote(**params)
    elif request.method == 'PUT':
        return edit_vote(**params)
