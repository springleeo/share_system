# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from models.user.user_model import User, Department
from models.user.user_ret_model import UserRet
from typing import Optional
import datetime


def get_user_by_username_and_pwd(db: Session, username: str, md5_pwd: str) -> User:
    user = db.query(User).filter(
        User.username == username,
        User.pwd == md5_pwd).first()
    return user


def update_login_time_and_ip(db: Session, user_id: int, login_date: datetime.datetime, ip: str):
    user = db.query(User).filter(User.id == user_id).first()
    user.last_login_date = login_date
    user.ip = ip
    db.commit()
    db.flush()


def get_user_by_id(db: Session, id: int) -> User:
    user = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date).filter(User.id == id).first()
    return user


def get_user_pagenation(db: Session, page_size: int, current_page: int) -> [User]:
    users = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date, User.addr, User.state,
                     User.create_time, User.dep_id, Department.name).join(Department).limit(
        page_size).offset((current_page - 1) * page_size).all()
    return users


def get_user_query_pagenation(db: Session, username: str, department_name: str, page_size: int, current_page: int) -> [
    User]:
    department = db.query(Department).filter(Department.name == department_name).first()
    if department:
        if username:
            users = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date, User.addr, User.state,
                             User.create_time, User.dep_id, Department.name) \
                .join(Department) \
                .filter(User.username.like('%' + username + '%'), User.dep_id == department.id) \
                .limit(page_size) \
                .offset((current_page - 1) * page_size).all()
        else:
            users = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date, User.addr, User.state,
                             User.create_time, User.dep_id, Department.name) \
                .join(Department) \
                .filter(User.dep_id == department.id) \
                .limit(page_size) \
                .offset((current_page - 1) * page_size).all()
    else:
        if username:
            users = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date, User.addr, User.state,
                             User.create_time, User.dep_id, Department.name) \
                .filter(User.username.like('%' + username + '%')) \
                .limit(page_size) \
                .offset((current_page - 1) * page_size).all()
        else:
            users = get_user_pagenation(db, page_size, current_page)
    return users


def get_user_total(db: Session, ) -> int:
    total = db.query(User).count()
    return total


def get_user_query_total(db: Session, username: str, department_name: str) -> int:
    department = db.query(Department).filter(Department.name == department_name).first()
    if department:
        if username:
            total = db.query(User).filter(User.username.like('%' + username + '%'), User.dep_id == department.id).count()
        else:
            total = db.query(User).filter(User.dep_id == department.id).count()
    else:
        if username:
            total = db.query(User).filter(User.username.like('%' + username + '%')).count()
        else:
            total = db.query(User).count()
    return total


def active(db: Session, id: int, state: int):
    user = db.query(User).filter(User.id == id).first()
    user.state = state
    db.commit()
    db.flush()


def user_update(db: Session, id: int, username: str, pwd: str, addr: str, state: int, avatar: str,
                department_name: str):
    department = db.query(Department).filter(Department.name == department_name).first()
    user = db.query(User).filter(User.id == id).first()
    user.username = username
    if pwd:
        user.pwd = pwd
    user.addr = addr
    user.state = state
    user.avatar = '/' + avatar
    user.dep_id = department.id
    db.commit()
    db.flush()


def user_add(db: Session, username: str, pwd: str, addr: str, state: int, avatar: str, department_name: str):
    department = db.query(Department).filter(Department.name == department_name).first()
    user = User(username=username,
                pwd=pwd,
                avatar='/' + avatar,
                addr=addr,
                state=state,
                dep_id=department.id)
    db.add(user)
    db.commit()
    db.flush()


def delete_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    db.delete(user)
    db.commit()
    db.flush()


def get_departments(db: Session):
    departments = db.query(Department.name).all()
    return departments


def get_departments_except_me(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    departments = db.query(Department).filter(Department.id != user.dep_id).all()
    return departments
