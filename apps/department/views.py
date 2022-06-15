# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from extend.get_db import get_db
from models.department.department_ret_model import DepartmentRet
from utils import token
from utils.get_md5_data import get_md5_pwd
from models.department.department_operation import get_department_pagenation, get_department_query_pagenation, \
    get_department_total, get_department_query_total, department_edit, delete_department_by_id, department_add

router = APIRouter(
    prefix='/department'
)


@router.get('/department_list', tags=['部门模块'])
def get_department_list(page_size: int, current_page: int, id: str = Depends(token.parse_token),
                        db: Session = Depends(get_db)):
    departments = get_department_pagenation(db, page_size, current_page)
    total = get_department_total(db)
    # print(departments)
    content = {
        'departments': departments,
        'pageSize': page_size,
        'currentPage': current_page,
        'pageTotal': total
    }
    return content


@router.get('/query', tags=['部门模块'])
def get_department_query_list(name: str, page_size: int, current_page: int, id: str = Depends(token.parse_token),
                              db: Session = Depends(get_db)):
    departments = get_department_query_pagenation(db, name, page_size, current_page)
    total = get_department_query_total(db, name)
    # print(departments)
    content = {
        'departments': departments,
        'pageSize': page_size,
        'currentPage': current_page,
        'pageTotal': total
    }
    return content


# 部门修改
@router.post('/edit', tags=['部门模块'])
async def edit(
        department: DepartmentRet,
        token_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    department_edit(db, department)

    content = {'code': 200, 'msg': '更新成功'}
    return content


#
# @router.post('/active', tags=['部门模块'])
# def active_user(department: DepartmentRet, id: str = Depends(token.parse_token), db: Session = Depends(get_db)):
#     if department.state == 1:
#         active(db, department.id, state=2)
#         return {'code': 200, 'msg': '停用成功', 'state': 2}
#     if department.state == 2:
#         active(db, department.id, state=1)
#         return {'code': 200, 'msg': '启用成功', 'state': 1}


@router.post('/delete', tags=['部门模块'])
def delete_user(department: DepartmentRet,
                token_id: str = Depends(token.parse_token),
                db: Session = Depends(get_db)):
    id = department.id
    delete_department_by_id(db, id)
    return JSONResponse(content={
        'code': 200,
        'msg': '删除成功',
        # 'id': id
    })


# 添加用户
@router.post('/add', tags=['部门模块'])
async def add(departments: DepartmentRet,
              user_id: str = Depends(token.parse_token),
              db: Session = Depends(get_db)):
    department_add(db, departments)
    return JSONResponse(content={
        'code': 200,
        'msg': '添加成功',
    })


