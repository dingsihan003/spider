# -s*- coding: utf-8 -*-
from flask import Flask
import pymysql.cursors
from flask import render_template
import spider


app = Flask(__name__)


@app.route('/<state>')
def SQL(state):

    try:
        connection = pymysql.connect(host='127.0.0.1', user='root', password='62043088', db='weather',charset='utf8')
        cursor = connection.cursor()

        sql = "select * from "+state
        cursor.execute(sql)    #执行sql语句

        results = cursor.fetchall()    #获取查询的所有记录
        connection.commit()
        connection.close()

    except:
        headers={
            'Host': 'www.weather.com.cn',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

        x=spider.WeatherSpider(state,headers)
        x.save_data()
        connection = pymysql.connect(host='127.0.0.1', user='root', password='62043088', db='weather',charset='utf8')
        cursor = connection.cursor()

        sql = "select * from "+state
        cursor.execute(sql)    #执行sql语句

        results = cursor.fetchall()    #获取查询的所有记录
        connection.commit()
        connection.close()

    district=[]
    day_weather=[]
    day_wind=[]
    day_temperature=[]
    night_weather=[]
    night_wind=[]
    night_temperature=[]
    for r in results:
        district.append(r[0])
        day_weather.append(r[1])
        day_wind.append(r[2])
        day_temperature.append(r[3])
        night_weather.append(r[4])
        night_wind.append(r[5])
        night_temperature.append(r[6])

    data=[]
    for i in range(0,len(district)):
        inner=[]
        while(len(inner)<7):
            inner.append(district[i])
            inner.append(day_weather[i])
            inner.append(day_wind[i])
            inner.append(day_temperature[i])
            inner.append(night_weather[i])
            inner.append(night_wind[i])
            inner.append(night_temperature[i])
        data.append(inner)


    return render_template('index.html',**locals())

if __name__ == '__main__':
    app.run()
