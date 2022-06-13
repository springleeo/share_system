# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from extend.get_db import get_db
from models.role.role_ret_model import RoleRet
from models.role.role_operation import get_role_pagenation, get_role_query_total, get_role_total, \
    get_role_query_pagenation, role_add, role_edit, delete_role_by_id, get_db_users, get_db_role_users, \
    save_db_config_users
from utils import token

router = APIRouter(
    prefix='/role'
)


@router.get('/role_list', tags=['角色模块'])
def get_role_list(page_size: int, current_page: int, id: str = Depends(token.parse_token),
                  db: Session = Depends(get_db)):
    roles = get_role_pagenation(db, page_size, current_page)
    total = get_role_total(db)
    content = {
        'roles': roles,
        'pageSize': page_size,
        'currentPage': current_page,
        'pageTotal': total
    }
    return content


@router.get('/query', tags=['角色模块'])
def get_role_query_list(name: str, page_size: int, current_page: int, token_id: str = Depends(token.parse_token),
                        db: Session = Depends(get_db)):
    roles = get_role_query_pagenation(db, name, page_size, current_page)
    total = get_role_query_total(db, name)
    content = {
        'roles': roles,
        'pageSize': page_size,
        'currentPage': current_page,
        'pageTotal': total
    }
    return content


# 修改
@router.post('/edit', tags=['角色模块'])
async def edit(
        department: RoleRet,
        token_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    role_edit(db, department)

    content = {'code': 200, 'msg': '更新成功'}
    return content


# 删除角色
@router.post('/delete', tags=['角色模块'])
def delete_role(role: RoleRet,
                token_id: str = Depends(token.parse_token),
                db: Session = Depends(get_db)):
    id = role.id
    delete_role_by_id(db, id)
    return JSONResponse(content={
        'code': 200,
        'msg': '删除成功',
        # 'id': id
    })


# 添加角色
@router.post('/add', tags=['角色模块'])
async def add(roles: RoleRet,
              token_id: str = Depends(token.parse_token),
              db: Session = Depends(get_db)):
    role_add(db, roles)
    return JSONResponse(content={
        'code': 200,
        'msg': '添加成功',
    })


# 获取所有用户列表
@router.get('/get_all_users', tags=['角色模块'])
def get_all_users(token_id: str = Depends(token.parse_token),
                  db: Session = Depends(get_db)):
    users = get_db_users(db)
    user_config_options = []
    for user in users:
        user_config_option = {
            'label': user.username,
            'value': user.id
        }
        user_config_options.append(user_config_option)
    return JSONResponse(content={
        'code': 200,
        'config_users_options': user_config_options,
    })


# 获取角色配置的用户列表
@router.get('/get_role_users', tags=['角色模块'])
def get_role_users(role_id: int,
                   token_id: str = Depends(token.parse_token),
                   db: Session = Depends(get_db)):
    role_users = get_db_role_users(db, role_id)
    config_users = []
    for role_user in role_users:
        config_users.append(role_user.user_id)
    return JSONResponse(content={
        'code': 200,
        'config_users': config_users,
    })


# 保存角色配置的用户列表
@router.post('/save_config_users', tags=['角色模块'])
def save_config_users(role_id: int = Form(...),
                      config_users: str = Form(...),
                      token_id: str = Depends(token.parse_token),
                      db: Session = Depends(get_db)):
    save_db_config_users(db, role_id, config_users.split(','))
    return JSONResponse(content={
        'code': 200,
    })
