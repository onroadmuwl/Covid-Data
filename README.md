# Covid-Data
与疫情数据获取与处理
---------

为研究疫情期间公众舆论反应与疫情发展状况直接的关系，利用python爬虫程序和平台API接口，获取有关数据，并进行数据处理，方便进行下一步时间序列分析，数据分析部分后期将进行相应更新。


# myCatch.py
基于央视新闻官方微博对公众舆论关注度进行分析，目的是获取2020年以来央视新闻官方微博的所有微博评论数，点赞量，以及转发数。<br>
与前面程序不同，这次爬取的是微博手机端的网页版，采取免登录的模式，并且采用多个代理ip，通过获取api接口，保证爬取任务的一次性完成。获取api接口：<br>
since_id<br>
https://m.weibo.cn/api/container/getIndex?uid=2656274875&type=uid&value=2656274875&containerid=1076032656274875<br>
https://m.weibo.cn/api/container/getIndex?uid=2656274875&type=uid&value=2656274875&containerid=1005052656274875<br>
https://m.weibo.cn/api/container/getIndex?uid=2656274875&type=uid&value=2656274875&containerid=1078032656274875<br>
https://m.weibo.cn/api/container/getIndex?uid=2656274875&type=uid&value=2656274875&containerid=2302832656274875<br>
https://m.weibo.cn/api/container/getIndex?uid=2656274875&type=uid&value=2656274875&containerid=1076032656274875&since_id=4511399117729669<br>
https://m.weibo.cn/api/container/getIndex?uid=2656274875&type=uid&value=2656274875&containerid=1076032656274875&since_id=4511342374405026<br>
https://m.weibo.cn/api/container/getIndex?uid=2656274875&type=uid&value=2656274875&containerid=1076032656274875&since_id=4511280708383633<br>
在谷歌浏览器中选择：检查-network-XHR-getIndex.....-preview,从而在上一个返回json中寻找since_id。在经过一系列处理后，直接存储到sql中<br>

# covid.py
利用万矿平台的现成的接口，获取数据，并且把数据整理成dataframe形式，然后保持到mysql中。<br>
 self.conn = create_engine('mysql+mysqlconnector://root:123456@127.0.0.1:3306/info')#需要下载一个软件mysql_connector到电脑上，或者用pymysql会有警告<br>
 improveData.to_sql(name="data_sum",con=self.conn, index=False, if_exists='replace')#存回数据库<br>
 
 # deal.py
deal1():<br>
先对数据进行初步筛选，获取发布日期为1月20日到6月9日的微博，然后构建一个简单的语义字典，判别本条微博是否与疫情相关，在dataframe中新建一列，如果相关的话，该列值为1。
deal2():<br>
实现数据按日期汇总归纳，之后再在dataframe中新建几个指标。
deal3():<br>
利用sql语句将疫情数据表和微博表合并，只保留一列的时间数据。

完成上面这些工作，下一步是对时间序列数据进行分析·············
==============
 
 



