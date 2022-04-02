# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional


class DepartmentRet(BaseModel):
    id: Optional[int]
    # 部门名称
    name: Optional[str]
    # 部门主管
    leader: Optional[str]
    # 部门职责
    desc: Optional[str]
    # 状态
    state: Optional[int]
    # 创建时间:年月日 时分秒
    create_time: Optional[str]
    # 创建日期
    create_date: Optional[str]
