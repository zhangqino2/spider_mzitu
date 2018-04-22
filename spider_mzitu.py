#coding=utf-8

import requests
from bs4 import BeautifulSoup
import os
import sys


if(os.name == 'nt'):
        print(u'你正在使用win平台')
else:
        print(u'你正在使用linux平台')


url = 'http://www.mzitu.com/'

#设置headers，网站会根据这个判断你的浏览器及操作系统，很多网站没有此信息将拒绝你访问
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3355.4 Safari/537.36'}

#用get方法打开url并发送headers
html = requests.get(url,headers = header)

#打印结果 .text是打印出文本信息即源码
#print(html.text)


#使用自带的html.parser解析，速度慢但通用
soup = BeautifulSoup(html.text,"html.parser")


#最大页数在a class='page-numbers'标签中的第3个，或者倒数第二个
max_page = soup.find_all("a",class_="page-numbers")[3].text
print(max_page)


'''#输出每个图片页面的地址
for i in range(1,int(max_page) + 1):
    href = url+'page/'+str(i)
    print(href)


#实际上是第一个class = 'postlist'的div里的所有a 标签是我们要找的信息
all_title = soup.find("div",class_="postlist").find_all("a",target="_blank")


for titles in all_title:
    title = titles.get_text() #提取文本
    print(title)'''

path = '/mzitu/'
same_url = 'http://www.mzitu.com/page/'
for n in range(1,int(max_page)+1):
    ul = same_url+str(n)
    start_html = requests.get(ul, headers=header)
    soup = BeautifulSoup(start_html.text,"html.parser")
    all_a = soup.find('div',class_='postlist').find_all('a',target='_blank')
    for a in all_a:
        title = a.get_text() #提取文本
        if(title != ''):
            print("准备扒取："+title)

            #win不能创建带？的目录
            if(os.path.exists(path+title.strip().replace('?',''))):
                    #print('目录已存在')
                    flag=1
            else:
                os.makedirs(path+title.strip().replace('?',''))
                flag=0
            os.chdir(path + title.strip().replace('?',''))
            href = a['href']
            html = requests.get(href,headers = header)
            mess = BeautifulSoup(html.text,"html.parser")
            pic_max = mess.find_all('span')
            pic_max = pic_max[10].text #最大页数
            if(flag == 1 and len(os.listdir(path+title.strip().replace('?',''))) >= int(pic_max)):
                print('已经保存完毕，跳过')
                continue
            for num in range(1,int(pic_max)+1):
                pic = href+'/'+str(num)
                html = requests.get(pic,headers = header)
                mess = BeautifulSoup(html.text,"html.parser")
                pic_url = mess.find('img',alt = title)
                html = requests.get(pic_url['src'],headers = header)
                file_name = pic_url['src'].split(r'/')[-1]
                f = open(file_name,'wb')
                f.write(html.content)
                f.close()
            print('完成')
    print('第',n,'页完成')