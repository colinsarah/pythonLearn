# **Day03回顾**

## **目前反爬总结**

- 基于User-Agent反爬

```python
1、发送请求携带请求头: headers={'User-Agent' : 'Mozilla/5.0 xxxxxx'}
2、多个请求随机切换User-Agent
   1、定义列表存放大量User-Agent，使用random.choice()每次随机选择
   2、定义py文件存放大量User-Agent，使用random.choice()每次随机选择
   3、使用fake_useragent每次访问随机生成User-Agent
      * from fake_useragent import UserAgent
      * ua = UserAgent()
      * user_agent = ua.random
      * print(user_agent)
```

- 响应内容前端做处理反爬

```python
1、html页面中可匹配出内容，程序中匹配结果为空
   * 响应内容中嵌入js，对页面结构做了一定调整导致，通过查看网页源代码，格式化输出查看结构，更改xpath或者正则测试
2、如果数据出不来可考虑更换 IE 的User-Agent尝试，数据返回最标准
```

- 基于IP反爬

```python
控制爬取速度，每爬取页面后随机休眠一定时间，再继续爬取下一个页面
```

## **请求模块总结**

- urllib库使用流程

```python
# 编码
params = {
    '':'',
    '':''
}
params = urllib.parse.urlencode(params)
url = baseurl + params

# 请求
request = urllib.request.Request(url,headers=headers)
response = urllib.request.urlopen(request)
html = response.read().decode('utf-8')
```

- requests模块使用流程

```python
url = baseurl + urllib.parse.urlencode({dict})
html = requests.get(url,headers=headers).text
```

## **解析模块总结**

- 正则解析re模块

```python
import re 

pattern = re.compile('正则表达式',re.S)
r_list = pattern.findall(html)
```

- lxml解析库

```python
from lxml import etree

parse_html = etree.HTML(res.text)
r_list = parse_html.xpath('xpath表达式')
```

## **xpath表达式**

- 匹配规则

```python
1、节点对象列表
   # xpath示例: //div、//div[@class="student"]、//div/a[@title="stu"]/span
2、字符串列表
   # xpath表达式中末尾为: @src、@href、text()
```

- xpath高级

```python
1、基准xpath表达式: 得到节点对象列表
2、for r in [节点对象列表]:
       username = r.xpath('./xxxxxx')  # 此处注意遍历后继续xpath一定要以:  . 开头，代表当前节点
```

# **Day04笔记**

## **requests.get()参数**

### **查询参数-params**

- 参数类型

```python
字典,字典中键值对作为查询参数
```

- 使用方法

```python
1、res = requests.get(url,params=params,headers=headers)
2、特点: 
   * url为基准的url地址，不包含查询参数
   * 该方法会自动对params字典编码,然后和url拼接
```

- 示例

```python
import requests

baseurl = 'http://tieba.baidu.com/f?'
params = {
  'kw' : '赵丽颖吧',
  'pn' : '50'
}
headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
# 自动对params进行编码,然后自动和url进行拼接,去发请求
res = requests.get(baseurl,params=params,headers=headers)
res.encoding = 'utf-8'
print(res.text)
```

**练习**

把课程第1天中的 百度贴吧 抓取案例改为使用requests模块的params参数实现？

```python
# 1、首先改为requests模块
import requests
def get_page(self,url):
    html = requests.get(url,headers=self.headers).content.decode('utf-8')
    return html
# 2、改为params参数（无须编码，无须拼接）
def get_page(self,params):
    html = requests.get(self.url,params=params,headers=self.headers).content.decode('utf-8')

def main(self):
    ... ... 
    for page in range(begin, end + 1):
        pn = (page - 1) * 50
        params ={
            'kw': name,
            'pn': str(pn)
        }

        # 发请求获取响应内容
        html = self.get_page(params=params)
```

### **Web客户端验证 参数-auth**

- 作用及类型

```python
1、针对于需要web客户端用户名密码认证的网站
2、auth = ('username','password')
```

- 达内code课程方向案例

```python
import requests
import re

class NoteSpider(object):
    def __init__(self):
        self.url = 'http://code.tarena.com.cn/'
        self.headers = {'User-Agent':'Mozilla/5.0'}
        self.auth = ('tarenacode','code_2013')

    # 获取+解析
    def get_parse_page(self):
        res = requests.get(
            url=self.url,
            auth=self.auth,
            headers=self.headers
        )
        res.encoding = 'utf-8'
        html = res.text
        # 解析
        p = re.compile('<a href=.*?>(.*?)/</a>',re.S)
        r_list = p.findall(html)
        # r_list : ['..','AIDCode','ACCCode']
        for r in r_list:
            if r != '..':
                print({ '课程方向' : r })

if __name__ == '__main__':
    spider = NoteSpider()
    spider.get_parse_page()
```

**思考：爬取具体的笔记文件？（把今天的笔记抓取下来）**

```python
import requests

# 定义常用变量
url = 'http://code.tarena.com.cn/AIDCode/aid1903/12-spider/spider_day03_note.zip'
headers = {
  'User-Agent' : 'Mozilla/5.0'
}
auth = ('tarenacode','code_2013')

# 发请求获取响应内容(bytes)
html = requests.get(url,headers=headers,auth=auth).content

# 将响应内容保存到本地
filename = url.split('/')[-1]
with open(filename,'wb') as f:
  f.write(html)
  print('%s下载成功' % filename)
```

**如何保存到指定目录？**

```python
import requests
import os 

url = 'http://code.tarena.com.cn/AIDCode/aid1903/12-spider/spider_day03_note.zip'
headers = {
  'User-Agent' : 'Mozilla/5.0'
}
auth = ('tarenacode','code_2013')
print(222)
html = requests.get(url,headers=headers,auth=auth).content
print(1111)
directory = '/home/tarena/' + '/'.join(url.split('/')[3:-1]) + '/'

print(directory)
if not os.path.exists(directory):
    os.makedirs(directory)

filename =  directory + url.split('/')[-1]
print(filename)
with open(filename,'wb') as f:
  f.write(html)
  print('%s下载成功' % filename)
```

### **SSL证书认证参数-verify**

- 适用网站及场景

```python
1、适用网站: https类型网站但是没有经过 证书认证机构 认证的网站
2、适用场景: 抛出 SSLError 异常则考虑使用此参数
```

- 参数类型

  ```python
  1、verify=True(默认)   : 检查证书认证
  2、verify=False（常用）: 忽略证书认证
  # 示例
  response = requests.get(
  	url=url,
  	params=params,
  	headers=headers,
  	verify=False
  )
  ```

### **代理参数-proxies**

- 定义

```python
1、定义: 代替你原来的IP地址去对接网络的IP地址。
2、作用: 隐藏自身真实IP,避免被封。
```

- 普通代理

**获取代理IP网站**

```python
西刺代理、快代理、全网代理、代理精灵、... ... 
```

**参数类型**

```python
1、语法结构
   	proxies = {
       	'协议':'协议://IP:端口号'
   	}
2、示例
    proxies = {
    	'http':'http://IP:端口号',
    	'https':'https://IP:端口号'
	}
```

**示例**

1. 使用免费普通代理IP访问测试网站: http://httpbin.org/get

   ```python
   import requests
   
   url = 'http://httpbin.org/get'
   headers = {
       'User-Agent':'Mozilla/5.0'
   }
   # 定义代理,在代理IP网站中查找免费代理IP
   proxies = {
       'http':'http://115.171.85.221:9000',
       'https':'https://115.171.85.221:9000'
   }
   html = requests.get(url,proxies=proxies,headers=headers,timeout=5).text
   print(html)
   ```

2. 思考: 建立一个自己的代理IP池，随时更新用来抓取网站数据

   fake_useragent使用示例

   ```python
   # 随机生成1个User-Agent
   from fake_useragent import UserAgent
   
   ua = UserAgent()
   print(ua.random)
   ```

   建立自己的IP代理池

```python
import requests
import random
from lxml import etree
from fake_useragent import UserAgent


# 生成随机的User-Agent
def get_random_ua():
    # 创建User-Agent对象
    ua = UserAgent()
    # 随机生成1个User-Agent
    return ua.random


url = 'http://httpbin.org/get'


# 从西刺代理网站上获取随机的代理IP
def get_ip_list():
    headers = {'User-Agent': get_random_ua()}
    # 访问西刺代理网站国内高匿代理，找到所有的tr节点对象
    res = requests.get('https://www.xicidaili.com/nn/', headers=headers)
    parse_html = etree.HTML(res.text)
    # 基准xpath，匹配每个代理IP的节点对象列表
    ipobj_list = parse_html.xpath('//tr')
    # 定义空列表，获取网页中所有代理IP地址及端口号
    ip_list = []
    # 从列表中第2个元素开始遍历，因为第1个为: 字段名（国家、IP、... ...）
    for ip in ipobj_list[1:]:
        ip_info = ip.xpath('./td[2]/text()')[0]
        port_info = ip.xpath('./td[3]/text()')[0]
        ip_list.append(
            {
                'http': 'http://' + ip_info + ':' + port_info,
                'https': 'https://' + ip_info + ':' + port_info
            }
        )
    # 返回代理IP及代理池（列表ip_list）
    return ip_list


# 主程序寻找测试可用代理
def main_print():
    # 获取抓取的所有代理IP
    ip_list = get_ip_list()
    # 将不能使用的代理删除
    for proxy_ip in ip_list:
        try:
            # 设置超时时间，如果代理不能使用则切换下一个
            headers = {'User-Agent': get_random_ua()}
            res = requests.get(url=url, headers=headers, proxies=proxy_ip, timeout=5)
            res.encoding = 'utf-8'
            print(res.text)

        except Exception as e:
            # 此代理IP不能使用，从代理池中移除
            ip_list.remove(proxy_ip)
            print('%s不能用，已经移除' % proxy_ip)
            # 继续循环获取最后1个代理IP
            continue

    # 将可用代理保存到本地文件
    with open('proxies.txt','a') as f:
        for ip in ip_list:
            f.write(ip + '\n')

if __name__ == '__main__':
    main_print()
```

**2、写一个获取收费开放代理的接口**

```python
# getip.py
# 获取开放代理的接口
import requests

# 提取代理IP
def get_ip_list():
  api_url = 'http://dev.kdlapi.com/api/getproxy/?orderid=996140620552954&num=100&protocol=2&method=2&an_an=1&an_ha=1&sep=1'
  res = requests.get(api_url)
  ip_port_list = res.text.split('\r\n')

  return ip_port_list

if __name__ == '__main__':
    proxy_ip_list = get_ip_list()
    print(proxy_ip_list)
```

**3、使用收费开放代理IP访问测试网站: http://httpbin.org/get**

```
1、从代理网站上获取购买的普通代理的api链接
2、从api链接中提取出IP
3、随机选择代理IP访问网站进行数据抓取
```

```python
from getip import *
import time
import random

url = 'http://httpbin.org/get'
headers = {'User-Agent' : 'Mozilla/5.0'}
proxy_ip_list = get_ip_list()

while True:
    # 判断是否还有可用代理
    if not proxy_ip_list:
        proxy_ip_list = get_ip_list()

    proxy_ip = random.choice(proxy_ip_list)
    proxies = {
        'http' : 'http://{}'.format(proxy_ip),
        'https' : 'https://{}'.format(proxy_ip)
    }
    print(proxies)

    try:
        html = requests.get(url=url,proxies=proxies,headers=headers,timeout=5,verify=False).text
        print(html)
        break
    except:
        print('正在更换代理IP，请稍后... ...')
        # 及时把不可用的代理IP移除
        proxy_ip_list.remove(proxy_ip)
        continue
```

- 私密代理

**语法格式**

```python
1、语法结构
proxies = {
    '协议':'协议://用户名:密码@IP:端口号'
}

2、示例
proxies = {
	'http':'http://用户名:密码@IP:端口号',
    'https':'https://用户名:密码@IP:端口号'
}
```

**示例代码**

```python
import requests
url = 'http://httpbin.org/get'
proxies = {
    'http': 'http://309435365:szayclhp@122.114.67.136:16819',
    'https':'https://309435365:szayclhp@122.114.67.136:16819',
}
headers = {
    'User-Agent' : 'Mozilla/5.0',
}

html = requests.get(url,proxies=proxies,headers=headers,timeout=5).text
print(html)
```

## **requests.post()**

- 适用场景a

```
Post类型请求的网站
```

- 参数-data

```python
response = requests.post(url,data=data,headers=headers)
# data ：post数据（Form表单数据-字典格式）
```

- 
  请求方式的特点

```python
# 一般
GET请求 : 参数在URL地址中有显示
POST请求: Form表单提交数据
```

**有道翻译破解案例(post)**

1. 目标

```python
破解有道翻译接口，抓取翻译结果
# 结果展示
请输入要翻译的词语: elephant
翻译结果: 大象
**************************
请输入要翻译的词语: 喵喵叫
翻译结果: mews
```

2. 实现步骤

   ```python
   1、浏览器F12开启网络抓包,Network-All,页面翻译单词后找Form表单数据
   2、在页面中多翻译几个单词，观察Form表单数据变化（有数据是加密字符串）
   3、刷新有道翻译页面，抓取并分析JS代码（本地JS加密）
   4、找到JS加密算法，用Python按同样方式加密生成加密数据
   5、将Form表单数据处理为字典，通过requests.post()的data参数发送
   ```

**具体实现**

- 1、开启F12抓包，找到Form表单数据如下:

```python
i: 喵喵叫
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 15614112641250
sign: 94008208919faa19bd531acde36aac5d
ts: 1561411264125
bv: f4d62a2579ebb44874d7ef93ba47e822
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTlME
```

- 2、在页面中多翻译几个单词，观察Form表单数据变化

```python
salt: 15614112641250
sign: 94008208919faa19bd531acde36aac5d
ts: 1561411264125
bv: f4d62a2579ebb44874d7ef93ba47e822
# 但是bv的值不变
```

- 3、一般为本地js文件加密，刷新页面，找到js文件并分析JS代码

```python
# 方法1
Network - JS选项 - 搜索关键词salt
# 方法2
控制台右上角 - Search - 搜索salt - 查看文件 - 格式化输出

# 最终找到相关JS文件 : fanyi.min.js
```

- 4、打开JS文件，分析加密算法，用Python实现

```python
# ts : 经过分析为13位的时间戳，字符串类型
js代码实现:  "" + (new Date).getTime()
python实现:  str(int(time.time()*1000))

# salt
js代码实现:  r+parseInt(10 * Math.random(), 10);
python实现:  ts + str(random.randint(0,9))

# sign（设置断点调试，来查看 e 的值，发现 e 为要翻译的单词）
js代码实现: n.md5("fanyideskweb" + e + salt + "n%A-rKaT5fb[Gy?;N5@Tj")
python实现:
from hashlib import md5
s = md5()
s.update("fanyideskweb" + e + salt + "n%A-rKaT5fb[Gy?;N5@Tj".encode())
sign = s.hexdigest()
```

-  5、代码实现

```python
import requests
import time
from hashlib import md5
import random

# 获取相关加密算法的结果
def get_salt_sign_ts(word):
    # salt
    salt = str(int(time.time()*1000)) + str(random.randint(0,9))
    # sign
    string = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
    s = md5()
    s.update(string.encode())
    sign = s.hexdigest()
    # ts
    ts = str(int(time.time()*1000))
    return salt,sign,ts

# 攻克有道
def attack_yd(word):
    salt,sign,ts = get_salt_sign_ts(word)
    # url为抓包抓到的地址 F12 -> translate_o -> post
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "238",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "OUTFOX_SEARCH_USER_ID=-1449945727@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=1492587933.976261; JSESSIONID=aaa5_Lj5jzfQZ_IPPuaSw; ___rl__test__cookies=1559193524685",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    # Form表单数据
    data = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': ts,
        'bv': 'cf156b581152bd0b259b90070b1120e6',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }

    json_html = requests.post(url,data=data,headers=headers).json()
    result = json_html['translateResult'][0][0]['tgt']
    return result

if __name__ == '__main__':
    word = input('请输入要翻译的单词：')
    result = attack_yd(word)
    print(result)
```

# **今日作业**

```python
1、仔细复习并总结有道翻译案例，抓包流程，代码实现
2、通过百度翻译，来再次熟练抓包流程，分析，断点调试等操作
```


