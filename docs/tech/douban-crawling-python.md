# 极速在论坛里找房：爬取douban

!!! bug
    正在從其他平臺搬運文章，下面所有的圖片均無法顯示，正在尋找圖床中……

### 前言

打工人难免会遇到租房这种烦心事，也是应届生踏入社会挨的第一大板。不过幸运的人总归能幸运；如果觉得自己不被幸运女神照顾，那就要开始努力找寻捷径，好让多出来的时间给自己躺下来放松一下。


除了各种租房App，传统论坛上也有许多房源，因为有些租客着急转租，这种情况是捡漏的好机会。但是像豆瓣这样的论坛，小组页面内没有可供精确搜索的功能、每页帖子数量的限制导致用户需要不断翻页获取新帖子，想找到符合需求目标实在是太慢太繁琐。


这个时候爬虫就派上用场了。像上上期我分享过在校招网里找工作一样，我们也可以将豆瓣的帖子标题和链接全部爬取下来，放进excel再慢慢检索。有了爬虫爬取douban之后，我们可以做到：



- 通过地铁线、区域快速搜索高亮符合需求的帖子；

- 无需翻页，爬取一次即可调出所有帖子；

- 在Excel里操作比网页更加方便，可自行备注、筛选。

- 去除重复的帖子



去除重复的帖子：

如果经常在豆瓣找房的同学就会发现，自己每看完一页点下一页之后，许多之前看过的又会重复在新的一页上。这是因为许多发布房源的房东用了机器人或者纯手动不断的在自己的帖子底下水贴，不断刷新回复时间让自己的帖子更加的靠前——所以那些没有水贴的帖子就会往下沉，之前看过的帖子就会在下一页出现。根据我的观察，如果每一页停留1-2分钟，在周末夜晚这种高峰时段基本在前几页都会有25% - 40% 的帖子重复率，大大降低每一页获取新信息的速度。所以我在写代码的时候加入了个检查重复的小function，直接毙掉重复帖子~



### 开始爬行



这次就不分步骤详解了，豆瓣的网页做的十分亲民，后台的源代码做得是整整齐齐，轻松就能定位出所有的帖子链接。只要我们把帖子链接和标题爬取出来，工作就完成了。

需要注意的点：

1. 豆瓣也有反爬虫，我们需要在request的时候将我们的浏览器版本放到headers中，让豆瓣觉得我们是用浏览器去打开网站而不是python。

2. 另外，为了避免链接请求过快被封锁IP，我们在爬取每一页之后让python休眠1秒，所以还需要用到time这个库。

```python

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_doubantitle(group, page):
    href = []
    title = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    
    for i in range(page):
        url = 'https://www.douban.com/group/{}/discussion?start={}'.format(group,i*25)
        print('try to get page {}...'.format(i))
        r = requests.get(url,headers=headers)
        if r.status_code == 200:
            content = r.content
        else:
            print('Failed')
        print('cool.')
        soup = BeautifulSoup(content,"lxml")

        titleset = soup.find_all('td',class_ = 'title')

        href.extend([i.find('a').attrs['href'] for i in titleset])
        title.extend([i.find('a').attrs['title'] for i in titleset])
        print('page {} done, 1 seconds to next page'.format(i))
        time.sleep(1)
        
    return href,title

```


到这里，我们就设定好爬虫的公式。接着只要运行这个公式就可以爬取到数据了。最后我们将它们放到表格里边，按需储存为excel或者其他格式就好了：

```python


href,title = get_doubantitle('477137',10) #477137是徐汇法租界租房小组的代号，在小组的url上面哦~10代表要爬取10页。

#转入表格
df = pd.DataFrame([title,href]).T
df.drop_duplicates(inplace= True)
df.index = range(df.shape[0])
df


```

### 总结



〇

虽然这次是爬取租房帖子，但理论上所有小组的帖子都可以爬到。因为时间关系没有把每个帖子的内容也顺便爬下来，因为那样代表着电脑要重新访问一遍每一帖，所以按需手动复制链接会比较理想。



（完）

