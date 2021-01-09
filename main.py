# -*- coding = utf-8 -*-
# @Time = 2021/1/7 20:06
# @Author : Chen Yiling
# @File : main.py
# @Software : PyCharm
import spider, dao


def main():
    # 1. 爬取数据
    url = "http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList"
    data_list = spider.getDataFromUrl(url)

    # 2.创建数据库和表
    dbpath = "cosmetics.db"  # 数据库路径
    dao.init_db(dbpath)

    # 3.往表里插入数据
    dao.save2db(data_list, dbpath)


if __name__ == "__main__":
    main()
