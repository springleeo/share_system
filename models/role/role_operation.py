# -*- coding: utf-8 -*-
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.permission.permission_model import Permission
from models.role.role_model import Role, RoleUsers, RolePermissions
from models.user.user_model import User
from models.role.role_ret_model import RoleRet


def get_role_pagenation(db: Session, page_size: int, current_page: int) -> [Role]:
    roles = db.query(Role.id, Role.name, Role.desc,
                     Role.create_time).limit(page_size).offset((current_page - 1) * page_size).all()
    return roles


def get_role_query_pagenation(db: Session, name: str, page_size: int, current_page: int) -> [Role]:
    # departments = db.query(Department.id, Department.name, Department.leader, Department.desc,
    #                        Department.create_time).filter(Department.name == name).limit(
    #     page_size).offset((current_page - 1) * page_size).all()

    # 多条件或查询or_
    roles = db.query(Role.id, Role.name, Role.desc,
                     Role.create_time).filter(
        or_(Role.name.like("%" + name + "%") if name is not None else "",
            Role.desc.like("%" + name + "%") if name is not None else "")
    ).limit(page_size).offset((current_page - 1) * page_size).all()

    return roles


def get_role_total(db: Session) -> int:
    total = db.query(Role).count()
    return total


# def get_role_query_total(db: Session, name: str) -> int:
#     total = db.query(Role).filter(Role.name == name).count()
#     return total


def get_role_query_total(db: Session, name: str) -> int:
    # 多条件或查询or_
    # total = db.query(Role).filter(
    #     or_(Role.name.like("%" + name + "%") if name is not None else "",
    #         Role.desc.like("%" + name + "%") if name is not None else "")
    # ).count()

    total = db.query(Role).filter(
        or_(Role.name.like("%" + name + "%"),
            Role.desc.like("%" + name + "%"))).count()
    return total


def role_edit(db: Session, roles: RoleRet):
    role = db.query(Role).filter(Role.id == roles.id).first()
    role.name = roles.name
    role.desc = roles.desc
    db.commit()
    db.flush()


def delete_role_by_id(db: Session, id: int):
    role = db.query(Role).filter(Role.id == id).first()
    db.delete(role)
    db.commit()
    db.flush()


def role_add(db: Session, role: RoleRet):
    role = Role(name=role.name, desc=role.desc, )
    db.add(role)
    db.commit()
    db.flush()


def get_db_users(db: Session):
    users = db.query(User.id, User.username).filter(User.state == 1).all()
    return users


def get_db_role_users(db: Session, role_id: int) -> [RoleUsers]:
    role_users = db.query(RoleUsers.user_id).filter(RoleUsers.role_id == role_id).all()
    return role_users


def save_db_config_users(db: Session, role_id: int, config_users: [int]):
    role_users = db.query(RoleUsers).filter(RoleUsers.role_id == role_id).delete(synchronize_session=False)
    db.commit()
    role_users_list = []
    for i in config_users:
        role_users_list.append(RoleUsers(role_id=role_id, user_id=i))
    db.add_all(role_users_list)
    db.commit()


# {
#     id: 1,
#     label: '用户管理',
#     children: [
#         {
#             id: 4,
#             label: '用户列表',
#             children: []
#         }
#     ]
# },
def get_db_permissions_info(db: Session, role_id: int):
    tree = []
    permissions = db.query(Permission).filter(Permission.parent_id == 0).all()
    for permission in permissions:
        first_level = {
            'id': permission.id,
            'label': permission.name,
            'children': []
        }

        next_permission = db.query(Permission).filter(Permission.parent_id == permission.id).all()
        if next_permission:
            first_level['children'] = get_children(db, next_permission)
        tree.append(first_level)

    role_permissions = db.query(RolePermissions.permission_id).filter(RolePermissions.role_id == role_id).all()
    checked_permissions = [p.permission_id for p in role_permissions]

    return {'permissions_tree': tree, 'checked_permissions': checked_permissions}


def get_children(db: Session, permission: [Permission]):
    children = []
    for child in permission:
        next_child = {
            'id': child.id,
            'label': child.name,
            'children': []
        }
        next_permission = db.query(Permission).filter(Permission.parent_id == child.id).all()
        if next_permission:
            next_child['children'] = get_children(db, next_permission)
        children.append(next_child)
    return children


def save_db_permission_config(db: Session, role_id: int, selected_permissions: [int]):
    db.query(RolePermissions).filter(RolePermissions.role_id == role_id).delete(synchronize_session=False)
    db.commit()
    role_permissions_list = []
    for i in selected_permissions:
        role_permissions_list.append(RolePermissions(role_id=role_id, permission_id=i))
    db.add_all(role_permissions_list)
    db.commit()
