import tkinter as tk
import tkinter.ttk as ttk

import math
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button

import helpLibs.audio as audio
import helpLibs.mycsv as mycsv
import helpLibs.consts as consts

import guiLibs.DecksAndLevels
import guiLibs.editEntry as editEntry

class newSearch(Screen):
	def __init__(self, controller, **kw):
		super(newSearch, self).__init__(**kw)
		self.controller = controller
		self.searchArray = {}
		self.audioController = audio.lessonAudioBytes()

		self.changed = False
		self.total = mycsv.read(workdoc = consts.workdoc())
		self.layout = StackLayout()
		self.add_widget(self.layout)
		self.createWidgets()

	def createWidgets(self):
		topLayout = GridLayout(cols = 2, size_hint_y = .1)
		self.layout.add_widget(topLayout)
		self.searchBox = TextInput(font_size = 24, multiline = False)
		self.searchBox.bind(text = lambda w, x: self.updateResults(args = x))
		self.backButton = Button(text = "Go back", size_hint_x = None)
		self.backButton.bind(on_release = self.goback)
		topLayout.add_widget(self.searchBox)
		topLayout.add_widget(self.backButton)


		self.pageLayout = GridLayout(cols = 3, size_hint_y = .05)
		self.layout.add_widget(self.pageLayout)

		lastButton = Button(text='Previous page')
		lastButton.bind(on_release=self.lastPage)
		self.pageLabel = Label(text='Page /')
		nextButton = Button(text='Next page')
		nextButton.bind(on_release=self.nextPage)
		self.pageLayout.add_widget(lastButton)
		self.pageLayout.add_widget(self.pageLabel)
		self.pageLayout.add_widget(nextButton)

		self.resultsFrame = StackLayout(size_hint_y = None)
		self.resultsFrame.curBox = 0
		self.resultsFrame.lines = None
		self.resultsFrame.bind(minimum_height=self.resultsFrame.setter('height'))

		self.scv = ScrollView(scroll_type = ['bars','content'], bar_width = 20, size_hint_y = .85)
		self.layout.add_widget(self.scv)

	def goback(self, *w):
		if self.changed:
			self.controller.doValues()
		self.controller.switch_to(guiLibs.DecksAndLevels.DecksAndLevels(self))

	def nextPage(self, *w):
		if not (len(self.resultsFrame.lines)/100) <= self.resultsFrame.curBox + 1: 
			self.resultsFrame.curBox += 1
			self.showResults()

	def lastPage(self, *w):
		if not self.resultsFrame.curBox  == 0: 
			self.resultsFrame.curBox -= 1
			self.showResults()

	def updateResults(self, args = None, reset = False):
		total = self.total

		if reset:
			mlist = list(self.searchArray.keys())
			for j in mlist:
				args = j
				index = mlist.index(j)
				self.searchArray[j] = []
				if index == 0:
					self.searchArray[j] = total
				else:
					self.searchArray[j] = [x for x in self.searchArray[mlist[index-1]] if args in x.split(',')[1] or args in x.split(',')[0]]
		else:
			if not args in self.searchArray:
				self.searchArray[args] = []
				mlist = list(self.searchArray.keys())
				index = mlist.index(args)

				if index == 0:
					self.searchArray[args] = total
				else:
					self.searchArray[args] = [x for x in self.searchArray[mlist[index-1]] if args in x.split(',')[1] or args in x.split(',')[0]]
			else:
				mlist = list(self.searchArray.keys())
				index = mlist.index(args)
				for i in range(index+1, len(self.searchArray)):
					del self.searchArray[mlist[i]]

		self.showResults(self.searchArray[args])

	def showResults(self, lines = None):
		self.resultsFrame.clear_widgets()
		self.scv.clear_widgets()
		if lines:
			self.resultsFrame.curBox = 0
			self.resultsFrame.lines = lines
		
		for i in range(100*self.resultsFrame.curBox, (100*self.resultsFrame.curBox) +  100):
			try:
				layout = GridLayout(cols = 3, size_hint_y = None)
				line = self.resultsFrame.lines[i].split(',')

				l = Label(text = '{}: {}'.format(line[0], line[1]), size_hint_y = 1, padding_y = 10)
				l.width = self.resultsFrame.width
				l.texture_update()
				
				layout.height  = l.texture_size[1]
				layout.add_widget(l)

				b = Button(text = 'View/edit', size_hint_y = 1, size_hint_x = None)
				b.line = line
				b.bind(on_release=self.editEntry)
				layout.add_widget(b)

				w = Widget(size_hint_x = None, width = 20)
				layout.add_widget(w)

				self.resultsFrame.add_widget(layout)
			except: pass
			
		self.scv.add_widget(self.resultsFrame)
		self.scv.scroll_y = 1
		self.pageLabel.text = 'Page {}/{}'.format(self.resultsFrame.curBox + 1, math.ceil(len(self.resultsFrame.lines)/100))

	def editEntry(self, w):
		self.editEntrytl = editEntry.editEntry(self, w.line, size_hint_x = 0.8)
		self.editEntrytl.open()
	
	def deleteWord(self, line):
		mycsv.clearlines(mstr = line[10], option = 10)
		self.total = mycsv.read(workdoc = consts.workdoc())
		self.updateResults(reset = True)
		self.changed = True
		
	def editWord(self, line, new):
		mycsv.write(mstr = ','.join(new), lesson = True, review = True)
		self.total = mycsv.read(workdoc = consts.workdoc())
		self.updateResults(reset = True)
		self.changed = True

class mnewSearch(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		self.controller = controller
		self.searchArray = {}
		self.size = "900x600"
		self.bind("<<ShowFrame>>", self.on_show_frame)

	def on_show_frame(self, event):
		for widget in self.winfo_children():
			widget.destroy()
		self.controller.controller.geometry(self.size)
		self.createWidgets()

	def createWidgets(self):
		self.searchBox = rusEntry.Entry(self,  font = (lambda x: self.cget('font'), 24), width = 45)
		self.searchBox.bind('<<textEntered>>', lambda event:self.updateResults(args = event, w = self.searchBox))
		self.searchBox.grid()

		self.backButton = tk.Button(self, text = "Go back", command = self.goback)
		self.backButton.grid(column = 1, row = 0, sticky = 'n')

		self.resultsFrame = tk.Frame(self)
		self.resultsFrame.grid(column = 0, row = 1)
		self.resultsLBoxScrollBar = tk.Scrollbar(self.resultsFrame, orient = tk.VERTICAL)
		self.resultsLBoxScrollBar.pack(side = tk.RIGHT, fill = tk.Y)

		self.resultsLBox = tk.Listbox(self.resultsFrame, font = (lambda x: self.cget('font'), 12), selectmode = "BROWSE", exportselection=0, width = 90, name = "results", yscrollcommand = self.resultsLBoxScrollBar.set)
		self.resultsLBox.pack()
		self.resultsLBox.bind('<<ListboxSelect>>', self.resultsLBoxSelect)

		self.resultsLBoxScrollBar.config(command = self.resultsLBox.yview)

		self.frame = tk.Frame(self)
		self.frame.grid(row = 2, column = 0)
		
		self.updateResults(args = True)

	def resultsLBoxSelect(self, е):
		if not self.resultsLBox.curselection() == ():
			self.line = self.searchArray[self.curSearch][self.resultsLBox.curselection()[0]][0]
			self.createEditFrameWidgets(self.frame, self.line, search = True)
	
	def removeBad(self, list):
		for i in self.searchArray:
			if (not i == self.curSearch) and (not i in self.curSearch):
				del self.searchArray[i]
				return self.removeBad(self.searchArray)
		return True
	
	def updateResults(self, args = None, reset = False, w = None):
		k = None
		total = self.controller.controller.total
		if isinstance(args, tk.Event):
			k = self.curSearch
			self.curSearch = w.get().lower()
			if len(k) > len(self.curSearch):
				back = True
			else: 
				back = False
		elif args == True:
			self.curSearch = ""
			back = False			

		if not reset:
			if self.curSearch == "":
				self.searchArray[self.curSearch] = []
				for i in [x.split(",") for x in total]:
					self.searchArray[self.curSearch].append((i,"{}: {}".format(i[0],i[1]).replace("commaChar", ",")))
			else:
				if not back:
					self.searchArray[self.curSearch] = []
					for n,j in enumerate(self.searchArray.keys()):
						for i in [x for x in self.searchArray[list(self.searchArray.keys())[n-1]] if j == self.curSearch]:
							if self.curSearch in i[1].lower(): self.searchArray[self.curSearch].append((i[0],i[1]))
				else:
					if self.curSearch not in self.searchArray:
						self.searchArray[self.curSearch] = []
						for n,j in enumerate(self.searchArray.keys()):
							for i in [x for x in self.searchArray[list(self.searchArray.keys())[n-1]] if j in x[1] and j == self.curSearch]:
								self.searchArray[j].append((i[0],i[1]))
		else:
			for n,j in enumerate(self.searchArray.keys()):
				self.searchArray[j] = []
				if j == "":
					for i in [x.split(",") for x in total if j in x.split(",")[1].lower()]:
						self.searchArray[j].append((i,"{}: {}".format(i[0],i[1]).replace("commaChar", ",")))
				else:
					for i in [x for x in self.searchArray[list(self.searchArray.keys())[n-1]] if j in x[1]]:
						self.searchArray[j].append((i[0],i[1]))
				self.curSearch = j

		self.removeBad(self.searchArray)
		self.resultsLBox.delete(0,tk.END)
		for i in self.searchArray[self.curSearch]:
			self.resultsLBox.insert(tk.END, i[1])

	def createEditFrameWidgets(self, frame, line, search = False):
		self.labels = []
		self.entries = []

		for w in frame.winfo_children():
			w.destroy()

		self.textLabel = tk.Label(frame, text = "Entry")
		self.labels.append(self.textLabel)

		self.textEntry = rusEntry.Entry(frame)
		self.entries.append(self.textEntry)

		self.transLabel = tk.Label(frame, text = "Translation")
		self.labels.append(self.transLabel)

		self.transEntry = rusEntry.Entry(frame)
		self.entries.append(self.transEntry)

		self.tagsLabel = tk.Label(frame, text = "Tags")
		self.labels.append(self.tagsLabel)

		self.tagsEntry = tk.Entry(frame)
		self.entries.append(self.tagsEntry)

		self.learnedLabel = tk.Label(frame, text = "Learned")
		self.labels.append(self.learnedLabel)

		self.learnedEntry = tk.Label(frame, text = "-")
		self.entries.append(self.learnedEntry)

		self.attemptsLabel = tk.Label(frame, text = "Attmpts")
		self.labels.append(self.attemptsLabel)

		self.attemptsEntry = tk.Label(frame, text = "-")
		self.entries.append(self.attemptsEntry)

		self.successfulAttemptsLabel = tk.Label(frame, text = "Successful attempts")
		self.labels.append(self.successfulAttemptsLabel)

		self.successfulAttemptsEntry = tk.Label(frame, text = "-")
		self.entries.append(self.successfulAttemptsEntry)

		self.dayLastAttemptLabel = tk.Label(frame, text = "Day of last attempt")
		self.labels.append(self.dayLastAttemptLabel)

		self.dayLastAttemptEntry = tk.Label(frame, text = "-")
		self.entries.append(self.dayLastAttemptEntry)

		self.lastAttemptResultLabel = tk.Label(frame, text = "Result of last attempt")
		self.labels.append(self.lastAttemptResultLabel)

		self.lastAttemptResultEntry = tk.Label(frame, text = "-")
		self.entries.append(self.lastAttemptResultEntry)

		self.dayToReviewLabel = tk.Label(frame, text = "Day of next review")
		self.labels.append(self.dayToReviewLabel)

		self.dayToReviewEntry = tk.Label(frame, text = "-")
		self.entries.append(self.dayToReviewEntry)

		self.attemptStreakLabel = tk.Label(frame, text = "Attempt streak")
		self.labels.append(self.attemptStreakLabel)

		self.attemptStreakEntry = tk.Label(frame, text = "-")
		self.entries.append(self.attemptStreakEntry)

		self.idLabel = tk.Label(frame, text = "ID")
		self.labels.append(self.idLabel)

		self.idLabel2 = tk.Label(frame, text = "-")
		self.entries.append(self.idLabel2)

		self.deckLabel = tk.Label(frame, text = "Deck")
		self.labels.append(self.deckLabel)

		self.deckEntry = tk.Entry(frame)
		self.entries.append(self.deckEntry)

		self.levelLabel = tk.Label(frame, text = "Level")
		self.labels.append(self.levelLabel)

		self.levelEntry = tk.Entry(frame)
		self.entries.append(self.levelEntry)

		self.ignoreLabel = tk.Label(frame, text = "Ignore")
		self.labels.append(self.ignoreLabel)

		self.ignoreEntry = tk.Label(frame, text = "-")
		self.entries.append(self.ignoreEntry)

		self.langLabel = tk.Label(frame, text = "Language")
		self.labels.append(self.langLabel)

		self.langEntry = tk.Entry(frame)
		self.entries.append(self.langEntry)

		for n,w in enumerate(self.labels):
			w.grid(row = n, column = 1)
		for n,w in enumerate(self.entries):
			w.grid(row = n, column = 2)
			if w['text'] == "-":
				w['text'] = line[n]
			else:
				w.insert(0, line[n].replace("commaChar", ","))
			w['width'] = 55

		if self.ignoreEntry['text'] == "no":
			self.ignoreCheck = tk.Checkbutton(frame, command = self.ignoreCheckFunc)
			self.ignoreCheck.grid(column = 3, row = 13)
		else:
			self.ignoreCheck = tk.Checkbutton(frame, command = self.ignoreCheckFunc)
			self.ignoreCheck.grid(column = 3, row = 13)
			self.ignoreCheck.toggle()
		
		self.listenButton = tk.Button(frame, text = "Listen", command = self.listen)
		self.listenButton.grid(column = 3, row = 0)
		
		if not search:
			self.saveButton = tk.Button(frame, text = "Save", command = self.saveEdits)
			self.saveButton.grid(column = 1, columnspan = 2)
		else:
			self.saveButton = tk.Button(frame, text = "Save", command = self.saveEditsSearch)
			self.saveButton.grid(column = 1, columnspan = 2)

		self.deleteEntryButton = tk.Button(frame, text = "Delete entry", command = lambda: self.deleteEntry(line[10]))
		self.deleteEntryButton.grid(row  = 15, column = 3, columnspan = 2)

	def deleteEntry(self, ID):
		mycsv.clearlines(mstr = ID, option = 10)
		for w in self.winfo_children():
			w.destroy()
		self.createWidgets()

	def ignoreCheckFunc(self):
		if self.ignoreEntry['text'] == "no":
			self.ignoreEntry['text'] = "yes"
		else:
			self.ignoreEntry['text'] ="no"

	def listen(self):
		audio.preload(self.line)
		audio.play()

	def saveEditsSearch(self):
		newline = []
		self.changes = []
		for n,w in enumerate(self.entries):
			try:
				newline.append(w.get().replace(",", "commaChar"))
			except:
				newline.append(w['text'])
		self.changes.append(','.join(newline))

		mycsv.write(mstr = self.changes, lesson = True)
		self.controller.controller.doValues()
		self.updateResults(args = True, reset = True)

	def goback(self):
		self.controller.show_frame("DecksAndLevels", me = self)