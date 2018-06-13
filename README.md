# Spider
## 简介
这个爬虫能从[中国天气网](http://www.weather.com.cn/)的[文字版国内天气预报](http://www.weather.com.cn/textFC/hb.shtml#)网页中爬取当前省份中所有市区白天夜间的名称、天气现象、风向、最高气温并存入MySQL中。

## 环境
* python
>* python 2.7
>* requests
>* bs4
>* pymysql
* MySQL
>* MySQL 8.0.11

## spider.py
这个文件主要负责访问网页数据，查找各个市区的天气信息，并将它们存入一个二维list中。

## sql.py
这个文件主要负责链接MySQL服务器并将spider.py中爬取的天气信息list存入MySQL中。
