import os
import time

from gtts import gTTS

from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from requests_html import HTMLSession
import shutil
import time
import math
import sys
import helpLibs.consts as consts
import threading



def startAudio():
	pass
	#pygame.mixer.init(freq, bitsize, channels, buffer)

def endAudio():
	pass
	#pygame.mixer.quit()

class lessonAudioBytes(object):
	def __init__(self, words = []):
		self.mySounds = {}
		for i in words:
			i = i.split(',')
			self.addSLoader(i)
			
	def addSLoader(self, i):
		name = i[0]
		file = "{}\\{}\\{}\\{}\\{}.mp3".format(consts.cwd(),consts.fname(),i[11],i[12],i[0].replace("?", "qChar"))
		file = file.replace(" .mp3", ".mp3")
		file = file.replace("..mp3", ".mp3")
		file = file.replace('.mp3.mp3', '.mp3')
		file = file.replace("/", "slashChar")
		file = file.lower()

		self.preload(i)

		self.mySounds[name,i[10]] = SoundLoader.load(file)

	def play(self, i):
		if not (i[0],i[10]) in self.mySounds: self.addSLoader(i)
		sound = self.mySounds[i[0],i[10]]
		sound.volume = 1
		
		def f(а):
			while not а.state == 'stop': 
				Clock.tick()
		sound.bind(on_play= f)
		sound.play()		

	def preload(self, i, r = False):
		if i[14] == 'none':return
		if r:
			if 'img-' in i[1]:
				ifdir ="{}\\{}\\{}\\{}\\{}\\".format(consts.cwd(),consts.fname(),i[11],i[12],consts.images())
				ifile = "{}\\{}\\{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),i[11],i[12],consts.images(),i[1].split('/')[len(i[1].split('/')) - 1])
				if not os.path.isdir(ifdir):
					os.makedirs(ifdir)
				if not os.path.isfile(ifile):
					with open(ifile, 'wb') as f:
						shutil.copyfileobj(getFile(img =  i[1].split('img-')[1]), f)
				return
			elif 'audio-' in i[1]:
				ifdir ="{}\\{}\\{}\\{}\\".format(consts.cwd(),consts.fname(),i[11],i[12])
				ifile = "{}\\{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),i[11],i[12],'audio-' + i[1].split('/')[len(i[1].split('/')) - 1])
				if not os.path.isdir(ifdir):
					os.makedirs(ifdir)
				if not os.path.isfile(ifile):
					with open(ifile, 'wb') as f:
						f.write(getFile(audio = i[1].split('audio-')[1]))
				return
		elif not r:
			if 'audio-' in i[1]: return
		fdir ="{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),i[11],i[12])
		file = "{}\\{}\\{}\\{}\\{}.mp3".format(consts.cwd(),consts.fname(),i[11],i[12],i[0].replace("?", "qChar"))
		file = file.replace(" .mp3", ".mp3")
		file = file.replace("..mp3", ".mp3")
		file = file.replace("/", "slashChar")
		file = file.lower()

		if not os.path.isdir(fdir):
			os.makedirs(fdir)
		if not os.path.isfile(file):
			try:
				with open(file, 'wb') as f:
					f.write(getFile(word = i[0], lang = i[14]))
			except:
				tts = gTTS(text=i[0].replace("commaChar", ","), lang=i[14])
				tts.save("{}".format(file))

def getFile(word = None, lang = None, img = False, audio = False):
	session = HTMLSession()

	if word:
		url = 'http://shtooka.net/search.php?str={}'.format(word)
		r = session.get(url)

		a = r.html.find("img.player_mini")
		for i in a:
			attrs = i.attrs['onclick']
			na = attrs.split(',')[2].split("'")[1]
			if lang in na:
				mp3url = na
				break

		r = session.get(mp3url)
		return r.content
	elif img:
		url = img
		return session.get(url, stream = True).raw
	elif audio:
		url = audio
		return session.get(url).content

def dAllVoice(workdoc = consts.workdoc()):
	j = 1
	source = ""
	shc = 0
	ttsc = 0
	t0 = time.time()
	with open(workdoc,'r', encoding = 'utf-8') as f:
		lines = f.read().split("\n")
	f.close()
	for i in lines:
		if j ==0:
			i = i.split(",")
			fdir ="{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),i[11],i[12])
			file = "{}\\{}\\{}\\{}\\{}.mp3".format(consts.cwd(),consts.fname(),i[11],i[12],i[0].replace("?", "qChar"))
			file = file.replace(" .mp3", ".mp3")
			file = file.replace("..mp3", ".mp3")
			file = file.replace("/", "slashChar")
			file = file.lower()
			if not os.path.isdir(fdir):
				os.makedirs(fdir)
			if not os.path.isfile(file):
				try:
					with open(file, 'wb') as f:
						f.write(getFile(word = i[0], lang = i[14]))
						source = "shtooka"
						shc = shc + 1
				except Exception as e:
					tts = gTTS(text=i[0].replace('commaChar',",").replace("qChar","?").replace("slashChar","/").lower(), lang=i[14])
					tts.save("{}".format(file))
					source = "tts"
					ttsc = ttsc + 1
				
				progress = int(i[10])/len(lines)
				progress = math.floor(progress*100)
				os.system('cls')
				print('\r[{}] {}% {}/{} {} {} tts:{} shtooka:{} time:{}'.format('#'*math.floor(progress/10) + ' '*(10-math.floor(progress/10)), progress, i[10], len(lines), file, source, ttsc, shc, math.floor(time.time() - t0)), end = "\r", flush = True)
		else:
			j = 0

if __name__ == "__main__":
	dAllVoice()