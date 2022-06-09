# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.permission.permission_model import Permission
from models.permission.permission_ret_model import PermissionRet


def get_permission_pagenation(db: Session, page_size: int, current_page: int) -> [Permission]:
    permissions = db.query(Permission.id, Permission.name, Permission.url, Permission.method, Permission.args,
                           Permission.parent_id, Permission.desc, Permission.create_time).limit(page_size).offset((current_page - 1) * page_size).all()
    return permissions


def get_permission_query_pagenation(db: Session, name: str, page_size: int, current_page: int) -> [Permission]:
    # departments = db.query(Department.id, Department.name, Department.leader, Department.desc,
    #                        Department.create_time).filter(Department.name == name).limit(
    #     page_size).offset((current_page - 1) * page_size).all()

    # 多条件或查询or_
    permissions = db.query(Permission.id, Permission.name, Permission.url, Permission.method, Permission.args,
                           Permission.parent_id, Permission.desc, Permission.create_time).filter(
        or_(Permission.name.like("%" + name + "%") if name is not None else "",
            Permission.desc.like("%" + name + "%") if name is not None else "")
    ).limit(page_size).offset((current_page - 1) * page_size).all()

    return permissions


def get_permission_total(db: Session) -> int:
    total = db.query(Permission).count()
    return total


# def get_permission_query_total(db: Session, name: str) -> int:
#     total = db.query(Permission).filter(Permission.name == name).count()
#     return total


def get_permission_query_total(db: Session, name: str) -> int:
    # 多条件或查询or_
    # total = db.query(Permission).filter(
    #     or_(Permission.name.like("%" + name + "%") if name is not None else "",
    #         Permission.desc.like("%" + name + "%") if name is not None else "")
    # ).count()

    total = db.query(Permission).filter(
        or_(Permission.name.like("%" + name + "%"),
            Permission.desc.like("%" + name + "%"))).count()
    return total


def permission_edit(db: Session, permissions: PermissionRet):
    permission = db.query(Permission).filter(Permission.id == permissions.id).first()
    permission.name = permissions.name
    permission.url = permissions.url
    permission.method = permissions.method
    permission.args = permissions.args
    permission.parent_id = permissions.parent_id
    permission.desc = permissions.desc
    db.commit()
    db.flush()


def delete_permission_by_id(db: Session, id: int):
    permission = db.query(Permission).filter(Permission.id == id).first()
    db.delete(permission)
    db.commit()
    db.flush()


def permission_add(db: Session, permission: PermissionRet):
    permission = Permission(name=permission.name, url=permission.url, method=permission.method, args=permission.args,
                            parent_id=permission.parent_id, desc=permission.desc)
    db.add(permission)
    db.commit()
    db.flush()
