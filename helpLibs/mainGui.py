from datetime import timedelta as td

def convertStrTimeAddDays(date, days = 0):
	k = srs.convertToTime(date) + td(days = days)
	return "{}/{}/{}".format(k.day, k.month, k.year), k

import os
import zlib

def Crc32Hasher(file_path):
    buf_size = 65536
    crc32 = 0
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            crc32 = zlib.crc32(data, crc32)
    return format(crc32 & 0xFFFFFFFF, '08x')

import helpLibs.srs as srs
import datetime
import zipfile
import helpLibs.mycsv as mycsv

def makeBackup():
	dal = srs.findDecksAndLevels()
	for folder, subfolders, files in os.walk("{}\{}".format(consts.cwd(),consts.fname())):
		subs = subfolders
		for i in subs:
			if i in dal:
				for folder, subfolders, files in os.walk("{}\{}\{}".format(consts.cwd(),consts.fname(),i)):
					nsubs = subfolders
					for j in nsubs:
						if j in dal[i]:
							for folder, subfolders, files in os.walk("{}\{}\{}\{}".format(consts.cwd(),consts.fname(),i,j)):
									for f in files:
										nnsubs = [x[0].lower() for x in dal[i][j]]
										f = f.replace(".mp3", "").replace("qchar","?").replace("slashchar","/")
										if f in nnsubs:
											pass
										else:
											if os.path.isfile("{}\{}.mp3".format(folder, f)):
												if not 'audio-' in "{}\{}.mp3".format(folder, f):
													os.remove("{}\{}.mp3".format(folder, f))
											else:
												try:
													if not 'audio-' in "{}\{}".format(folder, f.replace("?","qchar") + '.mp3'):
														os.remove("{}\{}".format(folder, f.replace("?","qchar") + '.mp3'))
												except: pass

						else:
							for folder, subfolders, files in os.walk("{}\{}\{}\{}".format(consts.cwd(),consts.fname(),i,j), topdown = False):
								for file in files:
									os.remove("{}\{}".format(folder, file))
								os.rmdir(folder)
			else:
				for folder, subfolders, files in os.walk("{}\{}\{}".format(consts.cwd(),consts.fname(),i), topdown = False):
					for file in files:
						os.remove("{}\{}".format(folder, file))
					os.rmdir(folder)		
		
		
	d = str(datetime.datetime.now()).split(" ")[0]

	if not os.path.isdir(consts.backups() + d):
	 		os.makedirs(consts.backups() + d)

	for folder, subfolders, files in os.walk(consts.backups() + d):
		if len(files) == 0:
			p = consts.backups() + d + '\\session1.zip'
		else:
			p = consts.backups() + d + '\\session{}.zip'.format(len(files)+1)

	mzip = zipfile.ZipFile(p, 'w')

	for folder, subfolders, files in os.walk(consts.cwd()):
		for file in files:
			if file.endswith('.csv'):
				mzip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), consts.cwd()), compress_type = zipfile.ZIP_DEFLATED)
	mzip.close()

	for folder, subfolders, files in os.walk(consts.backups() + d):
		f = (consts.backups() + d + "\\" + files[len(files)-2])
		fc = Crc32Hasher(f)
		pc = Crc32Hasher(p)
		if fc == pc and not f == p:
			os.remove(p)

	for folder, subfolders, files in os.walk(consts.backups()):
		for i in subfolders:
			j = i.replace("-","/").split("/")
			k = "{}/{}/{}".format(j[2],j[1],j[0])
			if (convertStrTimeAddDays(mycsv.curdate)[1] - convertStrTimeAddDays(k)[1]).days > 5:
				for folder, subfolders, files in os.walk(consts.backups() + i):
					for file in files:
						os.remove(consts.backups() + i + "\\" + file)
				os.rmdir(consts.backups() + i)

import  helpLibs.consts as consts

def createDefaults():
	if not os.path.isfile(consts.workdoc()):
		with open(consts.workdoc(), 'w', encoding = 'utf-8') as t:
			t.write('0SENTENCE,1TRANSLATION,2TAGS,3LEARNED,4ATTEMPTS,5SUCCESFUL ATTEMPS,6DAY LAST ATTEMPT,7LAST ATTEMPT RESULT,8DAY TO REVIEW,9ATTEMPT STREAK,10ID,DECK11,LEVEL12,IGNORE13,LANGUAGE14')
		t.close()

from kivy.app import App
from kivy.uix.label import Label
from helpLibs.consts import json_settings
from kivy.config import Config

class mApp(App):
	def build(self):
		self.title = 'PySrs'
		self.use_kivy_settings = False
		return MainFrame(self)

	def build_config(self, config):
		import ctypes.wintypes
		CSIDL_PERSONAL = 5      # My Documents
		SHGFP_TYPE_CURRENT = 0   # Get current, not default value

		buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
		ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

		workloc = buf.value + '\PySrs'
		confile = workloc + '\config.ini'

		# Config.setdefaults('GENERAL', {'cwd': workloc,
		# 				 'month': 30,
		# 				 'workdoc': workloc + '\sentences.csv',
		# 				 'hwdoc': '\history.csv',
		# 				 'fname': 'data',
		# 				 'images':'pics',
		# 				 'backups': workloc + '\\backups\\',
		# 				 'reviewPerLesson': 25,
		# 				 'defaultLang': 'None'})

	def build_settings(self, settings):
		settings.add_json_panel('Settings', consts.Config, data = json_settings)

import guiLibs.mainMenu as mainMenu
from kivy.uix.screenmanager import ScreenManager, Screen

class Splash(Screen):
	def __init__(self, **kw):
		super(Splash, self).__init__(**kw)
		self.name = __name__
		loadingLabel = Label(text = "Loading")
		self.add_widget(loadingLabel)

import threading
from kivy.clock import Clock

class MainFrame(ScreenManager):
	def __init__(self, controller, **kw):
		super(MainFrame, self).__init__(**kw)
		splash = Splash()
		self.controller = controller
		self.add_widget(splash)

		#createDefaults()
		t = threading.Thread(target = self.doValues, daemon = True)
		t.start()
		def load(dt):
			if t.isAlive():
				pass
			else:
				self.remove_widget(splash)
				self.add_widget(mainMenu.mainMenu(self))
				return False
		Clock.schedule_interval(load,0)

	def convertStrTimeAddDays(self, date, days = 0):
		k = srs.convertToTime(date) + td(days = days)
		return "{}/{}/{}".format(k.day, k.month, k.year), k

	def init_vals(self):
		self.allHis = []
		self.hfiles = []
		self.hfilesread = {}
		self.days = {}
		self.secondsLearn = 0 
		self.minutesLearn = 0
		self.hoursLearn = 0

	def historyFiles(self):
		self.init_vals()
		for i in self.dandl:
			self.hfiles.append('{}\\{}\\{}{}'.format(consts.cwd(),consts.fname(),i,consts.hwdoc()))

		for j in self.hfiles:
			try:
				deckName = j.split("\\")[6]
				self.hfilesread[deckName] = []
				for line in mycsv.read(j).split("\n"):
					if not line == '':
						self.hfilesread[deckName].append(line.split(','))
			except:
				pass

		for k in self.hfilesread:
			for n,i in enumerate(self.hfilesread[k]):
				self.allHis.append(i)

		l = []
		p = []
		seconds = 0
		for i in self.allHis:
			if i[16] == mycsv.curdate and i[15] == "review":
				l.append(i)
				seconds += float(i[18])
			if i[16] == mycsv.curdate and i [15] == "learn":
				p.append(i)
		self.donetoday = len(l)
		self.learnedtoday = len(p)

		self.minutesLearn, self.secondsLearn = divmod(seconds, 60)
		self.hoursLearn, self.minutesLearn = divmod(self.minutesLearn, 60)

		j = self.convertStrTimeAddDays(mycsv.curdate)
		l = self.convertStrTimeAddDays(mycsv.curdate)
		for i in self.total:
			k = self.convertStrTimeAddDays(i.split(",")[8])
			if k[1] > j[1]:
				j = k
			if k[1] < l[1]:
				l = k

		self.latestdate = j
		self.earliestdate = l
		self.startdate = self.earliestdate
		
		while not self.startdate[1] == self.latestdate[1]:
			self.startdate = self.convertStrTimeAddDays(self.startdate[0], days = 1)
			if not self.startdate[0] in self.days:
				self.days[self.startdate[0]] = []
			for i in self.total:
				if i.split(",")[8] == self.startdate[0] and i.split(',')[3] == 'yes':
					self.days[self.startdate[0]].append(i)

	def doValues(self):
		t = srs.findTo()
		self.toReview = t[0]
		self.toLearn = t[1]
		self.total = t[2]
		self.deck = None
		self.dandl = srs.findDecksAndLevels()
		self.reviewCounts = {}
		self.learnCounts = {}
		self.totalCounts = {}
		self.langs = [{consts.supportedLangs()[x]:x} if x in consts.supportedLangs() else {'Other':x} for x in list(set([x.split(',')[14] for x in self.total]))]
		self.langs = {v:k for d in self.langs for k, v in d.items()}
		self.deckLangs = {}
		for i in self.dandl:
			self.reviewCounts[i] = len([x for x in self.toReview if i in x.split(",")[11]])
			self.learnCounts[i] = len([x for x in self.toLearn if i in x.split(",")[11]])
			self.totalCounts[i] = len([x for x in self.total if i in x.split(",")[11]])

			for j in self.dandl[i]:
				for k in self.dandl[i][j]:
					if i not in self.deckLangs:
						self.deckLangs[i] = ''
					#if not k[14] == self.deckLangs[i] and not self.deckLangs[i] == '':
					#	print('error found entry with different language in the deck')
					self.deckLangs[i] = self.langs[k[14]]
		self.historyFiles()