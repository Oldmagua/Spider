import requests
import re
#url='https://yz.lol.qq.com/v1/zh_cn/champions/syndra/index.json'
#url2='https://yz.lol.qq.com/v1/zh_cn/search/index.json'


def get_hero_name():
	url='https://yz.lol.qq.com/v1/zh_cn/search/index.json'
	r=requests.get(url).json()['champions']
	name={}
	for n in range(0,len(r)):
		nameZh=r[n]['name']#“暗裔剑魔”
		nameEn=r[n]['slug']#“aatrox”
		name[nameZh]=nameEn
	#print(name)
	return name

def get_story_url(name):
	url='https://yz.lol.qq.com/v1/zh_cn/champions/'+name+'/index.json'
	return url
	
def get_hero_file(url):
	r=requests.get(url).json()['champion']
	name=r['name']
	title=r['title']
	biography=r['biography']
	pat=re.compile('<p>(.*?)</p>',re.S)
	fullstory=re.findall(pat,str(biography))
	print(title,'\n',name,'\n')
	for i in range(0,len(fullstory)):
		print('   ',fullstory[i])	
	
def main(name):
	nameEn=get_hero_name()[name]
	url=get_story_url(nameEn)
	get_hero_file(url)
	
if __name__=='__main__':
	while True:
		name=input('\n\n输入英雄名称：')
		if name=='q':
			break
		else:
			try:
				main(name)
			except KeyError as ve:
				print(ve,'：输入英雄名字错误，例如 辛德拉')

