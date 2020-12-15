之前在安装jieba wordcloud时，不知道怎么整，于是整理这篇安装第三方包的方法，方便以后使用  

**本人使用windows，举两个例子，其他系统请掉头。**  
>
### 一.jieba  
#### (1.1) 下载第三方安装包jieba
[安装地址](https://pypi.org/project/jieba/)
页面如下：（进入后点击左侧的download files，然后点击右侧的压缩包下载）
![](https://img2018.cnblogs.com/blog/1465325/201908/1465325-20190818100045098-2068614444.png)
#### (1.2) 下载后解压，然后把它放到anaconda的其他库的存放位置。  
jieba里有个setup.py，安装就是要用到这个脚本，关键！    
我的Anaconda放在F盘，然后其他库的安装包放在在F:\Anaconda\pkgs里，所以我就把下载的jieba放到这个文件夹下    
>
#### (1.3) 接下来，打开电脑里的程序：Anaconda Prompt,（跟cmd一样，黑乎乎的界面），输入安装的指令：
![](https://img2018.cnblogs.com/blog/1465325/201908/1465325-20190818100731935-478194134.png)

- 首先，需要把目录切换到F盘（我的anaconda在F盘）  
- 然后，输入指令：cd Anaconda\pkgs\jieba-0.39 

（最终位置是这里：F:\Anaconda\pkgs\jieba-0.39）  

- 安装最后一步：输入指令：python setup.py install
![](https://img2018.cnblogs.com/blog/1465325/201908/1465325-20190818102528982-399022795.png)

- 检查安装情况：
可以去import一下，检验是否导入成功 
![](https://img2018.cnblogs.com/blog/1465325/201908/1465325-20190818103200974-1214898226.jpg)
> 
### 二.wordcloud
#### (2.1) 同理,下载wordcloud (先找到自己python对应版本，我的是3.6 64位）。[下载地址](https://pypi.org/project/wordcloud/#files) 
#### (2.2) 下载后，解压，放在F:\Anaconda\pkgs里

#### (2.3) 接下来，打开电脑里的程序：Anaconda Prompt，输入安装的指令：

- 首先，先把目录切换到F盘  
- 其次，然后输入指令：cd Anaconda\pkgs  
- 最后，输入指令：pip install wordcloud-1.5.0-cp36-cp36m-win_amd64.whl（后面这个 whl 格式的文件需要对应的是你自己下载的版本情况，不一定会跟我的一样哦）
![](https://img2018.cnblogs.com/blog/1465325/201908/1465325-20190818133904237-854767751.png)

显示成功啦！  
![](https://img2018.cnblogs.com/blog/1465325/201908/1465325-20190818134554877-1355382446.jpg)

最后的最后，去导入wordcloud试试吧。



