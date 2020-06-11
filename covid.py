import requests
import json
import pandas as pd
import time
from sqlalchemy import create_engine
# 需要切换成自己的万矿id
#https://www.windquant.com/
#https://mp.weixin.qq.com/s/9Em7pFR7eKMVK52xmj272A
pd.set_option('display.max_rows', None)  # 显示所有的行
pd.set_option('display.max_columns', None)
userid = "2d26ea32-1683-4832-8881-52e114deae4b"#在万矿网获取
indicators = "S6274775,S6274778,S6274779,S6274776,S6274777,S6291502,S6291528,S6291529,S6291530,S6291531,S6291532,S6274789,S6274788,S6274799,S6274802,S6274791,G5753623,G5753627,G5753533,G5753534,G5753535,G5753536,G5753543, G5753626,G5753630"
#在相应图形化界面获取
factors_name = ["ChinaConfirm","ChinaSuspect","ChinaSevere","ChinaDie","ChinaCure","ChinaRemoveObserve","ChinaConfirmNoHubei",
                "ChinaSuspectNoHubei","ChinaSevereNoHubei","ChinaDieNoHubei",
                "ChinaCureNoHubei","AmericanAddup","JapanAddup","GermanyAddup","EnglandAddup","KoreaAddup","GobalAddup","GobalAddupNoChina","AmericanConfirm","JapanConfirm","GermanyConfirm","EnglandConfirm","KoreaConfirm","GobalConfirm","GobalConfirmNoChina"]


#上面是行标
startdate = "2020-01-20"
enddate = "2020-06-09"

url = '''https://www.windquant.com/qntcloud/data/edb?userid={}&indicators={}&startdate={}&enddate={}'''.format(
        userid,indicators,startdate,enddate)
response = requests.get(url)
data = json.loads(response.content.decode("utf-8"))

time_list = data["times"]
value_list = data["data"]


for i in range(len(time_list)):
        time_list[i] = time.strftime("%m-%d", time.localtime(time_list[i]/1000))#获取时间
result = pd.DataFrame(columns=factors_name)#建立dataframe
result["times"]=time_list#插入时间
for i in range(len(factors_name)):#插入其他数据
        result[factors_name[i]] = value_list[i]

print(result)
db = create_engine('mysql+mysqlconnector://root:123456@127.0.0.1:3306/info')
result.to_sql(name="covid",con=db,index=False,if_exists='replace')#存储到数据库

'''
另一种获取途径
https://www.akshare.xyz/zh_CN/latest/
#encodeing:utf-8--
import akshare as ak
from sqlalchemy import create_engine
import pandas as pd
db = create_engine('mysql+mysqlconnector://root:123456@127.0.0.1:3306/info')
frame=ak.covid_19_163(indicator="中国历史时点数据")
date=frame.index.tolist()#读取行索引
times=[]
for i in date:
    i=str(i)[5:]
    times.append(i)
frame['times']=times
frames=frame.iloc[:-1]
#frames.to_sql(name="covid",con=db,index=False,if_exists='replace')
'''
