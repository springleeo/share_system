# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


# 生成token:用户数据，token过期时间
def create_token(data: dict, expire_time):
    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    data.update({'exp': expire})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


oauth_schema = OAuth2PasswordBearer(tokenUrl='login')


# 校验token
def parse_token(token: str = Depends(oauth_schema)):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token不正确或已过期',
        headers={'WWW-Authenticate': 'Beater'}
    )
    try:
        jwt_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = jwt_data.get('sub')
        if id is None or id == "":
            raise token_exception
    except JWTError:
        raise token_exception
    return id
