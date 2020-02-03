import requests  # download the song which was given a url
from selenium import webdriver  # webdriver
from urllib.parse import quote  # encode url
#  from selenium.webdriver.support.wait import WebDriverWait  # wait until elements appear
import time
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB  # write meta info to mp3

driver = webdriver.Safari()


def get_song_href(name):
	# print(name)
	url = "https://music.liuzhijin.cn/?name=" + quote(name) + "&type=netease"
	driver.get(url)
	time.sleep(2)
	# while (driver.find_element_by_id("j-src-btn").get_attribute("download")==None):
	# 	pass#wait unitl
	title = driver.find_element_by_id("j-src-btn").get_attribute("download").split("-", 1)[0]
	artist = driver.find_element_by_id("j-src-btn").get_attribute("download").split("-", 1)[1].split(".",1)[0]
	target = driver.find_element_by_id("j-src-btn").get_attribute("href")
	info = {'title': title, 'artist': artist, 'url': target}
	return info


def SetMp3Info(path, info):
	songFile = ID3(path)
	# songFile['APIC'] = APIC(  # 插入封面
	# 	encoding=3,
	# 	mime='image/jpeg',
	# 	type=3,
	# 	desc=u'Cover',
	# 	data=info['picData']
	# )
	songFile['TIT2'] = TIT2(  # 插入歌名
		encoding=3,
		text=info['title']
	)
	songFile['TPE1'] = TPE1(  # 插入第一演奏家、歌手、等
		encoding=3,
		text=info['artist']
	)
	# songFile['TALB'] = TALB(  # 插入专辑名
	# 	encoding=3,
	# 	text=info['album']
	# )
	songFile.save()
try:

	if input("input download mode\n1=list from file\n2=input one by one\n") == "1":
		with open("/Users/xiong/Downloads/Music/List.txt", "r") as ListFile:
			for song_name in ListFile.readlines():
				song_name=song_name.strip()
				try:
					info=get_song_href(song_name)
					target_mp3 = info['url']
					# print(target_mp3)
					if target_mp3 is None:
						print("**Can't Find: " + song_name)
						continue  # cant get the url of the song
					out = requests.get(target_mp3)
					with open("/Users/xiong/Downloads/Music/" + song_name + ".mp3", "wb") as output:
						output.write(out.content)
						SetMp3Info("/Users/xiong/Downloads/Music/" + song_name + ".mp3", info)
						print("Successful: " + song_name)
				except:
					print("**Error: " + song_name)
				continue
	else:
		while (1):
			song_name = input("input song name:")
			info=get_song_href(song_name)
			target_mp3=info['url']
			with open("/Users/xiong/Downloads/Music/" + song_name + ".mp3", "wb") as output:
				output.write(requests.get(target_mp3).content)
				SetMp3Info("/Users/xiong/Downloads/Music/" + song_name + ".mp3", info)
				print("Successful: " + song_name)
	driver.quit()
except:
	print("**Error: "+song_name)