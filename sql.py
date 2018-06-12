#!/usr/bin/python
# -*- coding: UTF-8 -*-
import spider
import pymysql.cursors
# 连接MySQL数据库

def save_data(data):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='62043088', db='weather',charset='utf8')
    cursor = connection.cursor()

    cursor.execute('drop table if exists tianqi')
    cursor.execute("create table weather.tianqi(district varchar(255) COLLATE utf8_bin NOT NULL, day_weather varchar(255) COLLATE utf8_bin NOT NULL, day_wind varchar(255) COLLATE utf8_bin NOT NULL, day_temperature varchar(255) COLLATE utf8_bin NOT NULL, night_weather varchar(255) COLLATE utf8_bin NOT NULL, night_wind varchar(255) COLLATE utf8_bin NOT NULL, night_temperature varchar(255) COLLATE utf8_bin NOT NULL, primary key (district)) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin")

    s = "insert into weather.tianqi (district, day_weather, day_wind , day_temperature , night_weather , night_wind , night_temperature ) VALUES ( %s,%s,%s,%s,%s,%s,%s )"
    data
    for a in data:
        cursor.execute(s, (a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
    connection.commit()

    connection.close()


def main(url):
    data=spider.main(url)
    save_data(data)
