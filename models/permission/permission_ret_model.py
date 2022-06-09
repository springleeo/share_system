# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class PermissionRet(BaseModel):
    id: Optional[int]
    # 权限名称
    name: Optional[str]
    # url
    url: Optional[str]
    # 请求方法
    method: Optional[str]
    # 参数
    args: Optional[str]
    # 父级菜单
    parent_name: Optional[str]
    # 描述
    desc: Optional[str]
    # 创建时间:年月日 时分秒
    create_time: Optional[str]
    # 创建日期
    create_date: Optional[str]
