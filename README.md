# Spider
## 简介
这个爬虫能从[中国天气网](http://www.weather.com.cn/ "http://www.weather.com.cn/")的[文字版国内天气预报](http://www.weather.com.cn/textFC/hb.shtml# "http://www.weather.com.cn/textFC/hb.shtml#")网页中爬取当前省份中所有市区白天夜间的名称、天气现象、风向、最高气温并存入MySQL中。之后flask将MySQL中的数据传入静态html网页中并可在127.0.0.1:5000／省市名称拼音 中访问天气数据。

## 环境
* python
>* python 2.7
>* requests
>* bs4
>* pymysql
>* flask 1.0.2

* MySQL
>* MySQL 8.0.11

## spider.py

这个文件包含一个class，该class共有两个参数，第一个是爬取目标省份的拼音，第二个是自定义的header。

* get_html
>这个函负责访问网页并存储网页html文本，并返回一个包含网页文本的字符串。函数有两个参数，第一个是爬取目标省份的拼音，第二个是自定义的header。

* get_data
>这个函数负责在html文本中搜素天气信息，并返回一个包含了每个市区天气的二维list。函数有一个参数，即目标html文本(get_html函数的返回值)。

* display
 >这个函数负责显示提取到的天气数据，用于测试。函数有一个参数，即get_data的返回值。

* save_data
 >这个函数负责将天气数据存入MySQL中。所有数据存在weather数据库下，每个省份的天气信息存入独立的一张表。函数有一个参数，即get_data的返回值。

## page.py

这个文件负责从数据库中搜素用户输入的天气信息，如果未找到则调用spider.py文件从网站获取数据存入数据库，并将数据库中的信息传入html文件中。

## index.html

这个文件将page.py传入的参数转化成html表格。


Thank
