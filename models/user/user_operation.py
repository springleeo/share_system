# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from models.user.user_model import User
from models.user.user_ret_model import UserRet
from typing import Optional


def get_user_by_username_and_pwd(db: Session, username: str, md5_pwd: str) -> User:
    user = db.query(User).filter(
        User.username == username,
        User.pwd == md5_pwd).first()
    return user


def get_user_by_id(db: Session, id: int) -> User:
    user = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date).filter(User.id == id).first()
    return user


def get_user_pagenation(db: Session, page_size: int, current_page: int) -> [User]:
    users = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date, User.addr, User.state,
                     User.create_time).limit(
        page_size).offset((current_page - 1) * page_size).all()
    return users


def get_user_total(db: Session) -> int:
    total = db.query(User).count()
    return total


def active(db: Session, id: int, state: int):
    user = db.query(User).filter(User.id == id).first()
    user.state = state
    db.commit()
    db.flush()


def user_update(db: Session, id: int, username: str, pwd: str, addr: str, state: int, avatar: str):
    user = db.query(User).filter(User.id == id).first()
    user.username = username
    if pwd:
        user.pwd = pwd
    user.addr = addr
    user.state = state
    user.avatar = '/' + avatar
    db.commit()
    db.flush()
