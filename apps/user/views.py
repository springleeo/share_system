# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from extend.get_db import get_db
from models.user.user_model import User
from utils import token
from models.user.user_operation import get_user_pagenation, get_user_total

router = APIRouter(
    prefix='/user'
)


@router.get('/user_list')
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
