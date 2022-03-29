# -*- coding: utf-8 -*-
from pydantic import BaseModel


class UserRet(BaseModel):
    id: int
    # 用户名
    username: str
    # todo 部门外健
    dep_id: int
    # 头像
    avatar: str
    # 地址
    addr: str
    # 状态
    state: int
    # 上次登陆日期
    last_login_date: str
    # 上次登录的IP地址
    ip: str
    # 创建时间:年月日 时分秒
    create_time: str
    # 创建日期
    create_date: str
