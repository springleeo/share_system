# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from extend.get_db import get_db
from models.user.user_model import User
from models.user.user_ret_model import UserRet
from utils import token
from utils.get_md5_data import get_md5_pwd
from models.user.user_operation import get_user_pagenation, get_user_total, active, user_update, delete_user_by_id, \
    user_add, get_user_query_pagenation, get_user_query_total, get_departments, get_departments_except_me, \
    get_user_by_id

router = APIRouter(
    prefix='/user'
)


@router.get('/user_list', tags=['用户模块'])
def get_user_list(page_size: int, current_page: int, id: str = Depends(token.parse_token),
                  db: Session = Depends(get_db)):
    users = get_user_pagenation(db, page_size, current_page)
    total = get_user_total(db)
    departments = get_departments(db)  # 用于前端选择部门时展示
    content = {
        'users': users,
        'pageSize': page_size,
        'currentPage': current_page,
        'pageTotal': total,
        'departments': departments
    }
    return content


@router.get('/query', tags=['用户模块'])
def get_user_query_list(username: str, department_name: str, page_size: int, current_page: int,
                        id: str = Depends(token.parse_token),
                        db: Session = Depends(get_db)):
    users = get_user_query_pagenation(db, username, department_name, page_size, current_page)
    total = get_user_query_total(db, username, department_name)

    content = {
        'users': users,
        'pageSize': page_size,
        'currentPage': current_page,
        'pageTotal': total
    }
    return content


@router.post('/active', tags=['用户模块'])
def active_user(user: UserRet, id: str = Depends(token.parse_token), db: Session = Depends(get_db)):
    if user.state == 1:
        state = 2
    else:
        state = 1

    active(db, user.id, state)
    if user.state == 1:
        return {'code': 200, 'msg': '停用成功', 'state': 1}
    if user.state == 2:
        return {'code': 200, 'msg': '启用成功', 'state': 2}


# 添加用户
@router.post('/add', tags=['用户模块'])
async def add(avatar: UploadFile = File(...),
              username: str = Form(...),
              department_name: str = Form(...),
              pwd: str = Form(...),
              addr: str = Form(...),
              state: int = Form(...),
              user_id: str = Depends(token.parse_token),
              db: Session = Depends(get_db)):
    rep = await avatar.read()
    file_path = 'uploads/users/' + avatar.filename
    with open(file_path, 'wb') as f:
        f.write(rep)
    md5_pwd = get_md5_pwd(pwd)
    user_add(db, username, md5_pwd, addr, state, file_path, department_name)
    return JSONResponse(content={
        'code': 200,
        'msg': '添加成功',
    })


# 用户修改，涉及图片上传，用formdata的形式
@router.post('/edit', tags=['用户模块'])
async def edit(avatar: UploadFile = File(...),
               id: int = Form(...),
               username: str = Form(...),
               pwd: str = Form(...),
               addr: str = Form(...),
               state: int = Form(...),
               department_name: str = Form(...),
               # create_time: str = Form(...),
               user_id: str = Depends(token.parse_token),
               db: Session = Depends(get_db)):
    rep = await avatar.read()
    file_path = 'uploads/users/' + avatar.filename
    with open(file_path, 'wb') as f:
        f.write(rep)
    if pwd:
        md5_pwd = get_md5_pwd(pwd)
    else:
        md5_pwd = None
    user_update(db, id, username, md5_pwd, addr, state, file_path, department_name)

    return {'code': 200, 'msg': '更新成功', 'id': id}


@router.post('/delete', tags=['用户模块'])
def delete_user(user: UserRet,
                user_id: str = Depends(token.parse_token),
                db: Session = Depends(get_db)):
    id = user.id
    delete_user_by_id(db, id)
    return JSONResponse(content={
        'code': 200,
        'msg': '删除成功',
        'id': id
    })


# 获取所有的部门
@router.get('/get_departments', tags=['用户模块'])
def get_department(user_id: str = Depends(token.parse_token),
                   db: Session = Depends(get_db)):
    departments = get_departments(db)
    return {
        'code': 200,
        'msg': '查询成功',
        'departments': departments
    }


# 获取除自己以外的所有部门
@router.get('/get_departments_except_me', tags=['用户模块'])
def get_department_except(
        id: int,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    departments = get_departments_except_me(db, id)
    return {
        'code': 200,
        'msg': '查询成功',
        'departments': departments
    }


# 获取用户头像
@router.get('/get_avatar', tags=['用户模块'])
def get_avatar(user_id: str = Depends(token.parse_token),
               db: Session = Depends(get_db)):
    user = get_user_by_id(db, int(user_id))
    return {
        'code': 200,
        'avatar': user.avatar,
    }
