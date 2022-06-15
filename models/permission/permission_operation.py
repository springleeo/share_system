# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.permission.permission_model import Permission
from models.permission.permission_ret_model import PermissionRet
from models.role.role_model import RoleUsers, RolePermissions


def get_permission_pagenation(db: Session, page_size: int, current_page: int) -> [Permission]:
    permissions = db.query(Permission.id, Permission.name, Permission.url, Permission.method, Permission.args,
                           Permission.parent_id, Permission.desc, Permission.icon, Permission.create_time).limit(
        page_size).offset(
        (current_page - 1) * page_size).all()
    return permissions


def get_permission_query_pagenation(db: Session, name: str, page_size: int, current_page: int) -> [Permission]:
    # departments = db.query(Department.id, Department.name, Department.leader, Department.desc,
    #                        Department.create_time).filter(Department.name == name).limit(
    #     page_size).offset((current_page - 1) * page_size).all()

    # 多条件或查询or_
    permissions = db.query(Permission.id, Permission.name, Permission.url, Permission.method, Permission.args,
                           Permission.parent_id, Permission.desc, Permission.icon, Permission.create_time).filter(
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
    permission.desc = permissions.desc
    permission.icon = permissions.icon
    if permissions.parent_name == '无':
        permission.parent_id = 0
    else:
        permission_by_parent_name = db.query(Permission).filter(Permission.name == permissions.parent_name).first()
        permission.parent_id = permission_by_parent_name.id

    db.commit()
    db.flush()


def get_permission_no_parent_names(db: Session, id: int) -> [Permission]:
    permission = db.query(Permission).filter(Permission.id == id).first()
    if permission.parent_id == 0:  # 一级菜单，父级菜单是无，显示其他父级菜单
        permissions = db.query(Permission).filter(Permission.id != permission.id, Permission.parent_id == 0).all()
    else:  # 二级菜单，显示所有父级菜单
        permissions = db.query(Permission).filter(Permission.parent_id == 0).all()
    return permissions


def get_permission_parent_names(db: Session) -> [Permission]:
    permissions = db.query(Permission).filter(Permission.parent_id == 0).all()
    return permissions


def delete_permission_by_id(db: Session, id: int):
    permission = db.query(Permission).filter(Permission.id == id).first()
    db.delete(permission)
    db.commit()
    db.flush()


def get_permission_by_id(db: Session, id: int):
    permission = db.query(Permission).filter(Permission.id == id).first()
    return permission


def permission_add(db: Session, permission: PermissionRet):
    if permission.parent_name == "无":
        permission = Permission(name=permission.name, url=permission.url, method=permission.method,
                                args=permission.args,
                                parent_id=0, desc=permission.desc)
    else:
        permission_by_parent_name = db.query(Permission).filter(Permission.name == permission.parent_name).first()
        permission = Permission(name=permission.name, url=permission.url, method=permission.method,
                                args=permission.args,
                                parent_id=permission_by_parent_name.id, desc=permission.desc)
    db.add(permission)
    db.commit()
    db.flush()




