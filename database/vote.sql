create table `vote` (
    `id` bigint(20) unsigned not null auto_increment comment '投票ID',
    `topic` varchar(128) not null default '' comment '标题',
    `desc` varchar(255) not null default '' comment '描述',
    `pic` varchar(128) not null default '' comment '图片链接',
    `deadline_time` datetime not null default '1970-01-01 00:00:00' comment '截止时间',
    `is_anonymous` tinyint(4) not null default 0 comment '是否匿名 0:不匿名 1:匿名',
    `sel_type` tinyint(4) not null default 1 comment '选择类型 1:单选 2:多选',
    `is_open` tinyint(4) not null default 1 comment '投票结果是否对发起者之外的人可见 1:公开 0:不公开',
    `wx_nick_name` varchar(32) not null default '' comment '发起者的微信昵称',
    `wx_open_id` varchar(32) not null default '' comment '发起者微信open_id',
    `wx_avatar_url` varchar(128) not null default '' comment '发起人头像url',
    `created_at` datetime not null default current_timestamp comment '创建时间',
    `updated_at` datetime not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`),
    key `ix_topic` (`topic`),
    key `ix_wx_open_id` (`wx_open_id`),
    key `ix_created_at` (`created_at`),
    key `ix_updated_at` (`updated_at`)
) engine=innodb default charset=utf8mb4 comment='投票主题表';

create table `option` (
    `id` bigint(20) unsigned not null auto_increment comment '选项ID',
    `desc` varchar(255) not null default '' comment '描述',
    `pic` varchar(128) not null default '' comment '图片链接',
    `vote_id` bigint(20) unsigned not null default 0 comment '投票ID',
    `is_deleted` tinyint(4) not null default 0 comment '是否删除',
    `created_at` datetime not null default current_timestamp comment '创建时间',
    `updated_at` datetime not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`),
    key `ix_vote_id` (`vote_id`),
    key `ix_created_at` (`created_at`),
    key `ix_updated_at` (`updated_at`)
) engine=innodb default charset=utf8mb4 comment='选项表';

create table `result_vote` (
    `id` bigint(20) unsigned not null auto_increment comment '投票结果ID',
    `vote_id` bigint(20) unsigned not null default 0 comment '投票ID',
    `option_id` bigint(20) unsigned not null default 0 comment '选项ID',
    `wx_nick_name` varchar(32) not null default '' comment '发起者的微信昵称',
    `wx_open_id` varchar(32) not null default '' comment '发起者微信open_id',
    `avatar_url` varchar(128) not null default '' comment '投票人头像url',
    `is_deleted` tinyint(4) not null default 0 comment '是否删除',
    `created_at` datetime not null default current_timestamp comment '创建时间',
    `updated_at` datetime not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`),
    key `ix_vote_id` (`vote_id`),
    key `ix_option_id` (`option_id`),
    key `ix_created_at` (`created_at`),
    key `ix_updated_at` (`updated_at`)
) engine=innodb default charset=utf8mb4 comment='投票结果表';

create table `feedback` (
    `id` bigint(20) unsigned not null auto_increment comment '反馈ID',
    `content` text not null default '' comment '反馈内容',
    `wx_nick_name` varchar(32) not null default '' comment '反馈人微信昵称',
    `wx_open_id` varchar(32) not null default '' comment '反馈人微信open_id',
    `created_at` datetime not null default current_timestamp comment '创建时间',
    `updated_at` datetime not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`),
    key `ix_wx_open_id` (`wx_open_id`),
    key `ix_created_at` (`created_at`),
    key `ix_updated_at` (`updated_at`)
) engine=innodb default charset=utf8mb4 comment='反馈表';

create table `notice` (
    `id` bigint(20) unsigned not null auto_increment comment '通知ID',
    `content` varchar(255) not null default '' comment '通知内容',
    `is_open` tinyint(4) not null default 0 comment '是否对所有人可见 0:不可见 1:可见',
    `wx_nick_name` varchar(32) not null default '' comment '反馈人微信昵称',
    `wx_open_id` varchar(32) not null default '' comment '反馈人微信open_id',
    `created_at` datetime not null default current_timestamp comment '创建时间',
    `updated_at` datetime not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`),
    key `ix_wx_open_id` (`wx_open_id`),
    key `ix_created_at` (`created_at`),
    key `ix_updated_at` (`updated_at`)
) engine=innodb default charset=utf8mb4 comment='通知表';
