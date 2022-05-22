# -*- coding: utf-8 -*-
import datetime

from extend.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 角色名称
    name = Column(String(255))
    # 角色描述
    desc = Column(String(255))
    # 创建时间:年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建日期
    create_date = Column(Date, default=datetime.datetime.now())
