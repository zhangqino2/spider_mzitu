#coding=utf-8

import requests
from bs4 import BeautifulSoup
import os


index_url = 'http://www.mzitu.com/'
#设置headers，网站会根据这个判断你的浏览器及操作系统，很多网站没有此信息将拒绝你访问
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3355.4 Safari/537.36','Referer': 'http://www.mzitu.com/'}

#用get方法打开url并发送headers
html = requests.get(index_url,headers = header)

#使用自带的html.parser解析，速度慢但通用
soup = BeautifulSoup(html.text,'html.parser')

#最大页数在a class='page-numbers'标签中的第3个，或者倒数第二个
max_page = soup.find_all("a",class_="page-numbers")[3].text

#生成下载目录
save_dir = os.path.join(os.getcwd(), 'mzitu')
try:
  os.mkdir(save_dir)
except:
  pass

page_url = 'http://www.mzitu.com/page/'

#设置爬取页数
print('请输入要爬取页数')
max_page_num = int(input())

if ((max_page_num<=(int(max_page)+1)) and (max_page_num>=1)):
  #读取套图首页信息
  for page_num in range(1,max_page_num+1):
    taotu_url = page_url + str(page_num)
    taotu_html = requests.get(taotu_url, headers=header)
    taotu_soup = BeautifulSoup(taotu_html.text, 'html.parser')
    # 实际上是第一个class = 'postlist'的div里的所有a 标签是我们要找的信息
    all_title = soup.find('div', class_='postlist').find_all('a', target='_blank')
    for titles in all_title:
      title = titles.get_text()
      if (title != ''):
        print("准备扒取：" + title)
        # 创建套图目录 win不能创建带？的目录
        taotu_dir = save_dir + '\\' + title.strip().replace('?', '')
        if (os.path.exists(taotu_dir)):
           print('目录已存在')
           flag = 1
        else:
          os.mkdir(taotu_dir)
          flag = 0
        os.chdir(taotu_dir)
        pics_url = titles['href']
        pics_html = requests.get(pics_url, headers=header)
        pics_soup = BeautifulSoup(pics_html.text, "html.parser")
        pics_max = pics_soup.find_all('span')
        pics_max_num = pics_max[10].text  # 最大页数
        if (flag == 1 and len(os.listdir(taotu_dir)) >= int(pics_max_num)):
          print('已经保存完毕，跳过')
          continue
        for pic_num in range(1,int(pics_max_num)+1):
          pic_url = pics_url + '/' + str(pic_num)
          pic_html = requests.get(pic_url, headers=header)
          pic_soup = BeautifulSoup(pic_html.text, "html.parser")

          # 图片地址在img标签alt属性和标题一样的地方
          url = pic_soup.find('img', alt=title)
          html = requests.get(url['src'], headers=header)

          # 获取图片的名字方便命名
          name = url['src'].split(r'/')[-1]

          # 图片不是文本文件，以二进制格式写入，所以是html.content
          # f = open(pic_name, 'wb')
          # f.write(html.content)
          # f.close()
          if os.path.isfile(name):
            print("{}已存在".format(name))
            pass
          else:
            with open(name, 'wb')as f:
              f.write(html.content)
              print("正在保存{}".format(name))
              f.close()
          #print(title + '  已经下载完成！')
      if title!='':
        print(title + ' 已经下载完成！！！！！！！')
  print('第' + str(page_num) + '页已经下载完毕！')




else:
  print('输入页数有误')
  pass
