# -s*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pymysql.cursors
import sys

class WeatherSpider():

    def __init__(self,state,headers):
        self.url='http://www.weather.com.cn/textFC/'+state+'.shtml'
        self.headers=headers
        self.state=state

    def get_html(self,url):
        try:
            requests.adapters.DEFAULT_RETRIES = 2
            r = requests.get(url, headers = self.headers)
            r.encoding='utf-8'
            text=r.text

            return text

        except:
            sys.exit()



    def get_data(self):
        
        text=self.get_html(self.url)

        soup = BeautifulSoup(text,'lxml')
        items=soup.find('div', class_="conMidtab").find_all('div', class_="conMidtab3")

        search_temp1=[]
        for item in items:
            search_temp1.append(str(item))

        search_temp2=[]
        for item in search_temp1:
            soup = BeautifulSoup(item,'lxml')
            tar=soup.find_all('tr')

            convert_to_string = []
            for item in tar:
                convert_to_string.append(str(item))
            search_temp2.append(convert_to_string)

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
        temperature=[]



        for j in search_temp2:
            for i in j:

                distr=dist.search(i)
                district.append(distr.group(1))
                weat=wea.search(i)
                weather.append(weat.group(1))
                win=wi.search(i)
                wind.append(win.group(1))
                tempe=temp.search(i)
                temperature.append(int(tempe.group(1)))

        for j in search_temp2:
            for i in j:
                weat2=wea2.search(i)
                weather.append(weat2.group(1))
                win2=wi2.findall(i)
                wind.append(win2[1])
                tempe2=temp2.search(i)
                temperature.append(int(tempe2.group(1)))


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


    def display(self):
        data=self.get_data()

        for x in data:
            for y in x:
                if type(y) == 'string':
                    print(y.decode('utf-8'))
                else:
                    print(y)
            print(' ')

    def save_data(self):
        data=self.get_data()

        connection = pymysql.connect(host='127.0.0.1', user='root', password='62043088', db='weather',charset='utf8')
        cursor = connection.cursor()

        cursor.execute('drop table if exists '+self.state)
        cursor.execute("create table weather."+self.state+"(district varchar(255) COLLATE utf8_bin NOT NULL, day_weather varchar(255) COLLATE utf8_bin NOT NULL, day_wind varchar(255) COLLATE utf8_bin NOT NULL, day_temperature INT COLLATE utf8_bin NOT NULL, night_weather varchar(255) COLLATE utf8_bin NOT NULL, night_wind varchar(255) COLLATE utf8_bin NOT NULL, night_temperature INT COLLATE utf8_bin NOT NULL) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin")

        insert = "insert into weather."+self.state+" (district, day_weather, day_wind , day_temperature , night_weather , night_wind , night_temperature ) VALUES ( %s,%s,%s,%s,%s,%s,%s )"

        for a in data:

            cursor.execute(insert, (a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
        connection.commit()

        connection.close()
