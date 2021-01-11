# -*- coding = utf-8 -*-
# @Time = 2021/1/6 11:02
# @Author : Chen Yiling, Zhang Shiyu
# @File : main.py
# @Software : PyCharm

import sqlite3
import re
from flask import Flask, render_template

app = Flask(__name__)

# 数据库路径
dbpath = "cosmetics.db"


# 主页
@app.route('/')
def index():
    return render_template("index.html")


# 主页
@app.route('/index.html')
def index_2():
    return render_template("index.html")


# 分布_企业位置_Map
@app.route('/dist_loc')
def dist_loc():
    # 连接数据库的操作
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    sql = """
            select province as name,count(*) as value
            from cosmetics
            group by province
            order by value ;
        """
    dataList = cursor.execute(sql)
    dataDict = []
    dataJson = {}
    for data in dataList:
        tdict = {}
        province = data[0]
        if province != "黑龙江" and province != "内蒙古":
            province = province[0:2]
        tdict['name'] = province
        tdict['value'] = data[1]
        dataDict.append(tdict)
        dataJson[province] = data[1]

    print(dataDict)  # 测试

    # 关闭连接
    cursor.close()
    conn.close()

    return render_template("maps/map1.html", dataDict=dataDict,dataJson=dataJson)


# 分布_产品项目类型在位置上_Map
@app.route('/dist_item')
def dist_item():
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    dataList = cursor.execute("select province, item from cosmetics order by province").fetchall()
    curprovince = ""
    itemDict = {}  # {'广东':'护发清洁类','黑龙江':'发蜡类'}
    tdict = {}
    for i in range(len(dataList)):
        data = dataList[i]
        province = data[0]
        if province != "黑龙江" and province != "内蒙古":
            province = province[0:2]
        if curprovince == "":
            # 刚开始
            curprovince = province

        strItem = str(data[1])  # 一般液态单元（护发清洁类、护肤水类、啫喱类）；膏霜乳液单元（护肤清洁类、护发类）‘
        itemList = re.split('（|、|；|#|）', strItem)
        # itemList = ['一般液态单元', '护发清洁类', '护肤水类', '啫喱类', '膏霜乳液单元', '护肤清洁类', '护发类', '']

        for item in itemList:
            # 是有效的可统计的类别
            if item.find("类") != -1:
                # eg. item = '护发清洁类' XX类
                # 对当前省份继续统计
                if curprovince == province and i != len(dataList) - 1:
                    # eg.tdict = {'护发清洁类':2,'啫喱类':3}
                    #  这一类第一次统计
                    if tdict.get(item, -1) == -1:
                        tdict[item] = 1
                    # 这一类之前有记录数字
                    else:
                        tdict[item] += 1
                else:
                    # 新遍历到的省是另一个省了或是查询结果中最后的一个省，需要写入刚刚那个省的统计结果到字典
                    # dict进行降序排序 maxItem = '护发清洁类'
                    stupleList = sorted(tdict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
                    # eg.stupleList = [('护肤水类', 7), ('护肤清洁类', 6),...]
                    maxItem = stupleList[0][0]
                    if len(stupleList) > 1 and stupleList[0][1] == stupleList[1][1]:  # 若有并列
                        maxItem += '、' + stupleList[1][0]
                    # 字典里加键值对 '广东':'护发清洁类'
                    itemDict[curprovince] = maxItem
                    # 重置curprovince和tdict
                    curprovince = province
                    tdict.clear()

    # 数量随省分布的数据
    sql = """
                select province as name,count(*) as value
                from cosmetics
                group by province
                order by value ;
            """
    dataList = cursor.execute(sql)

    dataList_ord = []

    for data in dataList:
        tdict = {}
        province = data[0]
        if province != "黑龙江" and province != "内蒙古":
            province = province[0:2]
        tdict['name'] = province
        tdict['value'] = data[1]
        dataList_ord.append(tdict)



    cursor.close()
    conn.close()
    return render_template('maps/map2.html', dataList_ord=dataList_ord, itemDict=itemDict)



# 许可证_分发时间_Chart_Bar
@app.route('/cert_issue')
def cert_issue():
    # 连接数据库的操作
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    dataList = cursor.execute("select substr(date,1,7) as month,count(*) from cosmetics group by substr(date,1,7)")
    # [month, count]
    # [2020-01, 10]
    month = []
    mcount = []
    for data in dataList:
        month.append(data[0])
        mcount.append(data[1])
    print(month[0]) # 测试

    cursor.close()
    conn.close()
    return render_template("charts/charts.html", month=month, mcount=mcount)


# 许可证_有效时长_Chart_Pie
@app.route('/cert_life')
def cert_life():
    # 连接数据库的操作
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    sql = """
        select count(case when life >= 0 and life < 1 then 1 else null end) as '1年以内',
        count(case when life >= 1 and life < 2 then 1 else null end) as '1~2年',
        count(case when life >= 2 and life < 3 then 1 else null end) as '2~3年',
        count(case when life >= 3 and life < 4 then 1 else null end) as '3~4年',
        count(case when life >= 4 and life < 5 then 1 else null end) as '4~5年',
        count(case when life =  5 then 1 else null end) as '5年'
        from cosmetics;
    """
    # ['1年以内',100]
    dataList = cursor.execute(sql)
    length = ["<1年","1~2年","2~3年","3~4年","4~5年","5年"]
    lcount = []
    for data in dataList:
        for counts in data:
            lcount.append(counts)
    print(lcount[0])  # test
    cursor.close()
    conn.close()
    return render_template("charts/charts_2.html", length=length, lcount=lcount)


# 源数据表打印_datatable
@app.route('/tables/datatables')
def table():
    # 连接数据库的操作
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    dataList = list(cursor.execute("select name, num, province, office, date, life, item from cosmetics"))
        #[{'name': '海南卓瑞生物医药有限公司', 'num': '琼妆20190009', 'province': '海南省', 'office': '海南省药品监督管理局',
         #        'date': '2021-01-05', 'life': '1413', 'item': '一般液态单元（护肤水类）'}]

    print(dataList[0]) #test
    cursor.close()
    conn.close()
    return render_template("tables/datatables.html", dataList=dataList)


if __name__ == '__main__':
    app.run()
