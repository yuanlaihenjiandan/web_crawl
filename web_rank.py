#-*- coding:utf-8-*-
import urllib
import urllib2
import re
import os
import random
import time
import socket

class Tool:
    def get_domains(self):
      filepath = 'D:\\my college\\Python\\web_crawl\\web\\web_info.txt'
      data = open(filepath).readlines()
      url_list = []
      for line in data:
        items = line.split('\t')
        if items[0] == "":
          pass
        else:
          #url_list.append([items[0],items[2]])
          #用来存放所有爬下的网址。形式为http://....
          with open('D:\\my college\\Python\\web_crawl\\web\\web_test.txt','a') as f:
            f.write(items[0]+','+items[2]+'\n')
          f.close()
          
    def get_all_urls(self):
      #filepath = 'D:\\my college\\Python\\web_crawl\\web\\web_test.txt'#第一次执行时 
      #domains = open(filepath).readlines()
      #domains = [domain.split(',')[1][7:].strip() for domain in domains]
      """用来存放所有domain的文件，形式为www.baidu.com
      for domain in domains:
        with open('D:\\my college\\Python\\web_crawl\\web\\all_domain.txt','a') as f:
          f.write(domain+'\n')
      """
      filepath = 'D:\\my college\\Python\\web_crawl\\web\\domains_rest.txt'
      domains = open(filepath).readlines()
      return domains

    def get_rest_urls(self):#得到剩下的还没爬取排名的形如www.baidu.com形式的网址
      filepath = 'D:\\my college\\Python\\web_crawl\\web\\all_domain.txt'
      all_domains = open(filepath).readlines()#所有的记录，得处理下，将后面的处理下
      all_domains = [domain.replace('/\n','') for domain in all_domains]
      all_domains = [domain.replace('\n','') for domain in all_domains]
      all_domains_login = open('D:\\my college\\Python\\web_crawl\\web\\web_rank_final.txt').readlines()
      all_domains_login = [domain.split('\t')[0] for domain in all_domains_login]#已经爬取的
      set1 = set(all_domains)-set(all_domains_login)#还没爬取的
      os.remove('D:\\my college\\Python\\web_crawl\\web\\domains_rest.txt')
      print u'已经删除原有文件domains_rest.txt'
      #print len(set1)
      for line in list(set1):
        with open('D:\\my college\\Python\\web_crawl\\web\\domains_rest.txt','a') as f:
          f.write(line)
          f.write('\n')
        f.close()             
    
    def get_final_url(self):
        filepath = 'D:\\my college\\Python\\web_crawl\\web\\web_rank_final.txt'
        data = open(filepath).readlines()
        data = list(set(data))
        os.remove(filepath)
        for line in data:
            with open('D:\\my college\\Python\\web_crawl\\web\\web_rank_final.txt','a') as f:
                d = line.split('\t')
                f.write(d[0]+'\t'+d[1])
            f.close()
    
    
class Rank:
  
  def __init__(self):
    #timeout = 20
    #socket.setdefaulttimeout(self.timeout)
    #self.filepath = open('D:\\my college\\Python\\web_crawl\\web\\web_test.txt')
    #self.domains = self.filepath.readlines()
    #self.domains = [domain[7:].strip() for domain in self.domains]

    """
    url = "http://alexa.chinaz.com/default.aspx?"
    for domain in self.domains:
      post_data = {
        "domain":domain,
        "upd":"true"
        }
      data = urllib.urlencode(post_data)
      baseurl = url+data
      print baseurl
    """        
    self.url = "http://alexa.chinaz.com/default.aspx?"
    self.headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
      "Connection":"keep-alive"
      }

  def get_url(self):
    tool = Tool()
    tool.get_rest_urls()
    domains = tool.get_all_urls()
    url_list = []
    for domain in domains:
      #time.sleep(5)#睡眠5秒钟
      post_data = {
        "domain":domain,
        "upd":"true"
        }
      data = urllib.urlencode(post_data)
      baseurl = self.url+data
      url_list.append(baseurl)
    return url_list
    
    
  def getPage(self,url):
    iplist = ['180.140.161.168:8888']#,'124.193.51.249:3128','58.255.66.147:9999','36.97.107.18:9797','119.29.115.107:808','27.38.143.137:9797','39.160.152.167:8123','125.112.241.107:808']
    if len(iplist)>0:
      '''
        设置代理
      '''
      proxy = urllib2.ProxyHandler({'https':random.choice(iplist)})
      opener = urllib2.build_opener(proxy)#urllib2.HTTPHandler(debuglevel = 1)
      urllib2.install_opener(opener)
    try:
      request = urllib2.Request(url,headers = self.headers)
      response = urllib2.urlopen(request)
      return response.read()
    except urllib2.URLError,e:
      print u'错误类型为',e.reason
      return None
    except socket.timeout,e:
      print u'长时间没相应',url
      return None
    except Exception,e:
      print u'其他类型错误'
      return None

  def get_Info(self,page):
    pat = re.compile('<h4>.*?<em>(.*?)</em>.*?<em>(.*?)</em>',re.S)
    items = re.findall(pat,page)
    for item in items:
      #print item[0],item[1]
      #用来存放所有形如www.baidu.com对应排名的文件
      with open('D:\\my college\\Python\\web_crawl\\web\\web_rank_final.txt','a') as f:
        f.write(item[0]+'\t'+item[1]+'\n')
      f.close()
  
  def main(self):
    url_list = self.get_url()
    for url in url_list:
      time.sleep(2)
      html = self.getPage(url)
      if html:
          self.get_Info(html)
      else:
          continue
    
    
if __name__ == '__main__':
  #tool.get_domains()这一句不用在执行了，已经生成文件了。
  #每次执行main时先将文件处理下，因为其实news.qq.com/militery.shtml跟news.qq.com是一样的，而且最终返回结果是一样，需要去重处理
  #tool = Tool()
  #tool.get_final_url()
  rank = Rank()
  rank.main()
    
