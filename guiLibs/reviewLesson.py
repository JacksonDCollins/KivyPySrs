from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.clock import Clock

import helpLibs.srs as srs
import helpLibs.audio as audio
import helpLibs.consts as consts
import helpLibs.mycsv as mycsv

import guiLibs.mainMenu
import guiLibs.editEntry as editEntry

from datetime import datetime, timedelta
import math


class reviewLesson(Screen):
	def __init__(self, controller, words, **kw):
		super(reviewLesson, self).__init__(**kw)
		self.controller = controller
		self.words = words
		self.layout = StackLayout()
		
		self.createWidgets()
		self.add_widget(self.layout)

	def createWidgets(self):
		def t(s, v):
			s.text_size[0] = s.width
			s.texture_update()
			s.height = s.texture_size[1]

		top = BoxLayout(size_hint_y = None)

		self.countLabel = Label(text = "/", font_size = 20, size_hint_y = None, size_hint_x = None, halign = 'center')
		#self.countLabel.text_size[0] = 100
		top.add_widget(self.countLabel)

		self.label = Label(text = "", font_size = 32, size_hint_y = None, size_hint_x = 1, halign = 'center')
		self.label.bind(text = t)
		top.add_widget(self.label)

		exitButton = Button(text = "Exit", font_size = 32, size_hint_y = None, size_hint_x = None)
		exitButton.bind(on_release=self.goMainMenu)
		top.add_widget(exitButton)
		
		self.layout.add_widget(top)

		self.tagsLabel = Label(text = "", font_size = 20, size_hint_y = None, halign = 'center')
		#self.tagsLabel.bind(text = t)
		self.layout.add_widget(self.tagsLabel)

		self.correctLabel = Label(text = '', font_size = 0, size_hint_y = None, halign = 'center')
		self.correctLabel.bind(text = t)
		self.layout.add_widget(self.correctLabel)

		confLayout = BoxLayout(size_hint_y = None)
		self.confirmButton = Button(text = "Submit", size_hint_y = None)
		confLayout.add_widget(Widget())
		confLayout.add_widget(self.confirmButton)
		confLayout.add_widget(Widget())
		self.layout.add_widget(confLayout)

		confLayout = BoxLayout(size_hint_y = None, height = 50)
		self.answerEntry = TextInput(font_size = 32, multiline = False)
		confLayout.add_widget(Widget(size_hint_x=.1))
		confLayout.add_widget(self.answerEntry)
		confLayout.add_widget(Widget(size_hint_x=.1))
		self.layout.add_widget(confLayout)		

		confLayout = BoxLayout(size_hint_y = None)
		editButton = Button(text = "Edit", size_hint_y = None)
		editButton.bind(on_release=lambda x: self.editEntry(self.r.curWord))
		confLayout.add_widget(Widget())
		confLayout.add_widget(editButton)
		confLayout.add_widget(Widget())
		self.layout.add_widget(confLayout)

	def review(self):
		self.r = reviewLessonClass(self, self.words, tWidget = self.label, eWidget = self.answerEntry, tagsWidget = self.tagsLabel, cWidget = self.countLabel, cButton = self.confirmButton, cLabel = self.correctLabel)
		audio.startAudio()
		self.r.start()
		#self.controller.controller.doValues()
		#self.goMainMenu()
		#except Exception as e:
		#	print(e)
		#	self.goMainMenu()

	def on_enter(self):
		#self.layout.clear_widgets()
		#self.createWidgets()
		self.review()

	def on_leave(self):
		audio.endAudio()

	def editEntry(self, line):
		self.editEntrytl = editEntry.editEntry(self.r, line, size_hint_x = 0.8)
		self.editEntrytl.open()
		
	def goMainMenu(self, *args):
		self.controller.controller.switch_to(guiLibs.mainMenu.mainMenu(self.controller.controller))

class reviewLessonClass(object):
	def __init__(self, controller, words, tWidget, eWidget, tagsWidget, cWidget, cButton, cLabel):
		try: self.audLight = AsyncImage(source='extras/audLight.png')
		except: self.audLight = AsyncImage(source='audLight.png')
		try: self.audDark = AsyncImage(source='extras/audDark.png')
		except: self.audDark = AsyncImage(source='audDark.png')

		self.curdate = "{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year)
		self.completed = []
		self.uncompleted = []
		self.redo = []
		self.hissentences = []

		self.nextFunc = None
		self.stopTimer = False
		self.newWord = None
		self.curWord = None

		self.words = words
		self.root = controller
		self.controller = controller.controller
		self.tWidget = tWidget
		self.eWidget = eWidget
		self.cLabel = cLabel

		self.eWidget.bind(text = lambda x,d: self.getAnswer(x, False, func = self.nextFunc))
		self.eWidget.bind(on_text_validate = lambda x: self.getAnswer(x, True, func = self.nextFunc))
		self.eWidget.time = 0

		self.tagsWidget = tagsWidget
		self.cWidget = cWidget
		self.cButton = cButton
		self.cButton.bind(on_release=lambda x: self.getAnswer(self.eWidget, True, func = self.nextFunc))

		self.audioController = audio.lessonAudioBytes(self.words)

	def afterAnswer(self, w, line, edited, func):
		w.text = ''
		if not edited:
			if not 'audio-' in line.split(',')[1].replace('commaChar', ','): self.audioController.play(line.split(','))# audio.preload(line.split(',')); audio.play(line.split(','))
			else: self.audioController.play(line.split(','))
			
		w.background_colour = (1,1,1,1)
		w.foreground_colour = (0,0,0,1)
		func()

	def deleteWord(self, line):
		try:
			self.words.remove(','.join(line))
			self.uncompleted.remove(','.join(line))
			self.redo.remove(','.join(line))
		except:
			pass
		mycsv.clearlines(mstr = line[10], option = 10)
		self.normal()

	def editWord(self, line, new):
		try:
			self.words.remove(','.join(line))
			self.uncompleted.remove(','.join(line))
			self.redo.remove(','.join(line))
		except:
			pass
		self.words.append(','.join(new))
		self.normal()

	def addDays(self, line):
		def convertToTime(date):
			return datetime.strptime("{}/{}/{}".format(date.split("/")[0],date.split("/")[1],date.split("/")[2]), "%d/%m/%Y")
		
		if line[7] == "fail":
			days = 1
		else:
			streakco = math.floor((float(line[9]) * 1.8)*(float(line[9]) * 1.8))
			attemptsco = int(line[4])
			sucattemptsco = int(line[5])
			try:
				tco = (sucattemptsco/attemptsco)
			except:
				tco = 0
			days = math.floor(streakco * tco)
			if days == 0:
				days = 1
		
		newDate = convertToTime(line[6]) + timedelta(days = days)
		return "{}/{}/{}".format(newDate.day, newDate.month, newDate.year)

	def timer(self, w, dt = 0, last = 0, old = 0, text = None):
		if w.readonly: w.readonly = False
		if old == 0: old = last
		if text == None: text = w.text
		if not text == w.text:
			old = last
			text = w.text

		if last - old > 5:
			last = old
		
		last += dt
		w.time = last		
		if not self.stopTimer:
			if w.focus:
				Clock.schedule_once(lambda dt: self.timer(w = w, dt = dt, last = last, old = old, text = text))
			else:
				Clock.schedule_once(lambda dt: self.timer(w = w, dt = 0, last = last, old = old, text = text))
		else:
			self.stopTimer = False

	def getAnswer(self, w, manual = False, func = None):
		userinput = w.text.replace(',','commaChar').lower()
		try:
			if manual or userinput == self.curWord[0].lower().replace(".", ""):
				self.stopTimer = True
				def t(dt): w.focus = True; w.readonly = True
				Clock.schedule_once(t,-1)
				func(userinput, w.time, self.newWord)
		except Exception as e:
			print(e)
			return

	def start(self):
		self.normal()

	def normal(self):
		self.nextFunc = self.normal2
		if len(self.words) > 0:
			self.curWord = self.words[0]
			self.cWidget.text = "{}/{}".format(len(self.completed) + 1, len(self.words) + len(self.completed) + len(self.uncompleted) + len(self.redo))
			self.curWord =  self.curWord.split(",")
			self.cLabel.text = self.curWord[0].replace("commaChar", ",")
			self.cLabel.font_size = 0

			self.eWidget.text = ''
			self.eWidget.background_color = (1,1,1,1)
			self.eWidget.foreground_color = (0,0,0,1)

			if not 'img-' in self.curWord[1].replace('commaChar', ',') and not 'audio-' in self.curWord[1].replace('commaChar', ','):
				self.tWidget.text = self.curWord[1].replace("commaChar", ",")
			elif 'img-' in self.curWord[1].replace('commaChar', ','):
				imgFile = "{}\\{}\\{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),self.curWord[11],self.curWord[12],consts.images(),self.curWord[1].replace('img-',''))
				img = AsyncImage(source = imgFile)
				self.tWidget = AsyncImage		
			elif 'audio-' in self.curWord[1].replace('commaChar', ','):
				self.tWidget = audLight
				def audPlay(): self.tWidget = audDark; audio.play(self.curWord, a = True); self.tWidget - audLight
				self.tWidget.bind(on_release = lambda x: threading.Thread(target = audPlay, daemon = True).start())

			self.tagsWidget.text = self.curWord[2].replace("commaChar", ",") if not self.curWord[2] == "none" else  ""

			self.timer(self.eWidget)
		else:
			self.uncomplete()

	def normal2(self, answer, time, newWord):
		userinput = answer
		wait = time

		edited = False
		if newWord:
			if newWord[13] == "no":
				self.words.remove(','.join(self.curWord))
				newWord = ','.join(newWord)
				self.words.append(newWord)
			elif newWord[13] == "yes":
				self.words.remove(','.join(self.curWord))
				nhisline = self.curWord[:]
				nhisline.append('none')
				nhisline.append("-1")
				nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
				nhisline.append('-1')
				self.hissentences.append(nhisline)
				newWord = ','.join(newWord)
				self.completed.append(newWord)
			edited = True
			self.nextFunc = self.normal
		else:
			if userinput == self.curWord[0].lower().replace(".", ""):
				self.words.remove(','.join(self.curWord))
				self.eWidget.background_color = (0,1,0,1)
				self.eWidget.foreground_color = (1,1,1,1)
				self.curWord[4] = str(int(self.curWord[4]) + 1)
				self.curWord[5] = str(int(self.curWord[5]) + 1)					
				self.curWord[6] = self.curdate						
				self.curWord[7] = 'success'						
				self.curWord[9] = str(int(self.curWord[9]) + 1)						
				self.curWord[8] = self.addDays(self.curWord)					
				nhisline = self.curWord[:]
				nhisline.append('none')
				nhisline.append("-1")
				nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
				nhisline.append(str(wait))
				self.hissentences.append(nhisline)
				self.curWord = ','.join(self.curWord)
				self.completed.append(self.curWord)
				self.nextFunc = self.normal
			else:
				self.words.remove(','.join(self.curWord))
				self.eWidget.background_color = (1,0,0,1)
				self.eWidget.foreground_color = (1,1,1,1)
				self.curWord[4] = str(int(self.curWord[4]) + 1)
				self.curWord[6] = self.curdate
				self.curWord[7] = 'fail'
				self.curWord[8] = self.addDays(self.curWord)
				self.curWord = ','.join(self.curWord)
				self.redo.append(self.curWord)
				self.nextFunc = self.redoFunc

		Clock.schedule_once(lambda dt: self.afterAnswer(self.eWidget, self.curWord, edited, self.nextFunc),1)

	def redoFunc(self):
		self.nextFunc = self.redoFunc2
		if len(self.redo) > 0:
			self.curWord = self.redo[0]
			self.cWidget.text = "{}/{}".format(len(self.completed) + 1, len(self.words) + len(self.completed) + len(self.uncompleted) + len(self.redo))
			self.curWord =  self.curWord.split(",")
			self.cLabel.text = self.curWord[0].replace("commaChar", ",")
			self.cLabel.font_size = 32

			self.eWidget.text = ''
			self.eWidget.background_color = (1,1,1,1)
			self.eWidget.foreground_color = (0,0,0,1)

			if not 'img-' in self.curWord[1].replace('commaChar', ',') and not 'audio-' in self.curWord[1].replace('commaChar', ','):
				self.tWidget.text = self.curWord[1].replace("commaChar", ",")

			self.tagsWidget.text = self.curWord[2].replace("commaChar", ",") if not self.curWord[2] == "none" else  ""

			self.timer(self.eWidget)

	def redoFunc2(self, answer, time, newWord):
		userinput = answer
		wait = time

		edited = False
		if newWord:
			if newWord[13] == "no":
				self.redo.remove(','.join(self.curWord))
				newWord = ','.join(newWord)
				self.words.append(newWord)
			elif newWord[13] == "yes":
				self.redo.remove(','.join(self.curWord))
				nhisline = self.curWord[:]
				nhisline.append('none')
				nhisline.append("-1")
				nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
				nhisline.append('-1')
				self.hissentences.append(nhisline)
				newWord = ','.join(newWord)
				self.completed.append(newWord)
			edited = True
			self.nextFunc = self.normal
		else:
			if userinput == self.curWord[0].lower().replace(".", ""):
				self.redo.remove(','.join(self.curWord))
				self.eWidget.background_color = (0,1,0,1)
				self.eWidget.foreground_color = (1,1,1,1)
				self.curWord[9] = str(1)
				self.curWord[8] = self.addDays(self.curWord)
				self.curWord.append(str(wait))
				self.curWord = ','.join(self.curWord)
				self.uncompleted.append(self.curWord)
				self.nextFunc = self.normal
			else:
				self.redo.remove(','.join(self.curWord))
				self.eWidget.background_color = (1,0,0,1)
				self.eWidget.foreground_color = (1,1,1,1)
				self.curWord = ','.join(self.curWord)
				self.redo.append(self.curWord)
				self.nextFunc = self.redoFunc

		Clock.schedule_once(lambda dt: self.afterAnswer(self.eWidget, self.curWord, edited, self.nextFunc),1)

	def uncomplete(self):
		self.nextFunc = self.uncomplete2
		if len(self.uncompleted) > 0:
			self.curWord = self.uncompleted[0]
			self.cWidget.text = "{}/{}".format(len(self.completed) + 1, len(self.words) + len(self.completed) + len(self.uncompleted) + len(self.redo))
			self.curWord =  self.curWord.split(",")
			self.cLabel.text = self.curWord[0].replace("commaChar", ",")
			self.cLabel.font_size = 32

			self.eWidget.text = ''
			self.eWidget.background_color = (1,1,1,1)
			self.eWidget.foreground_color = (0,0,0,1)

			if not 'img-' in self.curWord[1].replace('commaChar', ',') and not 'audio-' in self.curWord[1].replace('commaChar', ','):
				self.tWidget.text = self.curWord[1].replace("commaChar", ",")

			self.tagsWidget.text = self.curWord[2].replace("commaChar", ",") if not self.curWord[2] == "none" else  ""

			self.timer(self.eWidget)
		else:
			self.finishLesson()

	def uncomplete2(self, answer, time, newWord):
		userinput = answer
		wait = time
		edited = False
		if newWord:
			if newWord[13] == "no":
				self.uncompleted.remove(','.join(self.curWord))
				newWord = ','.join(newWord)
				self.uncompleted.append(newWord)
			elif newWord[13] == "yes":
				self.uncompleted.remove(','.join(self.curWord))
				nhisline = self.curWord[:-1]
				nhisline.append('none')
				nhisline.append("-1")
				nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
				nhisline.append('-1')
				self.hissentences.append(nhisline)
				newWord = ','.join(newWord)
				self.completed.append(newWord)
			edited = True
			self.nextFunc = self.normal
		else:
			if userinput == self.curWord[0].lower().replace(".", ""):
				self.uncompleted.remove(','.join(self.curWord))
				self.eWidget.background_color = (0,1,0,1)
				self.eWidget.foreground_color = (1,1,1,1)
				self.curWord[9] = str(1)
				self.curWord[8] = self.addDays(self.curWord)
				nhisline = self.curWord[:-1]
				nhisline.append('none')
				nhisline.append("-1")
				nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
				nhisline.append(str(float(self.curWord[15]) + wait))
				del self.curWord[15]
				self.hissentences.append(nhisline)
				self.curWord = ','.join(self.curWord)
				self.completed.append(self.curWord)
				self.nextFunc = self.normal
			else:
				self.uncompleted.remove(','.join(self.curWord))
				self.eWidget.background_color = (1,0,0,1)
				self.eWidget.foreground_color = (1,1,1,1)
				self.curWord = ','.join(self.curWord)
				self.uncompleted.append(self.curWord)
				self.nextFunc = self.normal

		Clock.schedule_once(lambda dt: self.afterAnswer(self.eWidget, self.curWord, edited, self.nextFunc),1)

	def finishLesson(self):

		# for widget in root.winfo_children():
		# 	widget.destroy()
		# 	root.update()
		# text = tk.Label(root, font =(lambda x: Label.cget('font'), 32), text = "Review Done!")
		# text.grid()
		# root.update()

		mycsv.write(consts.workdoc(), mstr = self.completed, lesson = True, review = True)
		mycsv.writeHistory(self.hissentences,  tag = 'review')

		self.controller.controller.doValues()
		self.root.goMainMenu()
