# 数据爬虫项目
主要实现了针对四种网页：
['https://vega.github.io/.*', 
    'https://bl.ocks.org/.*', 
    'https://makingdatavisual.github.io/.*',
    'https://www.trafforddatalab.io/.*']
中 vega-lite/v4.json 类型和少量vega-lite其他类型的可视化图表模型、数据与图片的抓取

##爬虫内容存储

| 参数名称 | 参数说明 | 参数类型 | 是否必须 | 缺省值 |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| id | 主键，标识 | Integer | 是 | 1 |
| url | 爬取的vega-lite地址 | Text | 是 | “https://makingdatavisual.github.io/” |
| model | 爬取的vega-lite的JSON Specification | Map | 是 | - |
| hashmodel | 爬取的vega-lite的唯一标识 | String | 是 | - |
| data | vega-lite数据，也可能在model中 | Map | 否 | - |
| picture | vega-lite生成的图片 | Text | 否 | - |
| registerTime | 爬取时间 | Data | 是 | - |
| latestModifyTime | 修改时间 | Data | 是 | - |


## 快速开始


1.新建虚拟环境、安装环境
-   cd data_crawl_pro
-   virtualenv venv
-   source ./bin/activate
-   cd ..
-   pip install -r requirement.txt
      
2.修改本地数据库信息
-   将properties.py中的url等信息修改为自己本地的信息

3.chromedriver的配置
-   下载地址：http://chromedriver.storage.googleapis.com/index.html
-   从中找到与本地谷歌浏览器版本相同的driver版本，并根据window、mac、linux进行选择
-   将下载下来的chromedriver覆盖data_crawl_pro的chrodriver

4.环境已配好，开始运行
-   python set_up.py


