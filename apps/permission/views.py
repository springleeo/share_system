# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from extend.get_db import get_db
from models.permission.permission_ret_model import PermissionRet
from models.permission.permission_operation import get_permission_pagenation, get_permission_query_total, \
    get_permission_total, \
    get_permission_query_pagenation, permission_add, permission_edit, delete_permission_by_id, get_permission_by_id, \
    get_permission_no_parent_names, get_permission_parent_names
from utils import token

router = APIRouter(
    prefix='/permission'
)


@router.get('/permission_list', tags=['权限模块'])
def get_permission_list(page_size: int, current_page: int, token_id: str = Depends(token.parse_token),
                        db: Session = Depends(get_db)):
    permissions = get_permission_pagenation(db, page_size, current_page)
    permission_rets = []
    for permission in permissions:
        permission_ret = PermissionRet()
        permission_ret.id = permission.id
        permission_ret.name = permission.name
        permission_ret.url = permission.url
        permission_ret.method = permission.method
        permission_ret.args = permission.args
        permission_ret.desc = permission.desc
        permission_ret.icon = permission.icon
        permission_ret.create_time = permission.create_time
        if permission.parent_id == 0:
            permission_ret.parent_name = '无'
            permission_ret.level = '一级'
        else:
            permission_by_parent_id = get_permission_by_id(db, permission.parent_id)
            permission_ret.parent_name = permission_by_parent_id.name
            permission_ret.level = '二级'
        permission_rets.append(permission_ret)
    total = get_permission_total(db)
    content = {
        'permissions': permission_rets,
        'pageSize': page_size,
        'currentPage': current_page,
        'pageTotal': total
    }
    return content


@router.get('/query', tags=['权限模块'])
def get_permission_query_list(name: str, page_size: int, current_page: int, token_id: str = Depends(token.parse_token),
                              db: Session = Depends(get_db)):
    permissions = get_permission_query_pagenation(db, name, page_size, current_page)
    permission_rets = []
    for permission in permissions:
        permission_ret = PermissionRet()
        permission_ret.id = permission.id
        permission_ret.name = permission.name
        permission_ret.url = permission.url
        permission_ret.method = permission.method
        permission_ret.args = permission.args
        permission_ret.desc = permission.desc
        permission_ret.icon = permission.icon
        permission_ret.create_time = permission.create_time
        if permission.parent_id == 0:
            permission_ret.parent_name = '无'
            permission_ret.level = '一级'
        else:
            permission_by_parent_id = get_permission_by_id(db, permission.parent_id)
            permission_ret.parent_name = permission_by_parent_id.name
            permission_ret.level = '二级'
        permission_rets.append(permission_ret)
    total = get_permission_query_total(db, name)
    content = {
        'permissions': permission_rets,
        'pageSize': page_size,
        'currentPage': current_page,
        'pageTotal': total
    }
    return content


# 修改
@router.post('/edit', tags=['权限模块'])
async def edit(
        permission: PermissionRet,
        token_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    permission_edit(db, permission)

    content = {'code': 200, 'msg': '更新成功'}
    return content


# 获取父级菜单
@router.get('/get_no_parent_names', tags=['权限模块'])
def get_no_parent_names(id: int, token_id: str = Depends(token.parse_token),
                        db: Session = Depends(get_db)):
    parent_names = get_permission_no_parent_names(db, id)
    content = {'code': 200, 'parent_names': parent_names}
    return content


# 获取父级菜单
@router.get('/get_parent_names', tags=['权限模块'])
def get_parent_names(token_id: str = Depends(token.parse_token),
                        db: Session = Depends(get_db)):
    parent_names = get_permission_parent_names(db)
    content = {'code': 200, 'parent_names': parent_names}
    return content

# 删除角色
@router.post('/delete', tags=['权限模块'])
def delete_permission(permission: PermissionRet,
                      token_id: str = Depends(token.parse_token),
                      db: Session = Depends(get_db)):
    id = permission.id
    delete_permission_by_id(db, id)
    return JSONResponse(content={
        'code': 200,
        'msg': '删除成功',
        # 'id': id
    })


# 添加角色
@router.post('/add', tags=['权限模块'])
async def add(permissions: PermissionRet,
              token_id: str = Depends(token.parse_token),
              db: Session = Depends(get_db)):
    permission_add(db, permissions)
    return JSONResponse(content={
        'code': 200,
        'msg': '添加成功',
    })
