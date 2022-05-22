# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.role.role_model import Role
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
