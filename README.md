# 数据爬虫项目
主要实现了针对vega类型的可视化图表模型、数据与图片的抓取

##快速开始

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

4.环境已配好，开始运行
-   python set_up.py


