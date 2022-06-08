# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import datetime

from extend.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date


class Rermission(Base):
    __tablename__ = "permission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 权限名称
    name = Column(String(255))
    # url，前端的url
    url = Column(String(255))
    # 请求方法
    method = Column(String(255))
    # 参数
    args = Column(String(255))
    # 父级菜单id，如果是一级菜单则为0
    parent_id = Column(Integer)
    # 描述
    desc = Column(String(255))

    # 创建时间:年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建日期
    create_date = Column(Date, default=datetime.datetime.now())
