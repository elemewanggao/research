# -*- coding:utf-8 -*-
from datetime import datetime
from flask import Blueprint, request
from research.utils.request import get_request_args
from research.utils.route import api_route
from research.model.vote import Vote, Options, ResultVote


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
    common_vote_ids = []
    if vote_id:
        conditions.append(Vote.id == vote_id)
    if creater_open_id:
        conditions.append(Vote.wx_open_id == creater_open_id)
    if conditions:
        votes = Vote.query(Vote, filter=conditions)
        if votes:
            common_vote_ids = [vote.id for vote in votes]
    if voter_open_id:
        revotes = ResultVote.query(ResultVote, filter=[
            ResultVote.voter_open_id == voter_open_id])
        revote_ids = [revote.id for revote in revotes]
        if revote_ids:
            common_vote_ids = list(set(common_vote_ids) & set(revote_ids))

    votes = Vote.query(Vote, filter=[Vote.id.in_(common_vote_ids)])
    for vote in votes:
        vid = vote.id
        vote_result = {
            'vote_id': vid,
            'topic': vote.topic,
            'desc': vote.desc,
            'pic': vote.pic,
            'dealine': str(vote.deadline_time),
            'is_anonymous': vote.is_anonymous,
            'sel_type': vote.sel_type,
            'is_open': vote.is_open,
            'status': 1 if datetime.now() < vote.deadline_time else 2,
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
    option_list = kwargs.pop('options', [])

    Vote.update(kwargs, [Vote.id == vote_id])

    option_ids = [
        option['option_id'] for option in option_list if option.get('option_id')]
    # 删除option
    Options.update(
        {'is_deleted': 1},
        [~Options.id.in_(option_ids)])
    # 对于删除的option，将已经选择的投票结果删除
    ResultVote.update(
        {'is_deleted': 1},
        [~ResultVote.option_id.in_(option_ids)])

    for option_dict in option_list:
        option_id = option_dict.get('option_id')
        desc = option_dict['desc']
        pic = option_dict.get('pic')
        if not option_id:
            # 传入的option_id为None代表新加选项
            Options(
                desc=desc,
                pic=pic,
                vote_id=vote_id).add()
            continue
        Options.update(
            {'desc': desc, 'pic': pic},
            [Options.id == option_id,
             Options.is_deleted == 0])


def get_vote_result(vote_id):
    """获取投票的结果."""
    options = Options.query(
        Options,
        filter=[
            Options.is_deleted == 0,
            Options.vote_id == vote_id])
    data = []
    participant_num = ResultVote.count(
        ResultVote.wx_open_id,
        [ResultVote.is_deleted == 0,
         ResultVote.vote_id == vote_id],
        True)
    for option in options:
        option_id = option.id
        vote_results = ResultVote.query(
            ResultVote,
            filter=[
                ResultVote.is_deleted == 0,
                ResultVote.option_id == option_id])
        vote_num = len(vote_results)
        voters = [
            {'wx_nick_name': voter.wx_nick_name,
             'wx_open_id': voter.wx_open_id,
             'avatar_url': voter.avatar_url} for voter in vote_results]
        data.append({
            'option_id': option_id,
            'vote_num': vote_num,
            'voters': voters,
            'vote_rate': int(100.0 * vote_num / participant_num if participant_num else 0)
        })
    return {
        'participant_num': participant_num,
        'data': data
    }


def post_vote_result(vote_id,
                     option_id_list,
                     voter_wx_name,
                     voter_wx_open_id,
                     avatar_url):
    results = []
    for option_id in option_id_list:
        results.append(
            ResultVote(
                vote_id=vote_id,
                option_id=option_id,
                wx_nick_name=voter_wx_name,
                wx_open_id=voter_wx_open_id,
                avatar_url=avatar_url))
    ResultVote.batch_add(results)


@api_route(vote, '', methods=['GET', 'POST', 'PUT'])
def vote_handler(*args, **kwargs):
    params = get_request_args(request)
    if request.method == 'GET':
        return get_vote(**params)
    elif request.method == 'POST':
        return add_vote(**params)
    elif request.method == 'PUT':
        return edit_vote(**params)


@api_route(vote, '/result', methods=['GET', 'POST'])
def vote_result_handle(*args, **kwargs):
    params = get_request_args(request)
    vote_id = params.get('vote_id')
    option_id_list = params.get('option_id_list')
    voter_wx_name = params.get('voter_wx_name')
    voter_wx_open_id = params.get('voter_wx_open_id')
    avatar_url = params.get('avatar_url')
    if request.method == 'GET':
        return get_vote_result(vote_id)
    elif request.method == 'POST':
        return post_vote_result(
            vote_id,
            option_id_list,
            voter_wx_name,
            voter_wx_open_id,
            avatar_url)
