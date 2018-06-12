# -s*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

def get_html(url):
    headers={
        'Host': 'www.weather.com.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'vjuids=12e8755c2.163d2e344bb.0.90de82576377e; userNewsPort0=1; f_city=%E6%B3%89%E5%B7%9E%7C101230501%7C; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1528251503; UM_distinctid=163d2e376e470b-007fc8eabbcf57-336e7707-fa000-163d2e376e5245; CNZZDATA1262608253=1293431561-1528246424-null%7C1528246424; Wa_lvt_1=1528251513; defaultCity=101230501; zs=101230501%7C%7C%7Cyd-uv; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1528335450; vjlast=1528251500.1528335450.13; Wa_lpvt_1=1528335450'
    }
    requests.adapters.DEFAULT_RETRIES = 2
    r = requests.get(url, headers = headers)
    r.encoding='utf-8'
    x=r.text

    soup = BeautifulSoup(x,'lxml')
    items=soup.find('div', class_="conMidtab").find_all('div', class_="conMidtab3")

    a=[]
    for item in items:
        a.append(str(item))
    b=[]
    for x in a:
        soup = BeautifulSoup(x,'lxml')
        tar=soup.find_all('tr')
        l = []
        for item in tar:
            l.append(str(item))
        b.append(l)
    return b


def find(html):
    dist=re.compile(r'<a href="http://www.weather.com.cn/weather/.*target="_blank">(.*)</a></td>')
    wea=re.compile(r'<td width="89">(.*)</td>')
    wi=re.compile(r'<span>(.*)</span>')
    temp=re.compile(r'<td width="92">(.*)</td>')


    wea2=re.compile(r'<td width="98">(.*)</td>')
    wi2=re.compile(r'<span>(.*)</span>')
    temp2=re.compile(r'<td width="86">(.*)</td>')

    district=[]
    weather=[]
    wind=[]
    category=[]
    temperature=[]

    for j in html:
        for i in j:

            distr=dist.search(i)
            district.append(distr.group(1))
            weat=wea.search(i)
            weather.append(weat.group(1))
            win=wi.search(i)
            wind.append(win.group(1))
            tempe=temp.search(i)
            temperature.append(tempe.group(1))

    for j in html:
        for i in j:
            weat2=wea2.search(i)
            weather.append(weat2.group(1))
            win2=wi2.findall(i)
            wind.append(win2[1])
            tempe2=temp2.search(i)
            temperature.append(tempe2.group(1))


    data=[]
    for i in range(0,len(district)):
        inner=[]
        while(len(inner)<7):
            inner.append(district[i])
            inner.append(weather[i])
            inner.append(wind[i])
            inner.append(temperature[i])
            inner.append(weather[i+len(district)])
            inner.append(wind[i+len(district)])
            inner.append(temperature[i+len(district)])
        data.append(inner)
    return data


def display(data):
    for x in data:
        for y in x:
            print(y.decode('utf-8'))
        print(' ')



def main(url):
    html=get_html(url)
    data=find(html)
    return data

url='http://www.weather.com.cn/textFC/yunnan.shtml'
x=main(url)
display(x)
