# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, UploadFile, File, Form
# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from extend.get_db import get_db
from models.user.user_model import User
from models.user.user_ret_model import UserRet
from utils import token
from utils.get_md5_data import get_md5_pwd
from models.user.user_operation import get_user_pagenation, get_user_total, active, user_update

router = APIRouter(
    prefix='/user'
)


@router.get('/user_list', tags=['用户模块'])
def get_user_list(page_size: int, current_page: int, id: str = Depends(token.parse_token),
                  db: Session = Depends(get_db)):
    users = get_user_pagenation(db, page_size, current_page)
    total = get_user_total(db)
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


# 用户修改，涉及图片上传，用formdata的形式
@router.post('/update', tags=['用户模块'])
async def upload(avatar: UploadFile = File(...),
                 id: int = Form(...),
                 username: str = Form(...),
                 pwd: str = Form(...),
                 addr: str = Form(...),
                 state: int = Form(...),
                 create_time: str = Form(...),
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
    user_update(db, id, username, md5_pwd, addr, state, file_path)

    return {'code': 200, 'msg': '更新成功', 'id': id}
