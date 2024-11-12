# funLibrary.py

import requests
import json
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# 将日期转换成前一天
def changeDate(date_string):
    # 将日期字符串转换为日期对象
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    # 计算前一天的日期
    previous_day = date_object - timedelta(days=1)
    # 将前一天的日期对象转换为字符串
    return previous_day.strftime("%Y-%m-%d")

def get_cookie():
    try:
        # 请求获取 cookie
        response = requests.get("http://io.power.xyquan.top/getcookie.php")
        # 解析 JSON 响应
        data = response.json()
        # 获取 cookie 值
        cookie_value = data.get("cookie")
        return cookie_value
    except Exception as e:
        print("获取 cookie 时出错：", e)
        return None

# 从数据库数据库所有房间编号
def get_roomcodes(get_data_url):
    try:
        # 发送 GET 请求获取 roomcode 数据
        response = requests.get(get_data_url)
        # 将 JSON 数据解析为 Python 字典
        data = response.json()
        # 返回 roomcodes 数组
        return data['roomcodes']
    except Exception as e:
        print("获取房间代码时出错：", e)
        return []

# 将爬去的数据更新到数据库
def update_power(update_data_url, roomcodes, powers, dates, electricities):
    try:
        # 构造要发送的数据，包含 roomcodes 和 powers 数组
        payload = {'roomcodes': roomcodes, 'powers': powers, 'dates': dates, 'electricities': electricities}
        # 将数据转换为 JSON 格式
        json_payload = json.dumps(payload)
        print(json_payload)
        # 发送 POST 请求更新数据
        response = requests.post(update_data_url, data=json_payload)
        # 打印响应结果
        print("更新响应：", response.text)
    except Exception as e:
        print("更新电量时出错：", e)

# 返回200-切换房间成功
def changeRoom(roomCode, cookie):
    __VIEWSTATE = ''
    # 第一次headers
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookie,
        'Host': 'electric.dgcu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0',
        'referer': 'http://electric.dgcu.edu.cn/'
    }
    
    # 第一次请求：get
    response = requests.get('http://electric.dgcu.edu.cn/', headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 <input> 标签，并获取 value 属性值
        input_tag = soup.find('input', id='__VIEWSTATE')
        if input_tag:
            __VIEWSTATE = input_tag['value']
        else:
            print("第一次请求get时：未找到__VIEWSTATE")
    else:
        print("请求失败:", response.status_code)

    # 第二次headers
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Content-Length': '941',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 'electric.dgcu.edu.cn',
        'Origin': 'http://electric.dgcu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://electric.dgcu.edu.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0'
    }

    # 第二次请求的表单
    form_data = {
        '__EVENTTARGET': 'drlouming',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': 'CA0B0334',
        'drlouming': roomCode[0: 2],
        'drceng': '',
        'drfangjian': '',
        'radio': 'usedR',
        'ImageButton1.x': '52',
        'ImageButton1.y': '13'
    }

    # 第二次请求：post
    url = 'http://electric.dgcu.edu.cn/'
    response = requests.post(url, headers=headers, data=form_data)
    
        # 检查响应状态码
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 <input> 标签，并获取 value 属性值
        input_tag = soup.find('input', id='__VIEWSTATE')
        if input_tag:
            __VIEWSTATE = input_tag['value']
        else:
            print("第二次请求post时：未找到__VIEWSTATE")
    else:
        print("请求失败:", response.status_code)


    # 第三次headers
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Content-Length': '1118',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 'electric.dgcu.edu.cn',
        'Origin': 'http://electric.dgcu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://electric.dgcu.edu.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0'
    }


    # 第三次请求的表单
    form_data = {
        '__EVENTTARGET': 'drceng',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': 'CA0B0334',
        'drlouming': roomCode[0: 2],
        'drceng': roomCode[0: 4],
        'drfangjian': '',
        'radio': 'usedR',
        'ImageButton1.x': '52',
        'ImageButton1.y': '13'
    }

    # 第三次请求：post
    url = 'http://electric.dgcu.edu.cn/'
    response = requests.post(url, headers=headers, data=form_data)
    
        # 检查响应状态码
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 <input> 标签，并获取 value 属性值
        input_tag = soup.find('input', id='__VIEWSTATE')
        if input_tag:
            __VIEWSTATE = input_tag['value']
        else:
            print("第三次请求post时：未找到__VIEWSTATE")
    else:
        print("请求失败:", response.status_code)

    # 第四次headers
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Content-Length': '1950',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 'electric.dgcu.edu.cn',
        'Origin': 'http://electric.dgcu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://electric.dgcu.edu.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0'
    }

    # 第四次请求的表单
    form_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': 'CA0B0334',
        'drlouming': roomCode[0: 2],
        'drceng': roomCode[0: 4],
        'drfangjian': roomCode,
        'radio': 'usedR',
        'ImageButton1.x': '52',
        'ImageButton1.y': '13'
    }

    # 第四次请求：post
    url = 'http://electric.dgcu.edu.cn/'
    response = requests.post(url, headers=headers, data=form_data)
    
        # 检查响应状态码
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 <input> 标签，并获取 value 属性值
        input_tag = soup.find('input', id='__VIEWSTATE')
        if input_tag:
            __VIEWSTATE = input_tag['value']
        else:
            print("第四次请求post时：未找到__VIEWSTATE")
    else:
        print("请求失败:", response.status_code)

    return response.status_code

# 爬去电量信息
def getPower(cookie):
    # 设置请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Cookie': cookie,
        'Host': 'electric.dgcu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://electric.dgcu.edu.cn/default.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0'
    }

    # 发送 GET 请求
    url = 'http://electric.dgcu.edu.cn/usedRecord.aspx'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # 视图状态
        __VIEWSTATE = ''
        # 视图状态生成器
        __VIEWSTATEGENERATOR = ''
        # 事件验证
        __EVENTVALIDATION = ''
        # 获取当前日期
        today = datetime.today()

        # 获取当天和十天前的日期字符串
        todayStr = today.strftime("%Y-%m-%d")
        tenDayAgoStr = (today - timedelta(days=10)).strftime("%Y-%m-%d")

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取__VIEWSTATE
        __VIEWSTATE_tag = soup.find('input', id='__VIEWSTATE')
        if __VIEWSTATE_tag:
            __VIEWSTATE = __VIEWSTATE_tag['value']
        
        # 获取__VIEWSTATEGENERATOR
        __VIEWSTATEGENERATOR_tag = soup.find('input', id='__VIEWSTATEGENERATOR')
        if __VIEWSTATEGENERATOR_tag:
            __VIEWSTATEGENERATOR = __VIEWSTATEGENERATOR_tag['value']
        
        # 获取__EVENTVALIDATION
        __EVENTVALIDATION_tag = soup.find('input', id='__EVENTVALIDATION')
        if __EVENTVALIDATION_tag:
            __EVENTVALIDATION = __EVENTVALIDATION_tag['value']

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "845",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookie,
            "Host": "electric.dgcu.edu.cn",
            "Origin": "http://electric.dgcu.edu.cn",
            "Referer": "http://electric.dgcu.edu.cn/usedRecord.aspx",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0"
        }
        form_data = {
            "__VIEWSTATE": __VIEWSTATE,
            "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": __EVENTVALIDATION,
            "txtstart": tenDayAgoStr,
            "txtend": todayStr,
            "btnser": "查询"
        }
        # 请求展开进十天的用电记录
        url = 'http://electric.dgcu.edu.cn/usedRecord.aspx'
        response = requests.post(url, headers=headers, data=form_data)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 初始化日期和电量列表
            power = soup.find('span', class_='number orange').text
            dates = []
            electricities = []

            # 找到所有<tr>标签（除了标题行）
            trs = soup.find_all('tr', class_='contentLine')

            # 遍历每个<tr>标签
            for tr in trs:
                # 找到当前<tr>标签下的所有<td>标签
                tds = tr.find_all('td')
                # 第一个<td>标签中是日期，第三个<td>标签中是电量
                date = int(changeDate(tds[0].text.strip())[-2:])
                electricity = float(tds[2].text.strip())
                # 将日期和电量添加到对应的列表中
                dates.append(date)
                electricities.append(electricity)
            dates.reverse()
            electricities.reverse()
            return {
                'power': power,
                'dates': dates,
                'electricities': electricities
            }
        else:
            print('展开进十天用电记录失败')
    else:
        print('获取电量页面失败')
    return {}
