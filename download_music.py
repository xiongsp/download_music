import requests
from selenium import webdriver#webdriver
from urllib.parse import quote#encode url
import time

driver=webdriver.Safari()

def get_song_href(name):
	print(name)
	url="https://music.liuzhijin.cn/?name="+quote(name)+"&type=netease"
	driver.get(url)
	time.sleep(3)
	return driver.find_element_by_id("j-src-btn").get_attribute("href")
	driver.quit()

try:

	if input("input download mode\n1=list from file\n2=input one by one\n")=="1":
		with open("/Users/xiong/Downloads/Music/List.txt","r") as f:
			for song_name in f.readlines():
				target_mp3=get_song_href(song_name.strip())
				print(target_mp3)
				if target_mp3==None:
					continue
				f=requests.get(target_mp3)
				with open("/Users/xiong/Downloads/Music/"+song_name+".mp3","wb") as code:
					code.write(f.content)
	else:
		while (1):
			song_name=input("input song name:")
			with open("/Users/xiong/Downloads/Music/"+song_name+".mp3","wb") as code:
				code.write(requests.get(get_song_href(song_name)).content)
	driver.quit()
except:


	driver.quit()
	exit(1)