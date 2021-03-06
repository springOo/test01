# -*- coding:UTF-8 -*-
import requests, json, time, sys
from contextlib import closing

"""
类说明:从unsplash网站爬取图片
参数：无
返回：无
时间：2017-11-17
"""

class get_photos(object):
	
	def __init__(self):
		self.photos_id = []
		self.download_server = "https://unsplash.com/photos/xxx/download?force=trues"
		self.target = "http://unsplash.com/napi/feeds/home"
		self.headers = {'authorization':'c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626'}
		
	"""
	函数说明：获取图片ID
	参数：无
	返回：无
	"""
	def get_ids(self):
		req = requests.get(url=self.target,headers = self.headers,verify=False)
		html = json.loads(req.text)
		next_page = html['next_page']
		for each in html['photos']:
			self.photos_id.append(each['id'])
		time.sleep(1)
		for i in range(4):
			req = requests.get(url=next_page,headers=self.headers,verify=False)
			html = json.loads(req.text)
			next_page = html['next_page']
			for each in html['photos']:
				self.photos_id.append(each['id'])
			time.sleep(1)
	"""
	函数说：图片下载
	"""
	def download(self,photos_id,filename):
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
		target = self.download_server.replace('xxx',photos_id)
		with closing(requests.get(url=target,streaa=True,verify=False,headers=self.headers)) as r:
			with open('%d.jpg' % filename,'ad+') as f:
				for chunk in r.iter_content(chunk_size = 1024):
					if chunk:
						f.write(chunk)
						f.flush()
	
if __name__ == '__main__':
	gp = get_photos()
	print('获取图片链接中：')
	gp.get_ids()
	print('图片下载中：')
	for i in range(len(gp.photos_id)):
		print('正在下载第%d张图片' % (i+1))
		gp.download(gp.photos_id[i],(i+1))