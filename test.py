
import sqlite3
import re
dbpath = 'cosmetics.db'
# 连接数据库的操作
# item = "一般液态单元（护发清洁类、护肤水类、啫喱类）；膏霜乳液单元（护肤清洁类、护发类）"
#
#
# result = re.split('（|、|；|#|）',item)
# print(result)
# key_value = {}

# 初始化
# key_value[2] = 56
# key_value[1] = 2
# key_value[5] = 12
# key_value[4] = 24
# key_value[6] = 18
# key_value[3] = 323
#
# print("按值(value)排序:")
# key_value = sorted(key_value.items(), key=lambda kv: (kv[1], kv[0]),reverse=True)
# print(key_value[0][0])
# 连接数据库的操作
# 连接数据库的操作
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()

dataList = cursor.execute("select province, item from cosmetics order by province")
curprovince = ""
itemDict = {}  # {'广东':'护发清洁类','黑龙江':'发蜡类'}
tdict = {}
for data in dataList:
    province = data[0]
    if province != "黑龙江" and province != "内蒙古":
        province = province[0:2]
    if curprovince == "":
        # 刚开始
        curprovince = province
    else:
        strItem = str(data[1])  # 一般液态单元（护发清洁类、护肤水类、啫喱类）；膏霜乳液单元（护肤清洁类、护发类）‘
        itemList = re.split('（|、|；|#|）', strItem)
        # itemList = ['一般液态单元', '护发清洁类', '护肤水类', '啫喱类', '膏霜乳液单元', '护肤清洁类', '护发类', '']

        for item in itemList:
            # 是有效的可统计的类别
            if item.find("类") != -1:
                # eg. item = '护发清洁类'
                # 对当前省份继续统计
                if curprovince == province:
                    # eg.tdict = {'护发清洁类':2,'啫喱类':3}
                    #  这一类第一次统计
                    if tdict.get(item, -1) == -1:
                        tdict[item] = 1
                    # 这一类之前有记录数字
                    else:
                        tdict[item] += 1
                else:
                    # 新遍历到的省是另一个省了，需要写入刚刚那个省的统计结果到字典
                    # dict进行降序排序 maxItem = '护发清洁类'
                    stupleList = sorted(tdict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
                    # eg.stupleList = [('护肤水类', 7), ('护肤清洁类', 6),...]
                    maxItem = stupleList[0][0]
                    if stupleList[0][1] == stupleList[1][1]: # 若有并列
                        maxItem += '、'+stupleList[1][0]
                    # 字典里加键值对 '广东':'护发清洁类'
                    itemDict[curprovince] = maxItem
                    # 重置curprovince和tdict
                    curprovince = province
                    tdict.clear()

# dataList = cursor.execute(sql)
# dataDict = []
# dataJson = {}
# for data in dataList:
#     tdict = {}
#     province = data[0]
#     if province != "黑龙江" and province != "内蒙古":
#         province = province[0:2]
#     tdict['name'] = province
#     tdict['value'] = data[1]
#     dataDict.append(tdict)
#     dataJson[province] = data[1]
# print(dataJson)  # 测试
#
# # 关闭连接
# cursor.close()
# conn.close()