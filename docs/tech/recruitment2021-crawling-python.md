# 爬取应届生网的两千条2021校招信息

!!! bug
    正在從其他平臺搬運文章，下面所有的圖片均無法顯示，正在尋找圖床中……

![在‘喝醉的龙猫’wechat订阅号回复“校招”即可领取本文提到的最新excel文档与python源码的网盘链接](https://upload-images.jianshu.io/upload_images/24101260-4a452bd50fe9bd91?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###前言
又到毕业季，大家开始为找工作而忙碌起来。加上疫情的原因，今年的校招可能是近几年竞争最激烈的一次。

校招与社招不同，大公司们会提前‘预定’好心仪的应届生，所以报名方式与社招直接投自己制作好的简历不同：每一家公司网站都要自己重新填一遍简历。

所以校招也算是一项繁重的工作，特别对于想要‘海投’的同学来说。有些人会把自己投递的校招公司信息整理成表格以便日后进行参考；但在记录投递的公司之前，找公司信息的方法就开始五花八门：有的校招信息来源通过朋友告知，有的通过日常接触的品牌而去网上搜索碰碰运气，有的则是直接在帮你罗列好所有信息的求职网站上寻觅……

参与校招的公司大部分投档方式都在自家网站，热门的求职网站对于校招的信息也不太多。而一些真的很用心的校招搜集网站呢，

却充斥着各种广告：![](https://upload-images.jianshu.io/upload_images/24101260-05f6caa63d0cf936?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
想必大家也不喜欢这种花花绿绿的上网体验，对于想‘海投’的同学来说，搜集信息也确实浪费了大量的时间。

所以，如何舒服地在无广告的世界里找校招？
![在excel里边就会变得非常简洁美观](https://upload-images.jianshu.io/upload_images/24101260-6b770977f7490bd8?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我把应届生校招网 [网站链接](http://www.yingjiesheng.com/2021/) 底下的2000+条校招信息全爬取下来，放进了excel文档里边，上图看到的便是完成后的样子。

有了这些信息在excel之后，可以通过搜索城市（地区）名，或搜索想要的公司来各取所需。另外，excel摆脱网页的束缚，你不需要容忍看完一页要点下一页的操作，你可以随意在表格上边进行删除、备注、记录，省去手动录入信息的大量时间。拥有python的同学，也可以通过运行源码，实时更新网站最新校招信息到本地。

---
###开始爬行

首先加载需要用到的库：
```python
import pandas as pd #这是本次将数据保存为表格形式，进行数据清洗，与录入excel文件所需要的库
import requests #让python请求网页的库
from bs4 import BeautifulSoup #解析html代码的库
import re #正则表达式的库，爬取校招信息对应链接时用到
import time #生成日期，保存的时候有用到
```
这次因为只爬取了三种数据（公司名，发布时间，对应链接），所以没有很复杂的正则表达式和冗长的函数，该网站对爬虫也十分友好。

首先定义好这三列数据的列表名字：
```python
namelist=[]
datelist=[]
link=[]
```

接着访问网站
```python
url = 'http://www.yingjiesheng.com/2021/index-1.html'
page = requests.get(url).content
soup = BeautifulSoup(page,'html')
```
url里的‘index-1’代表第一页，之后可以通过修改这个数字来遍历所有页面。
查看soup，依旧是熟悉的html格式，我们也可以通过在原网页的后台找到储存各项信息所在的标签和class，比如标题：
![](https://upload-images.jianshu.io/upload_images/24101260-29daa31dcf20cc81?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

所以就可以爬取公司校招信息标题：
```python
company = soup.find_all('div', class_='s_clear tit floatl')
for i in company:
namelist.append(i.text)
```
举一反三，爬取日期：
```python
date = soup.find_all('div', class_='box1 bg1')
for i in date:
datelist.append(i.text)
```
爬取链接：
```python
for i in range(len(company)):
  link.append(company[i].find_all('a')[0]['href'])
```
这里的链接藏在‘a’标签里边了，所以我们需要两次find_all， 第一次已经在company里边，所以我们再执行多一次就好了，再提取['href']里边的值，即为链接。

至此，我们就爬完了网页上的第一页100行数据。如果要继续抓取之后的页面，仅需在前面加上for循环把上边的代码全部循环一遍就可以了。
```python

```
###数据清洗
这次爬虫虽然抓取的时候不难，但抓取下来的信息还是需要稍微进行一下清理，比如爬取下来的日期首尾有换行符；比如头俩行居然还是广告；比如有些链接是导向网站的其他链接，所以我们要对它们添加主站域名‘http://www.yingjiesheng.com/’。
![这张图涵盖了上面所述的三种需要清理的现象](https://upload-images.jianshu.io/upload_images/24101260-d45875359513112a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

清洗的代码如下：
```python
df = pd.DataFrame([namelist,datelist,link]).T #先把数据储存进表格里
df.columns=['name','date','link']
df['date'] = df.date.apply(lambda x: x.strip()) #去除日期前后的换行符
df.drop([0,1],axis=0,inplace=True) #去掉前两行广告

linklist = df['link'].tolist() #修改链接让它可以直接访问

for i in range(len(linklist)):
    if re.search('^/job-',linklist[i]):
        linklist[i] = ('http://www.yingjiesheng.com'+linklist[i])
    else:
        pass

df['link'] = linklist

df['date'] = df.date.apply(lambda x: x.replace('网申','')) #去除前面的网申二字
```
清洗之后，我们的表格就顺眼多了，每个链接也都正确：
![](https://upload-images.jianshu.io/upload_images/24101260-5fed363bdf2bb0b4?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最后一步就是将表格保存到本地excel文档：
```python
timestamp = time.strftime('%m%d',time.localtime())
filename = 'recruit'+timestamp+'.xlsx'
df.to_excel(filename,index=False,encoding='utf-8-sig')
```
这里我使用time里边的localtime来显示时间，并用显示的日期自动为文件命名，区分开新旧文档。（对于想隔一段时间抓取一次的同学来说）

**大功告成！**

---
###总结与反思
一
这次爬虫十分简单但却十分有用，我在这里介绍一个好用的excel小技巧提高阅读信息的效率：

![](https://upload-images.jianshu.io/upload_images/24101260-447079f66dc1a11b?imageMogr2/auto-orient/strip)
我们点开筛选，然后将自己想要的公司校招信息用颜色高亮，再点击筛选的小箭头，点击用颜色进行排序。
![](https://upload-images.jianshu.io/upload_images/24101260-735340b429c0c086?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


