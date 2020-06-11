import pandas as pd
import pymysql
from sqlalchemy import create_engine
import numpy as np
class Deal():
    def __init__(self):
        self.db = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="info", charset="utf8mb4")
        self.conn = create_engine('mysql+mysqlconnector://root:123456@127.0.0.1:3306/info')#需要下载一个软件mysql_connector到电脑上，或者用pymysql会有警告
        pd.set_option('display.max_columns', None)
    def deal1(self):
        # 将获取到的数据规范化
        sql = "select * from 06_10_15_54_41 where text is not null"
        frame = pd.read_sql(sql, self.conn)
        for i in ["2019", "前", "01-1", "01-0"]:
            frame = frame[~frame["time"].str.contains(i)]  # 除去time中包含“2019”的行
        frame = frame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)  # 删除缺失值
        frame.time[frame["time"].str.contains("昨天")] = "06-09"  # 把昨天换成6月9日
        frame["concludeCovid"] = 0
        #建立简单的数据字典
        word_list = ["湖北籍", "新冠", "肺炎", "新型冠状", "病毒", "国家卫健委", "发烧",
                     "发热", "病例", "输入", "疫情", "口罩", "确诊", "疫", "钟南山", "张文宏",
                     "李兰娟", "隔离", "接触者", "呼吸道", "核酸检测", "感染", "传染", "患者",
                     "死亡", "重症", "医护", "管控", "防控", "消毒", "前线", "复工", "复产", "隔座售票", "驰援"]
        for k in word_list:
            frame.concludeCovid[frame["text"].str.contains(k)] = 1
        frame = frame.sort_values(ascending=True, by="time")#重新排序
        print(frame)
        frame.to_sql(name="data_improve", con=self.conn, index=False, if_exists='replace')

    def deal2(self):
        #将数据汇总
        sql = "select * from data_improve"
        frame = pd.read_sql(sql, self.conn)
        frame["WeiboNum"] = 1
        frame["CovidPrecent"] = 0
        # size=frame.groupby("time").describe()
        SumData = frame.groupby("time").agg({"sum"})#将数据进行按日期汇总
        SumData.reset_index(level=0, inplace=True)
        improveData=pd.DataFrame({"time":list(SumData['time']),"SupportSum":list(SumData["supportnumber"]["sum"]),
                                  "CommentSum":list(SumData["commentnumber"]["sum"]),"RepostSum":list(SumData["repostnumber"]["sum"]),
                                  "CovidSum":list(SumData["concludeCovid"]["sum"]),"WeiboSum":list(SumData["WeiboNum"]["sum"])})
        #新建几个指标
        improveData['CovidPrecent']=np.array(improveData["CovidSum"])/np.array(improveData["WeiboSum"])
        improveData['AverageSupport'] = np.array(improveData["SupportSum"]) / np.array(improveData["WeiboSum"])
        improveData['AverageComment'] = np.array(improveData["CommentSum"]) / np.array(improveData["WeiboSum"])
        improveData['AverageRepost'] = np.array(improveData["RepostSum"]) / np.array(improveData["WeiboSum"])
        improveData['CommSupportRatio'] = np.array(improveData["CommentSum"]) / np.array(improveData["SupportSum"])
        improveData['RepoSupportRatio'] = np.array(improveData["RepostSum"]) / np.array(improveData["SupportSum"])
        print(improveData)
        improveData.to_sql(name="data_sum",con=self.conn, index=False, if_exists='replace')#存回数据库


        #a=dict(SumData).get("('supportnumber', 'sum')")
        # covid=frame.groupby("time",as_index=False).agg({"concludeCovid":"sum"})
        # SumData=SumData.rename(columns=["SupportSum","CommentSum","RepostSum","TestSum","CovidSum","WeiboSum","Precent"])
        #SumData.to_sql(name="data_sum",con=self.conn, index=False, if_exists='replace')

    def deal3(self):
        #微博数据与疫情数据合并
        sql1 = "select data_sum.*,covid.* from data_sum,covid where data_sum.time=covid.times ;"
        frame1=pd.read_sql(sql1,self.conn)
        frame1=frame1.drop("times",axis=1)#删除列，axis=0删除行
        print(frame1)
        frame1.to_sql(name="totaldatas",con=self.conn,index=False,if_exists='replace')
        frame1.to_excel("totaldata.xlsx")
        frame1.to_stata("total.dta")

if __name__=="__main__":
    d=Deal()
    d.deal3()