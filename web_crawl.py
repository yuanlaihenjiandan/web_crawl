#遇到的问题：长期大量对一个网站进行访问时，会被判断为恶意攻击，最终会抛出error: [Errno 10054] 这个错误来，远程主机强迫关闭了一个现有的连接
#-*- coding:utf-8-*-
import urllib
import urllib2
import re
import os
import random
import time
import socket

class Web:
  """
  def __init__(self,url,ip_list):
    self.url = url
    self.iplist = ip_list
  """
  def getPage(self,url):
    iplist = ['180.140.161.168:8888']
    #sleep_time = 10
    timeout = 20
    socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
               "Connection":"keep-alive"
               }
    if len(iplist)>0:
      '''
      设置代理
      '''
      proxy = urllib2.ProxyHandler({'https':random.choice(iplist)})
      opener = urllib2.build_opener(proxy)#urllib2.HTTPHandler(debuglevel = 1)
      urllib2.install_opener(opener)
    try:
      #time.sleep(sleep_time)
      request = urllib2.Request(url,headers = headers)
      response = urllib2.urlopen(request)
    except urllib2.URLError,e:
      print '错误类型为',e.reason
      #print url
    except socket.timeout,e:
      print '长时间没相应',url
    #print response.read().decode('gbk')
    return response.read()

  def get_url1(self,page):#分布着各个国家的网页
    #pat = '<div align="center.*?<a.*?href=(.*?) target.*?>(.*?)</a>'
    #这里的正则匹配不是很完美，只是匹配了119个国家而已，漏掉一个!
    pat = '<div align="center.*?<a.*?href="(.*?)".*?>(.*?)</a>'
    pattern = re.compile(pat,re.S)
    items = re.findall(pattern,page)
    #for item in items:
    #  print item[0],item[1]
    items = items[2:]
    #for item in items:
    #  print item[0],item[1]
    url_country = {}
    for item in items:
      #print item[0],item[1]
      if item[1] not in url_country:
        url_country[item[1]] = item[0]
      else:
        pass
    return url_country
    #print url_country

  def get_url2(self,page1):#各个国家对应的页面
    pat = re.compile('<td width="20%.*?<ul.*?<li.*?<a.*?href=(.*?)>(.*?)</a>',re.S)
    items = re.findall(pat,page1)
    url_web_type = {}
    for item in items:
      #print item[0],item[1]
      if item[1] not in url_web_type:
        url_web_type[item[1]] = item[0]
      else:
        pass
    return url_web_type

  def get_url3_before(self,page2):#各种网站类型对应的信息
    pat = re.compile('<td nowrap="nowrap"><a href="(.*?)" target.*?>',re.S)
    items = re.findall(pat,page2)
    url_web_info = []
    for item in items:
      #print item
      url_web_info.append(item)
    return url_web_info

  def start(self):
    html = self.getPage('http://www.world68.com/country.asp')#各个国家所在的页面
    url_new = self.get_url1(html)#得到各个国家对应的部分url
    #print url_new
    #return url_new
    
    
    baseurl = 'http://www.world68.com/'
    url_final = [];#所有最终网址链接
    for country in url_new.keys():
      time_sleep = 5
      #time.sleep(time_sleep)
      #print country
      #print '休息5秒正在进入',country,'所在的网页'
      url_add = url_new[country]
      #print url_add
      url_country = baseurl+url_add
      #print url_country
      html1 = self.getPage(url_country)
      #print html1
      url_new1 = self.get_url2(html1)
      #print url_new1
      #break
      #return url_new1
      
      baseurl1 = 'http://www.world68.com/'
      for web_type in url_new1.keys():
        #print '正在跳转到',web_type,'类型所对应的页面'
        url_add1 = url_new1[web_type]
        #print url_add1
        url_type = baseurl1+url_add1
        #print url_type
        html2 = self.getPage(url_type)
        #print '正在跳转中。。。。。。。。。。。'
        url_add2 = self.get_url3_before(html2)
      
        baseurl2 = 'http://www.world68.com/'
        num = 0
        for i in range(len(url_add2)):
          url_info = baseurl2+url_add2[i]#最终网址
          #print url_info
          #url_final.append(url_info)
          with open('D:\\my college\\Python\\web_crawl\\web\\web_list.txt','a') as f:
            f.write(url_info+'\n')
          f.close()
          #return url_final

class Info:
  def __init__(self):
    self.web1 = Web()
    self.filepath = 'D:\\my college\\Python\\web_crawl\\web\\web_list.txt'
    self.url_list = open(self.filepath).readlines()

  def getInfo(self,page2):
    items = []
    pat = re.compile('<tr bgcolor=FFF.*?class="a9".*?<strong>(.*?)</strong>.*?<tr bgcolor=FFF.*?class="a8".*?<strong>(.*?)</strong>.*?<tr bgcolor=FFF.*?href.*?>(.*?)</a>.*?<a class="s".*?>(.*?)</a>.*?<tr bgcolor=FFF.*?<tr>.*?<td>(.*?)</td>',re.S)
    items = re.findall(pat,page2)
    #for item in items:
      #print item[0],item[1],item[2],item[3],item[4]
    return items
  
  def main(self):
    num = 0
    for url in self.url_list:
      #print url
      #time.sleep(2)
      html = self.web1.getPage(url)
      #print u'正在进入',url_info,u'网站'
      items = self.getInfo(html)
      for item in items:
      #print item[0],item[1],item[2],item[3],item[4]
        with open('D:\\my college\\Python\\web_crawl\\web\\web_info.txt','a') as f:
          num += 1
          f.write(item[2]+','+item[3]+','+item[1]+','+item[0]+','+item[4]+','+str(num)+'\n')
        f.close()
      
if __name__ == '__main__':
  #web = Web()
  #t1 = time.clock()
  #url_final = web.start()
  #print u'总共花了',time.clock()-t1
  info = Info()
  t1 = time.clock()
  info.main()
  print u'总共花了',time.clock()-t1
  #总共花了 1690.25581583


"""         
#print url_info
          html3 = self.getPage(url_info)
          #print u'正在进入',url_info,u'网站'
          items = self.get_final_info(html3)
          for item in items:
            #print item[0],item[1],item[2],item[3],item[4]
            with open('D:\\my college\\Python\\web_crawl\\web\\web_info.txt','a') as f:
              num += 1
              f.write(item[2]+','+item[3]+','+item[1]+','+item[0]+','+item[4]+','+str(num)+'\n')
            f.close()
"""    
#print time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))      

"""
request = urllib2.Request('http://www.world68.com/show.asp?id=10379')
response = urllib2.urlopen(request).read()
#print response
"""
"""
pat = re.compile('<tr bgcolor=FFF.*?class="a9".*?<strong>(.*?)</strong>.*?<tr bgcolor=FFF.*?class="a8".*?<strong>(.*?)</strong>.*?<tr bgcolor=FFF.*?href.*?>(.*?)</a>.*?<a class="s".*?>(.*?)</a>.*?<tr bgcolor=FFF.*?<tr>.*?<td>(.*?)</td>',re.S)
items = re.findall(pat,response)
for item in items:
  print item[0],item[1],item[2],item[3],item[4]
""" 


