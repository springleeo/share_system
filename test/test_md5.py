# -*- coding: utf-8 -*-
from utils.get_md5_data import get_md5_pwd

if __name__ == '__main__':
    pwd = 'test'
    pwd_md5 = get_md5_pwd(pwd)
    print(pwd_md5)
