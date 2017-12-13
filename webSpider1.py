# -*- coding:UTF-8 -*-
import requests
import sys
from bs4 import BeautifulSoup

"""
类说明：下载《笔趣看》网小说《一念永恒》
parameters:无
returns:无
日期：2017-11-16
"""

class downloader(object):
	
	def __init__(self):
		self.server = "http://www.biqukan.com/"
		self.target = "http://www.biqukan.com/1_1094/"
		self.name = [] #存放章节名
		self.urls = [] #存放章节链接
		self.nums = [] #章节数
	
	"""
	函数说明：获取下载链接
	参数：target=下载链接（string)
	返回：texts = 章节内容（string）
	"""
	def get_download_url(self):
		req = requests.get(url = self.target)
		html = req.text
		div_bf = BeautifulSoup(html)
		div = div_bf.find_all('div',class_='listmain')
		a_bf = BeautifulSoup(str(div[0]))
		a = a_bf.find_all('a')
		self.nums = len(a[15:])  #剔除不必要章节，统计节数
		for each in a[15:]:
			self.name.append(each.string)
			self.urls.append(self.server + each.get('href'))
		
	"""
	函数说明：获取章节内容
	"""
	def get_contents(self,target):
		req = requests.get(url = target)
		html = req.text
		bf = BeautifulSoup(html)
		texts = bf.find_all('div',class_='showtxt')
		texts = texts[0].text.replace('\xa0'*8,'\n\n')
		return texts
		
	"""
	函数说明：将爬取的文章内容写入文件
	参数：name - 章节名称（string）
		  path - 当前路径下，小说保存名称（string）
		  text - 章节内容（string）
	"""
	def writer(self,name,path,text):
		write_flag = True
		with open(path,'a',encoding='utf-8') as f:
			f.write(name + '\n')
			f.writelines(text)
			f.write('\n\n')
	
if __name__ =='__main__':
	dl = downloader()
	dl.get_download_url()
	print('《一念永恒》开始下载:')
	for i in range(dl.nums):
		dl.writer(dl.name[i],'一念永恒.txt',dl.get_contents(dl.urls[i]))
		sys.stdout.write(" 已下载：%.3f%%" % float(i/dl.nums) + '\r')
		sys.stdout.flush()
	print('《一念永恒》下载完成')
		
		