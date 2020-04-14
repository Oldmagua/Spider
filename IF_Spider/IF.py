from lxml import etree 
import requests
import re

#设置数据输出格式
def data_format(keys,values):
	keys=[key.strip() for key in keys]
	values=[value.strip() for value in values]
	print('\n')
	for i in range(len(keys)):
		print(keys[i]+'\t'+values[i])
	print('\n\n')

#Xpath数据匹配	
def xpath_format(page,pattern):
	html=etree.HTML(page)
	results=html.xpath(pattern)
	label=results[0].xpath('string(.)')
	label=re.split('\n',label)
	label=[i for i in label if i != '']
	return len(results),label

#爬取IF信息
def get_influence_factor(keyword):
	page=requests.get('http://www.greensci.net/search?kw='+keyword).text
	pattern_key='//table/tr'
	pattern_value='//table/tr/td/div/p[.=" '+keyword+' " or .=" '+keyword.upper()+' " or .=" '+keyword.lower()+' " or .=" '+keyword.title()+' "]/../../..'
	if xpath_format(page,pattern_key)[0]==1:
		print("\nDon't find the journal you had input\nPlease check the journal name\n\n")
	else:
		try:
			keys=xpath_format(page,pattern_key)[1]
			values=xpath_format(page,pattern_value)[1]
			data_format(keys,values)
		except:
			print("\nDon't find the journal you had input\nPlease check the journal name\n\n")

#设置显示界面
def main():
	while True:
		keyword=input('Input the journal name:\n')
		if keyword=='q':
			break
		else:
			get_influence_factor(keyword)

if __name__ == '__main__':
	main()
