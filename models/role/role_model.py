# -*- coding: utf-8 -*-
import datetime

from sqlalchemy.orm import relationship

from extend.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey


# 一对一：外键可以在任意一方，建议把外键放在主表
# 一对多：外键在多的一方
# 多对多：需要一个中间表

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


# 方式一
# 角色和权限多对多，中间表自动生成，难以对中间表排序
# permissions = relationship('Permission', backref='role', secondary='role_permissions')
# 角色和用户多对多
# users = relationship('User', backref='role', secondary='role_users')

# 方式二
class RolePermissions(Base):
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 角色外健
    role_id = Column(Integer, ForeignKey('role.id'))
    # 权限外健
    permission_id = Column(Integer, ForeignKey('permission.id'))
    # 创建时间:年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建日期
    create_date = Column(Date, default=datetime.datetime.now())


class RoleUsers(Base):
    __tablename__ = "role_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 角色外健
    role_id = Column(Integer, ForeignKey('role.id'))
    # 用户外健
    user_id = Column(Integer, ForeignKey('user.id'))
    # 创建时间:年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建日期
    create_date = Column(Date, default=datetime.datetime.now())
