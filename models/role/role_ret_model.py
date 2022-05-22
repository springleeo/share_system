# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class RoleRet(BaseModel):
    id: Optional[int]
    # 角色名称
    name: Optional[str]
    # 角色描述
    desc: Optional[str]
    # 创建时间:年月日 时分秒
    create_time: Optional[str]
    # 创建日期
    create_date: Optional[str]
