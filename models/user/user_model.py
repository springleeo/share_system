# -*- coding: utf-8 -*-
import datetime

from extend.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 部门名称
    name = Column(String(255),unique=True)
    # 部门主管
    leader = Column(String(255))
    # 部门职责
    desc = Column(String(255))
    # 用户表的反向关系
    user = relationship('User', backref='department')
    # 创建时间:年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建日期
    create_date = Column(Date, default=datetime.datetime.now())


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 用户名
    username = Column(String(255))
    # 密码
    pwd = Column(String(255))
    # 部门外健
    dep_id = Column(Integer, ForeignKey('department.id'))

    # 头像
    avatar = Column(String(255), default='/uploads/users/img.jpg')
    # 地址
    addr = Column(String(255))
    # 状态
    state = Column(Integer, default=1)
    # 上次登陆日期
    last_login_date = Column(Date, default=datetime.datetime.now())
    # 上次登录的IP地址
    ip = Column(String(255))
    # 创建时间:年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建日期
    create_date = Column(Date, default=datetime.datetime.now())
