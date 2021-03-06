# -*- coding: utf-8 -*-
import pathlib
from typing import Dict

import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from starlette.staticfiles import StaticFiles
from apps.user.views import router as user_router
from apps.department.views import router as department_router
from apps.role.views import router as role_router
from apps.permission.views import router as permission_router
from extend.db import Engine, LocalSession, Base
from extend.get_db import get_db
from utils.get_md5_data import get_md5_pwd
from utils import token
from models.user.user_operation import get_user_by_username_and_pwd, get_user_by_id, update_login_time_and_ip

app = FastAPI(
    title='文件共享系统',
    description='文件共享系统',
    docs_url=None,
    redoc_url=None
)

app.include_router(user_router)
app.include_router(department_router)
app.include_router(role_router)
app.include_router(permission_router)

# 静态文件
app.mount("/uploads", StaticFiles(directory=str(pathlib.Path(__file__).parent.absolute()) + '/uploads'), name="uploads")

# token过期时间
EXPIRE_MINUTE = 60

# 跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=['*'],
)

# 创建数据库表结构
Base.metadata.create_all(Engine)


@app.post('/login', tags=['登陆模块'])
def login(request: Request, user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1.用户信息获取
    username = user.username
    # 密码加密
    pwd = user.password
    md5_pwd = get_md5_pwd(pwd)
    # 2.数据库校验
    user = get_user_by_username_and_pwd(db, username, md5_pwd)

    if user:
        if user.state == 2:
            content = {'code': 500, 'msg': '用户已停用，请联系管理员！'}
            return JSONResponse(content=content)
        # 3.token生成
        expire_time = timedelta(minutes=EXPIRE_MINUTE)
        ret_token = token.create_token({'sub': str(user.id)}, expire_time)
        # 4.返回token及用户信息，日期格式转化
        ret_user = {'username': user.username, 'avatar': user.avatar, 'ip': user.ip,
                    'expire_time': user.last_login_date.strftime('%Y-%m-%d')
                    }
        last_date = datetime.now()
        update_login_time_and_ip(db, user.id, last_date, request.client.host)
        content = {'code': 200, 'msg': '登陆成功', 'token': ret_token, 'user': ret_user}
        return JSONResponse(content=content)
    else:
        content = {'code': 500, 'msg': '用户名或密码错误'}
        return JSONResponse(content=content)


@app.get('/index', tags=['首页模块'])
def index(id: str = Depends(token.parse_token), db: Session = Depends(get_db)):
    # 根据token解析出来的id查询数据库
    user = get_user_by_id(db, id=int(id))
    # todo 图表数据需要从数据库查询
    schart_data = {
        'labels': ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        'datas': [
            [90, 78, 31, 33, 145, 234, 278, 270, 190, 230, 213, 110],
            [90, 56, 69, 52, 111, 164, 178, 150, 135, 160, 267, 110],
            [90, 235, 200, 114, 145, 74, 218, 100, 135, 190, 112, 110]
        ]
    }
    content = {
        'user': user,
        'role': '管理员',
        # todo 数据需要从数据库查询
        'totalFiles': 1000,
        'shareFiles': 900,
        'personalFiles': 10,
        'adminPer': 5,
        'puPer': 25,
        'staffPer': 70,
        'schart_data': schart_data

    }
    return content


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/uploads/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/uploads/swagger-ui/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True, host='0.0.0.0', port=8080)
