# -*- coding = utf-8 -*-
# @Time = 2021/1/5 20:07
# @Author : Bai Xiaohan, Xu Feng
# @File : dao.py
# @Software : PyCharm

import sqlite3
import datetime


# 初始化 创建数据库
def init_db(dbpath):
    conn = sqlite3.connect(dbpath)
    print("Opened database successfully when initiating")
    cursor = conn.cursor()

    # 建表
    # id, name, num(许可证编号)，province, office, date, life,item(许可项目)
    cursor.execute("drop table if exists cosmetics; --如果表存在则删除")
    conn.commit()

    sql = """
        create table if not exists cosmetics
        (
        id varchar primary key,
        name varchar,
        num varchar,
        province varchar,
        office varchar,
        date varchar,
        life float,
        item varchar
        )
    """
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table created successfully")


def save2db(datalist, dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    print("Opened database successfully when saving")
    for data in datalist:
        # data是一个字典
        # 处理province 取发证机关前三个字
        province = data['qfManagerName'][0:3]
        # 处理life
        date_begin = data['xkDateStr']  # 2021-01-06
        date_end = data['xkDate']
        date_begin = datetime.date(int(date_begin[:4]), int(date_begin[5:7]), int(date_begin[8:10]))
        date_end = datetime.date(int(date_end[:4]), int(date_end[5:7]), int(date_end[8:10]))
        life = ((date_end - date_begin).days) / 365.0

        sql = """
            insert into cosmetics(id,name,num,province,office,date,life,item)
            values(%s,%s,%s,%s,%s,%s,%f,%s)
        """ % ('"' + data['businessLicenseNumber'] + '"', '"' + data['epsName'] + '"', '"' + data['productSn'] + '"',
               '"' + province + '"', '"' + data['qfManagerName'] + '"',
               '"' + data['xkDateStr'] + '"', life, '"' + data['certStr'] + '"')

        try:
            cursor.execute(sql)
        except:
            exit(0)
        conn.commit()

    cursor.close()
    conn.close()
    print("Records created successfully")
