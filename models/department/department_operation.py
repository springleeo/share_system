# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from models.user.user_model import Department
from models.department.department_ret_model import DepartmentRet
from typing import Optional
import datetime


# def get_user_by_username_and_pwd(db: Session, username: str, md5_pwd: str) -> User:
#     user = db.query(User).filter(
#         User.username == username,
#         User.pwd == md5_pwd).first()
#     return user

#
# def update_login_time_and_ip(db: Session, user_id: int, login_date: datetime.datetime, ip: str):
#     user = db.query(User).filter(User.id == user_id).first()
#     user.last_login_date = login_date
#     user.ip = ip
#     db.commit()
#     db.flush()


# def get_user_by_id(db: Session, id: int) -> User:
#     user = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date).filter(User.id == id).first()
#     return user


def get_department_pagenation(db: Session, page_size: int, current_page: int) -> [Department]:
    users = db.query(Department.id, Department.name, Department.leader, Department.desc,
                     Department.create_time).limit(page_size).offset((current_page - 1) * page_size).all()
    return users


def get_department_query_pagenation(db: Session, name: str, page_size: int, current_page: int) -> [Department]:
    departments = db.query(Department.id, Department.name, Department.leader, Department.desc,
                           Department.create_time).filter(Department.name == name).limit(
        page_size).offset((current_page - 1) * page_size).all()
    return departments


def get_department_total(db: Session) -> int:
    total = db.query(Department).count()
    return total


def get_department_query_total(db: Session, name: str) -> int:
    total = db.query(Department).filter(Department.name == name).count()
    return total


def department_edit(db: Session, departments: DepartmentRet):
    department = db.query(Department).filter(Department.id == departments.id).first()
    department.name = departments.name
    department.leader = departments.leader
    department.desc = departments.desc
    # department.state = departments.state
    db.commit()
    db.flush()


# def active(db: Session, id: int, state: int):
#     department = db.query(Department).filter(Department.id == id).first()
#     department.state = state
#     db.commit()
#     db.flush()


def delete_department_by_id(db: Session, id: int):
    department = db.query(Department).filter(Department.id == id).first()
    db.delete(department)
    db.commit()
    db.flush()


def department_add(db: Session, department: DepartmentRet):
    department = Department(name=department.name,
                            leader=department.leader,
                            desc=department.desc,
                            )
    db.add(department)
    db.commit()
    db.flush()
