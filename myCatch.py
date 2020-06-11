# -*- coding: UTF-8 -*-
import urllib.request
import random
import json
import re
import pandas as pd
import time
import pymysql
class catch():
    def __init__(self):
        #pd.set_option('display.max_rows', None)  # 显示所有的行
        #pd.set_option('display.max_columns', None)  # 显示所有的列
        #pd.set_option('max_colwidth', 30)  # 设置列的最大默认宽度
        self.times = time.strftime("%m_%d_%H_%M_%S", time.localtime())#获取当前时间并且格式化
        self.db = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="info", charset="utf8mb4")
        self.cursor = self.db.cursor()#建立游标

    def proxy(self):
        # 代理IP列表随机抽取
        #m免费代理ip自行百度
        proxy_list = [{"http": "220.168.52.245:55255"},
                      {"http": "124.193.135.242:54219"},
                      {"http": "36.7.128.146:52222"},
                      {"http":"125.108.69.212:9000"},
                      {"http":"163.125.28.163:8118"},
                      {"http":"59.62.26.158:9000"},
                      {"http":"125.108.88.166:9000"},
                      {"http":"117.87.177.231:9000"},
                      {"http":"123.101.67.81:9999"},
                      {"http":"175.42.128.186:9999"},
                      {"http": "117.69.12.139:9999"},
                      {"http": "171.35.162.210:9999"},
                      {"http": "1.199.30.42:9999"},
                      {"http": "113.195.225.96:9999"},
                      {"http":"110.243.10.85:9999"},
                      {"http":"119.254.94.71:55320"},
                      {"http":"219.159.38.207:56210"}
                      ]
        # 随机选择一个代理
        proxy = random.choice(proxy_list)
        return proxy

    def get_sinceid(self,old_sinceid):#获取构造url的关键部分since_id
        data=self.catchData(old_sinceid)
        since_id = json.loads(data).get("data").get("cardlistInfo").get("since_id")
        return since_id

    def catchData(self,sinceid):#利用代理IP和伪装浏览器头部信息获取访问url
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
        url = "https://m.weibo.cn/api/container/getIndex?uid=2656274875&type=uid&value=2656274875&containerid=1076032656274875&since_id="+str(sinceid)
        proxy=self.proxy()
        httpproxy_handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(httpproxy_handler)
        request = urllib.request.Request(url, headers=header)
        response = opener.open(request)
        data = response.read().decode('utf-8', 'ignore')
        return data


    def putOut(self,since_id):#程序关键部分，获取标准化数据，并插入MySQL
        dataframe = pd.DataFrame(#构造Dataframe
            {'time': [], 'supportNumber': [], 'commentNumber': [], 'repostsNumber': [], 'text': []})
        num = len(dataframe)
        data=self.catchData(since_id)#从函数中返回json数据
        #解析json数据
        data_card = json.loads(data).get("data").get("cards")
        num1=len(data_card)
        since_id = json.loads(data).get("data").get("cardlistInfo").get("since_id")
        for i in range(0, num1):
            datas=data_card[i].get("mblog")
            if datas==None:
                continue
            else:
                attitudes_count = datas.get('attitudes_count')
                comments_count = datas.get('comments_count')
                reposts_count = datas.get('reposts_count')
                create_time = datas.get('created_at')
                text = datas.get('text')
                #利用正则表达式去除不规范的文本信息
                text = re.sub(r'<a.*?</a>', "", text)
                text = re.sub(r'【.*?】', "", text)
                text = re.sub(r'<span.*?</span>', "", text)
                dataRows = [create_time, attitudes_count, comments_count, reposts_count, text]
                datas_sql = '("' + str(create_time) + '",' + str(attitudes_count) + ',' + str(comments_count) + ',' + str(reposts_count) + ',"' + str(text) + '")'
                dataframe.loc[num + i] = dataRows #在dataframe中插入数据
                self.add_sql(datas_sql)#插入数据到数据库
        print(dataframe)
        print("since_id:",since_id)

    def add_sql(self,data):#利用sql语句插入数据
        try:
            insert_sql = "INSERT INTO " + str(self.times) + "(time,supportnumber,commentnumber,repostnumber,text)  VALUES " + data+";"
            self.cursor.execute(insert_sql)
            self.db.commit()
        except:
            print("a data err")


    def sql(self):#创建表
        sql="create table if not exists "+str(self.times)+" (time varchar(30) not null,supportnumber int not null,commentnumber int not null,repostnumber int  not null, text varchar(1000) not null)engine=InnoDB default charset=utf8mb4;"
        self.cursor.execute(sql)


    def run(self):
        self.sql()
        since_id=""
        i=1
        while True:#建立死循环直到获取到所有数据，免cookie获取的情况下较为稳定，一般情况不会出错
            try:
                print("第"+str(i)+"页")
                self.putOut(since_id)
                since_id = self.get_sinceid(since_id)
                time.sleep(5)
                i+=1
            except:
                print("a page error")


if __name__=="__main__":
    d=catch()
    d.run()

#只显示2020年以来的数据
