from kivy.uix.screenmanager import Screen
from kivy.uix.listview import ListView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.adapters.models import SelectableDataItem
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.listview import ListItemButton, ListView
from kivy.clock import Clock

import helpLibs.srs as srs
import helpLibs.audio as audio
import helpLibs.mycsv as mycsv

import guiLibs.Search as Search
import guiLibs.newCards as newCards
import guiLibs.mainMenu

def getH(text, width):
			m = ToggleButton(text=text, padding_y = 10)
			m.text_size[0] = width
			m.texture_update()
			s = m.texture_size[1]
			return s

class DataItem(SelectableDataItem):
	def __init__(self, text, width, height, val = None, is_selected=False):
		self.is_selected = is_selected
		self.text = text
		self.name = val
		self.size = (width, height)

class ListboxWidget(ScrollView):
	def __init__(self, **kw):
		super(ListboxWidget, self).__init__(**kw)
		self.resultsFrame = StackLayout(size_hint_y = None)
		self.resultsFrame.bind(minimum_height=self.resultsFrame.setter('height'))
		self.add_widget(self.resultsFrame)

	def getH(text, width):
		m = ToggleButton(text=text, padding_y = 10)
		m.text_size[0] = width
		m.texture_update()
		s = m.texture_size[1]
		return s

class DecksAndLevels(Screen):
	def __init__(self, controller, **kw):
		super(DecksAndLevels, self).__init__(**kw)
		self.controller = controller
		self.layout = GridLayout(cols = 2)
		self.add_widget(self.layout)
		self.audio = audio.lessonAudioBytes()
		self.lastDeck = ()
		self.lastLevel = ()
		self.lastEntry = ()
		self.deckLevels = srs.findDecksAndLevels()
		self.changes = []
		self.changed = False

	def on_pre_enter(self):
		self.createWidgets()
		# self.deckLevels = self.controller.controller.dandl
		# self.lastDeck = ()
		# self.lastLevel = ()
		# self.lastEntry = ()

	def popDecksLView(self, LView, Data):
		LView.resultsFrame.clear_widgets()

		for i in Data:
			b = ToggleButton(text = i, group = LView, size_hint_y = None, halign = 'center', valign = 'center')
			b.text_size[0] = LView.resultsFrame.size[0]
			b.height = getH(i.replace('commaChar', ','), LView.resultsFrame.size[0])
			b.i = i
			b.bind(on_release = lambda a: self.popLevelsLView(self.levelsLBox, self.deckLevels[a.i], a.i))
			LView.resultsFrame.add_widget(b)

	def popLevelsLView(self, LView, Data, Text):
		self.createEditDeckWidgets(Text)
		self.entriesLBox.resultsFrame.clear_widgets()
		LView.resultsFrame.clear_widgets()

		for i in Data:
			b = ToggleButton(text = i, group = LView, size_hint_y = None, halign = 'center', valign = 'center')
			b.text_size[0] = LView.resultsFrame.size[0]
			b.height = getH(i.replace('commaChar', ','), LView.resultsFrame.size[0])
			b.i = i
			b.bind(on_release = lambda a: self.popEnteriesLView(self.entriesLBox, self.deckLevels[Text][a.i], Text, a.i))
			LView.resultsFrame.add_widget(b)

	def popEnteriesLView(self, LView, Data, Text, TText):
		self.createEditLevelWidgets(Text, TText)
		LView.resultsFrame.clear_widgets()

		for i in Data:
			b = ToggleButton(text = '{}: {}'.format(i[0].replace('commaChar', ','), i[1].replace('commaChar', ',')), group = LView, size_hint_y = None, halign = 'center', valign = 'center')
			b.text_size[0] = LView.resultsFrame.size[0]
			b.height = getH('{}: {}'.format(i[0].replace('commaChar', ','), i[1].replace('commaChar', ',')), LView.resultsFrame.size[0])
			b.i = i
			b.bind(on_release = lambda a: self.createEditEntryWidgets(a.i))
			LView.resultsFrame.add_widget(b)

	def on_enter(self):
		self.popDecksLView(self.decksLBox, self.deckLevels)
		
	def createWidgets(self):
		self.layout.clear_widgets()
		
		leftContainer = GridLayout(rows = 2)
		self.lboxLayout = GridLayout(cols = 3, size_hint_y = None, height = 200)
		leftContainer.add_widget(self.lboxLayout)

		self.decksLBox = ListboxWidget(scroll_type = ['bars','content'], bar_width = 20)
		self.lboxLayout.add_widget(self.decksLBox)

		self.levelsLBox = ListboxWidget(scroll_type = ['bars','content'], bar_width = 20)
		self.lboxLayout.add_widget(self.levelsLBox)

		self.entriesLBox = ListboxWidget(scroll_type = ['bars','content'], bar_width = 20)
		self.lboxLayout.add_widget(self.entriesLBox)

		self.f = StackLayout(size_hint_x = None)
		self.buttonGoBack = Button(text = "Go Back and commit entry saves", size_hint_y = None, height = 600/8, halign = 'center', valign = 'center')
		self.buttonGoBack.text_size[0] = self.buttonGoBack.size[0]
		self.buttonGoBack.bind(on_release = self.goMainMenu)
		self.f.add_widget(self.buttonGoBack)

		self.searchButton = Button(text = "Search", size_hint_y = None, height = 600/8, halign = 'center', valign = 'center')
		self.searchButton.text_size[0] = self.searchButton.size[0]
		self.searchButton.bind(on_release = self.search)
		self.f.add_widget(self.searchButton)

		self.newButton = Button(text = "Add new decks and entries", size_hint_y = None, height = 600/8, halign = 'center', valign = 'center')
		self.newButton.text_size[0] = self.newButton.size[0]
		self.newButton.bind(on_release = self.new)
		self.f.add_widget(self.newButton)

		self.selectButtons = StackLayout(size_hint_y = None)
		self.f.add_widget(Widget(size_hint_y = None, height = 2*(600/8)))
		self.f.add_widget(self.selectButtons)

		self.editFrame = GridLayout(cols = 2)
		leftContainer.add_widget(self.editFrame)
		self.layout.add_widget(leftContainer)
		self.layout.add_widget(self.f)

	def new(self, w):
		self.controller.controller.switch_to(newCards.newCards(self.controller.controller))
		
	def search(self, w):
		self.controller.controller.switch_to(Search.newSearch(self.controller.controller))

	def goMainMenu(self, *args):
		# DecksAndLevelsFuncs.goMainMenu(self)
		if len(self.changes) > 0:
			mycsv.write(mstr = self.changes, lesson = True)
			self.controller.controller.doValues()
			self.controller.controller.switch_to(guiLibs.mainMenu.mainMenu(self.controller.controller))
			return

		if self.changed:
			self.controller.controller.doValues()
			self.controller.controller.switch_to(guiLibs.mainMenu.mainMenu(self.controller.controller))
			return

		self.controller.controller.switch_to(guiLibs.mainMenu.mainMenu(self.controller.controller))

	def createEditDeckWidgets(self, deck):
		self.editFrame.clear_widgets()
		self.selectButtons.clear_widgets()

		self.deckNameLabel = Label(text = "Deck Name")
		self.editFrame.add_widget(self.deckNameLabel)

		self.deckNameEntry = TextInput(text = deck, multiline=False)
		self.editFrame.add_widget(self.deckNameEntry)

		self.totalLevelsLabel = Label(text = "Total Levels")
		self.editFrame.add_widget(self.totalLevelsLabel)

		self.totalLevelsLabel2 = Label(text = str(len(self.deckLevels[deck])))
		self.editFrame.add_widget(self.totalLevelsLabel2)

		self.totalEntriesLabel = Label(text = "Total entries")
		self.editFrame.add_widget(self.totalEntriesLabel)
		
		tc = 0
		d = self.deckLevels[deck]
		for e in d:
			tc += len(d[e])
		self.totalLevelsLabel1 = Label(text = str(tc))
		self.editFrame.add_widget(self.totalLevelsLabel1)

		self.saveButton = Button(text = "Save", size_hint_y = None, height = 600/8)
		self.saveButton.bind(on_release = lambda w: self.saveEditsDeck(deck))
		self.selectButtons.add_widget(self.saveButton)

		self.deleteDeckButton = Button(text = "Delete deck", size_hint_y = None, height = 600/8)
		self.deleteDeckButton.bind(on_release = lambda w: self.deleteDeck(deck))
		self.selectButtons.add_widget(self.deleteDeckButton)

	def deleteDeck(self, deck):
		mycsv.clearlines(mstr = deck, option = 11)
		self.deckLevels = srs.findDecksAndLevels()
		self.createWidgets()
		Clock.schedule_once(lambda dt: self.popDecksLView(self.decksLBox, self.deckLevels), 0)
		self.changed = True

	def saveEditsDeck(self, origDeckName):
		newDeckName = self.deckNameEntry.text
		mycsv.write(mstr = (origDeckName, newDeckName), option = 11)
		self.deckLevels = srs.findDecksAndLevels()
		self.createWidgets()
		Clock.schedule_once(lambda dt: self.popDecksLView(self.decksLBox, self.deckLevels), 0)
		self.changed = True

	def createEditLevelWidgets(self, deck, level):
		self.editFrame.clear_widgets()
		self.selectButtons.clear_widgets()

		self.levelNameLabel = Label(text = "Deck Name")
		self.editFrame.add_widget(self.levelNameLabel)

		self.levelNameLabel2 = Label(text = level)
		self.editFrame.add_widget(self.levelNameLabel2)

		self.totalEntriesLabel = Label(text = "Total Entries")
		self.editFrame.add_widget(self.totalEntriesLabel)

		self.totalEntriesLabel2 = Label(text = str(len(self.deckLevels[deck][level])))
		self.editFrame.add_widget(self.totalEntriesLabel2)

		self.ignoreAllLabel = Label(text = "Ignore level?")
		self.editFrame.add_widget(self.ignoreAllLabel)

		
		self.ignoreAllCheckbutton = CheckBox()#command = lambda: self.ignoreAll(deck, level, self.v.get()), variable = self.v, onvalue = "yes", offvalue = "no")
		self.editFrame.add_widget(self.ignoreAllCheckbutton)
		for j in self.deckLevels[deck][level]:
			if j[13] == "no":
				self.ignoreAllCheckbutton.active = False
				break
			else:
				self.ignoreAllCheckbutton.active = True
		self.ignoreAllCheckbutton.bind(active = lambda c, v: self.ignoreAll(deck, level, v))

		self.deleteLevelButton = Button(text = "Delete level", size_hint_y = None, height = 600/8)#, command = lambda: self.deleteLevel(deck, level))
		self.deleteLevelButton.bind(on_release = lambda w: self.deleteLevel(deck, level))
		self.selectButtons.add_widget(self.deleteLevelButton)

	def deleteLevel(self, deck, level):
		mycsv.clearlines(mstr = (deck,level), option = (11,12))
		self.deckLevels = srs.findDecksAndLevels()
		self.createWidgets()
		Clock.schedule_once(lambda dt: self.popDecksLView(self.decksLBox, self.deckLevels), 0)
		self.changed = True

	def ignoreAll(self, deck, level, val):
		if val:
			val = 'yes'
		else:
			val = 'no'
		mycsv.write(mstr = val, row = (deck, level), option = 13)
		self.deckLevels = srs.findDecksAndLevels()
		self.changed = True

	def createEditEntryWidgets(self, line):
		self.editFrame.clear_widgets()
		self.selectButtons.clear_widgets()

		self.labels = []
		self.entries = []

		self.textLabel = Label(text = "Entry")
		self.labels.append(self.textLabel)

		self.textEntry = TextInput(multiline=False)
		self.entries.append(self.textEntry)

		self.transLabel = Label(text = "Translation")
		self.labels.append(self.transLabel)

		self.transEntry = TextInput(multiline=False)
		self.entries.append(self.transEntry)

		self.tagsLabel = Label(text = "Tags")
		self.labels.append(self.tagsLabel)

		self.tagsEntry = TextInput(multiline=False)
		self.entries.append(self.tagsEntry)

		self.learnedLabel = Label(text = "Learned")
		self.labels.append(self.learnedLabel)

		self.learnedEntry = Label(text = "-")
		self.entries.append(self.learnedEntry)

		self.attemptsLabel = Label(text = "Attmpts")
		self.labels.append(self.attemptsLabel)

		self.attemptsEntry = Label(text = "-")
		self.entries.append(self.attemptsEntry)

		self.successfulAttemptsLabel = Label(text = "Successful attempts")
		self.labels.append(self.successfulAttemptsLabel)

		self.successfulAttemptsEntry = Label(text = "-")
		self.entries.append(self.successfulAttemptsEntry)

		self.dayLastAttemptLabel = Label(text = "Day of last attempt")
		self.labels.append(self.dayLastAttemptLabel)

		self.dayLastAttemptEntry = Label(text = "-")
		self.entries.append(self.dayLastAttemptEntry)

		self.lastAttemptResultLabel = Label(text = "Result of last attempt")
		self.labels.append(self.lastAttemptResultLabel)

		self.lastAttemptResultEntry = Label(text = "-")
		self.entries.append(self.lastAttemptResultEntry)

		self.dayToReviewLabel = Label(text = "Day of next review")
		self.labels.append(self.dayToReviewLabel)

		self.dayToReviewEntry = Label(text = "-")
		self.entries.append(self.dayToReviewEntry)

		self.attemptStreakLabel = Label(text = "Attempt streak")
		self.labels.append(self.attemptStreakLabel)

		self.attemptStreakEntry = Label(text = "-")
		self.entries.append(self.attemptStreakEntry)

		self.idLabel = Label(text = "ID")
		self.labels.append(self.idLabel)

		self.idLabel2 = Label(text = "-")
		self.entries.append(self.idLabel2)

		self.deckLabel = Label(text = "Deck")
		self.labels.append(self.deckLabel)

		self.deckEntry = TextInput(multiline=False)
		self.entries.append(self.deckEntry)

		self.levelLabel = Label(text = "Level")
		self.labels.append(self.levelLabel)

		self.levelEntry = TextInput(multiline=False)
		self.entries.append(self.levelEntry)

		self.ignoreLabel = Label(text = "Ignore")
		self.labels.append(self.ignoreLabel)

		self.ignoreCheck = CheckBox()
		self.entries.append(self.ignoreCheck)

		self.langLabel = Label(text = "Language")
		self.labels.append(self.langLabel)

		self.langEntry = TextInput(multiline=False)
		self.entries.append(self.langEntry)

		ignore = [self.attemptsLabel, self.dayLastAttemptLabel, self.lastAttemptResultLabel, self.attemptStreakLabel]
		for n,w in enumerate(self.labels):
			self.entries[n].text = line[n]
			if w in ignore: continue

			self.editFrame.add_widget(w)
			self.editFrame.add_widget(self.entries[n])
			
		if self.ignoreCheck.text == 'no':
			self.ignoreCheck.active = False
		elif self.ignoreCheck.text == 'yes':
			self.ignoreCheck.active = True
		self.ignoreCheck.bind(active = self.ignoreCheckFunc)
		
		
		self.listenButton = Button(text = "Listen", size_hint_y = None, height = 600/8)#
		self.listenButton.bind(on_release = lambda w: self.listen(line))
		self.selectButtons.add_widget(self.listenButton)
		
		self.saveButton = Button(text = "Save", size_hint_y = None, height = 600/8)
		self.saveButton.bind(on_release = self.saveEdits)
		self.selectButtons.add_widget(self.saveButton)

		self.deleteEntryButton = Button(text = "Delete entry", size_hint_y = None, height = 600/8)
		self.deleteEntryButton.bind(on_release = lambda w: self.deleteEntry(line[10]))
		self.selectButtons.add_widget(self.deleteEntryButton)
		
	def deleteEntry(self, ID):
		mycsv.clearlines(mstr = ID, option = 10)
		self.deckLevels = srs.findDecksAndLevels()
		self.createWidgets()
		Clock.schedule_once(lambda dt: self.popDecksLView(self.decksLBox, self.deckLevels), 0)
		self.changed = True

	def ignoreCheckFunc(self, w, v):
		if v:
			w.text = "yes"
		else:
			w.text = "no"

	def saveEdits(self, w):
		newline = []
		for n,w in enumerate(self.entries):
			newline.append(w.text)
		
		if newline[10] in [x.split(',')[10] for x in self.changes]:
			self.changes.remove([x for x in self.changes if x.split(',')[10] == newline[10]][0])
		
		self.changes.append(','.join(newline))

		self.deckLevels = srs.findDecksAndLevels()
		self.createWidgets()
		Clock.schedule_once(lambda dt: self.popDecksLView(self.decksLBox, self.deckLevels), 0)
		self.changed = True
		
		# lsel = self.entriesLBox.curselection()
		# for n,i in enumerate(self.levelsLBox.get(0, tk.END)):
		# 	if i == self.levelsLBox.get(self.levelsLBox.curselection()):
		# 		self.levelsLBox.selection_set(n)
		# 		self.levelsLBoxSelect(None)
		# self.entriesLBox.selection_set(lsel)
		# self.entriesLBoxSelect(None)

	def listen(self, line):
		self.audio.play(line)