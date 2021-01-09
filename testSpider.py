# -*- coding= utf-8 -*-
# @Time : 2021/1/5 14:32


import requests
import json
if __name__=="__main__":
    url="http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList"
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }
    id_list = []
    for page in range(1,10):
        data={
            'on': 'true',
            'page':page,
            'pageSize': '15',
            'productName':'',
            'conditionType': '1',
            'applyname':'',
            'applysn':'',
        }
        json_id = requests.post(url=url, data=data, headers=header).json()
        for dic in json_id['list']:
            id_list.append(dic['ID'])
    data_list=[]
    post_url='http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
    for id in id_list:
        Data={
            'id':id
        }
        data_json=requests.post(url=post_url,headers=header,data=Data).json()
        data_list.append(data_json)
    fp=open('./data.json','w',encoding='utf-8')
    json.dump(data_list,fp=fp,ensure_ascii=False)
    print('succeed----------')








