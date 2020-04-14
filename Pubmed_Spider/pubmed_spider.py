import requests
import re 
import pandas as pd
import random
import time

class Pubmed_Spider(): #建立一个爬虫对象


	#初始化参数
	def __init__(self,key_word): 
		self.key_word=key_word #关键词参数


	#爬取检测
	def base_crawl(self): 
		url='https://pubmed.ncbi.nlm.nih.gov/?term='+self.key_word
		req=requests.get(url).text

		#检测关键词查询是否有结果
		try:
			pat=re.compile(r'<span.*?class="value">(.*?)</span>',re.S)
			page_total_pat=re.compile(r'data-pages-amount="(.*?)"',re.S)
			results_num=re.findall(pat,req)[0]
			page_total=re.findall(page_total_pat,req)[0]
		except:
			results_num=0
			page_total=0

		#返回关键词查询结果：数据总条目，页面总数
		return results_num, page_total


	#爬取页面ids信息
	def ids_crawl(self,page):
		url='https://pubmed.ncbi.nlm.nih.gov/?term='+self.key_word+'&page='+page
		req=requests.get(url).text
		ids_pat=re.compile(r'data-chunk-ids="(.*?)"',re.S)
		ids=re.findall(ids_pat,req)[0].split(',')
		return ids


	#依次爬取每个id对应条目数据
	def page_crawl(self,id):
		url='https://pubmed.ncbi.nlm.nih.gov/'+id
		req=requests.get(url).text
		title_pat=re.compile(r'<h1.*?class="heading-title">(.*?)</h1>',re.S)
		abstract_pat=re.compile(r'<div.*?class="abstract-content selected".*?<p>(.*?)</p>',re.S)
		title=re.findall(title_pat,req)[0].replace('\n',' ').strip()

		#检测摘要是否显示结果
		try: 
			abstract=re.findall(abstract_pat,req)[0].replace('\n',' ').strip()
		except IndexError:
			abstract='无摘要或摘要无获取权限'
		return title, abstract


	#保存数据
	def save_data(self,i,title,abstract):
		df= pd.DataFrame(pd.read_excel(self.key_word+'.xlsx'))
		df_rows = df.shape[0]
		df.loc[df_rows] =[i,title,abstract]
		df.to_excel(self.key_word+'.xlsx', sheet_name='sheet1', index=False)



#我的爬虫
def crawl(download_page,my_spider):

	#新建一个爬虫对象
	crawl_spider=my_spider

	#建立空白excel表格，含有表头
	df=pd.DataFrame(columns=['page','title','abstract'])
	df.to_excel(crawl_spider.key_word+'.xlsx', sheet_name='sheet1', index=False)

	#爬虫主程序
	i=1
	while i<=int(download_page): #遍历所有页面
		ids=crawl_spider.ids_crawl(str(i)) #获取单一页面所有id信息
		k=1
		print('***第 '+str(i)+' 页开始下载***')
		for j in ids: #遍历所有id
			print('正在下载第 '+str(i)+' 页'+'	第 '+str(k)+' 条数据')
			title,abstract=crawl_spider.page_crawl(j) #按id爬取数据
			crawl_spider.save_data(i,title,abstract) #保存id爬取结果
			print('第 '+str(i)+' 页'+'	第 '+str(k)+' 条数据已保存\n')
			time.sleep(random.random()) #每爬取一次id，休眠 0~1s时间
			k+=1
		print('第 '+str(i)+' 页已下载保存完成\n')
		time.sleep(random.uniform(1,2)) #每爬取完成一个页面，休眠 1~2s时间
		i+=1
	print('已下载完成 '+download_page+' 页')



if __name__=='__main__':
	while True:
		search_word=input('\n*******Pubmed查询*******\n\n输入你想要查询的关键词：')
		my_spider=Pubmed_Spider(search_word) #新建一个爬虫对象
		print('\n*******查询中*******')
		results_num,page_total=my_spider.base_crawl() #查询关键词结果总数
		if results_num!=0:
			print('\n查询到 '+results_num+' 个结果，总计 '+page_total+' 页')
			while True:
				download_page=input('\n选择下载页数： \n0代表不下载但查看第一篇文章信息\nn（为数字，且不大于'+page_total+'）代表下载n页文章\n输入q退出下载页面\n\n输入下载页数：')
				try:
					if download_page=='q': #退出下载，返回查询界面
						break
					elif int(download_page)==0: #查询第一条结果信息
						ids=my_spider.ids_crawl('1')[0]
						title,abstract=my_spider.page_crawl(ids)
						print('title:\n'+title+'\nabstract:\n'+abstract)
					elif 0<int(download_page)<=int(page_total.replace(',','')): #下载指定数量页面数据
						crawl(download_page,my_spider)
						break
					else: #输入错误，返回输入
						print('输入无效，请重新输入')
				except Exception as e:
					print(e)
		else: 
			print('\n关键词查询结果为 0 ，请重新输入查询关键词')