import requests
from bs4 import BeautifulSoup
import time,os
# from tqdm import tqdm

class Baotu():

	def __init__(self):
		self.url = 'https://ibaotu.com/shipin/7-0-0-0-0-1.html'
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',}
		self.path = u'H:\\baotu'
		self.chunk_size = 1024

	def get_page(self):		# 获取首页，拿到最大页数
		html = self.request(self.url)
		html_soup = BeautifulSoup(html.text,'lxml')
		max_num = html_soup.find('div',attrs={'class','pagelist'}).find_all('a')[-2].text
		# print(max_num,type(max_num))
		return max_num

	def get_all_page(self,max_num):
		for num in range(1,int(max_num)+1)[::-1]:
			self.mkdir_page(num)
			small_url = 'https://ibaotu.com/shipin/7-0-0-0-0-{}.html'.format(num)
			small_html = self.request(small_url)

			small_soup = BeautifulSoup(small_html.text,'lxml')
			video_list = small_soup.find('ul',attrs={'class','clearfix sucai_list'}).find_all('a',attrs={'class','video-box-hand'})
			
			for video in video_list:
				video_url = 'https:{}'.format(video['href'])	# 详情页面
				video_html = self.request(video_url)
				video_soup = BeautifulSoup(video_html.text,'lxml')

				# 视频信息
				video_src = self.get_src(video_soup)		# 视频真实地址
				video_src = 'https://{}'.format(video_src)
				video_title = self.get_title(video_soup)	# 视频标题
				video_title = '{}.mp4'.format(video_title)
				# print(video_src,video_title)

				mp4_html = self.request(video_src,stream=True)
				self.down(mp4_html,video_title)
				
				# break
				# 作比较判断，判断是否存在
				# 每页创建一个文件夹
	
	def mkdir_page(self,num):			# 每页创建一个文件夹
		name = '第{0}页'.format(num)
		isExists = os.path.exists(os.path.join(self.path,name))
		if not isExists:
			print(u'\n[建了一个{0}文件夹！]'.format(name))
			os.makedirs(os.path.join(self.path,name))
			os.chdir(os.path.join(self.path,name)) ##切换到目录
			return True
		else:
			os.chdir(os.path.join(self.path,name)) ##切换到目录
			print(u'\n[名字叫{0}文件夹已存在！]'.format(name))
			return False

	def get_src(self,video_soup):	# 获取视频下载url
		video_src = video_soup.find('a',attrs={'class','video-src'})['src'][2:]
		return video_src

	def get_title(self,video_soup):	# 获取视频标题
		video_src = video_soup.find('h1',attrs={'class','works-name'}).text
		return video_src

	def down(self,mp4_html,video_title):	# 判断视频文件是否存在并下载
		isExists = os.path.exists(video_title)
		if not isExists:		
			data_count = 0
			content_size = int(mp4_html.headers['content-length'])

			with open(video_title,'ab') as f:
				for data in mp4_html.iter_content(chunk_size=self.chunk_size):
					f.write(data)
					data_count = data_count + len(data)
					now = (data_count / content_size) * 100 # 计算下载的进度
					print("\r %s下载进度:%d%% -- (%d/%d)" % (video_title,now,data_count,content_size), end=" ")
			print('\n')
			time.sleep(3)
			return True
		else:
			print(u'{0}已存在！]'.format(video_title))
			return False

	def request(self,url,stream=False):
		html = requests.get(url,headers=self.headers,stream=stream)
		return html

	def work(self):
		max_num = self.get_page()
		self.get_all_page(max_num)
		# mp4_html,video_title = self.get_all_page(max_num)
		# self.down(mp4_html,video_title)

ibaotu = Baotu()
ibaotu.work()