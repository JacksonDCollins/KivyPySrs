from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.clock import Clock
import threading

import helpLibs.consts as consts
import helpLibs.srs as srs
import helpLibs.audio as audio

import guiLibs.reviewLesson as reviewLesson
import guiLibs.learnLesson as learnLesson
import guiLibs.analytics as Analytics
import guiLibs.DecksAndLevels as DecksAndLevels

class DeckEntry(GridLayout):
	def __init__(self, controller, *args, **kw):
		super(DeckEntry, self).__init__(**kw)
		self.controller = controller
		self.deck = args[0]

		top = GridLayout(cols = 2)

		deckName = Label(text = "{}".format(args[0]), size_hint_y = 1, size_hint_x = 1, valign = 'center')
		deckName.text_size[0] = 240
		top.add_widget(deckName)

		reviewButton = Button(text = "Review: {}".format(args[1]), size_hint_x = .5)
		top.add_widget(reviewButton)
		reviewButton.bind(on_release=lambda w: threading.Thread(target = lambda: self.controller.reviewLesson(w, self.deck), daemon = True).start())
		if args[1] == 0:
			reviewButton.disabled = True

		self.add_widget(top)

		middle = GridLayout(cols = 2)

		toLearn = Label(text = "{}/{} words learned".format(args[3] - args[2], args[3]), size_hint_y = 1, size_hint_x = 1, valign = 'center')
		toLearn.text_size[0] = 240
		middle.add_widget(toLearn)

		learnButton = Button(text = "Learn", size_hint_x = .5)
		middle.add_widget(learnButton)
		learnButton.bind(on_release=lambda w: threading.Thread(target = lambda: self.controller.learnLesson(w, self.deck), daemon = True).start())
		self.add_widget(middle)

		pb = ProgressBar(max = args[3], value = args[3] - args[2])
		self.add_widget(pb)

		if args[3] - args[2] == args[3]:
			learnButton.disabled = True

class Decks(StackLayout):
	def __init__(self, controller, **kw):
		super(Decks, self).__init__(**kw)
		self.controller = controller

		for n,i in enumerate([x for x in self.controller.controller.dandl if self.controller.controller.deckLangs[x] == self.controller.curlang]):
			self.add_widget(Widget(size_hint_y=None, height = 10))
			self.add_widget(DeckEntry(self.controller, i, self.controller.controller.reviewCounts[i], self.controller.controller.learnCounts[i], self.controller.controller.totalCounts[i], size_hint_y = None, rows = 3))
			self.add_widget(Widget(size_hint_y=None, height = 10))

class OtherWidgets(GridLayout):
	def __init__(self, controller, **kw):
		super(OtherWidgets, self).__init__(**kw)
		self.controller = controller

		reviewButton = Button(text = "Review: {}".format(len(self.controller.controller.toReview)))
		self.add_widget(reviewButton)
		if len(self.controller.controller.toReview) == 0:
			reviewButton.disabled = True
		reviewButton.bind(on_release=lambda w: threading.Thread(target = lambda: self.controller.reviewLesson(w, None), daemon = True).start())

		buttonDecksAndLevels = Button(text = "Decks and Levels")
		self.add_widget(buttonDecksAndLevels)
		buttonDecksAndLevels.bind(on_release=self.controller.DecksAndLevels)

		analyticsButton = Button(text = "Analytics")
		self.add_widget(analyticsButton)
		analyticsButton.bind(on_release=self.controller.analytics)

		settingsButton = Button(text = "Settings")
		self.add_widget(settingsButton)
		settingsButton.bind(on_release=self.controller.settings)

class mainMenu(Screen):
	def __init__(self, controller, **kw):
		super(mainMenu, self).__init__(**kw)
		self.name = __name__
		self.controller = controller
		self.Grid = GridLayout(cols = 2)
		self.add_widget(self.Grid)
		if consts.defaultLang():
			self.curlang = consts.defaultLang()
		else:
			if not self.controller.langs == {}:
				self.curlang = [self.controller.langs[x] for x in self.controller.langs][len(self.controller.langs) -1]
			else:
				self.controller.langs = {'none': 'None'}
				self.curlang = [self.controller.langs[x] for x in self.controller.langs][len(self.controller.langs) -1]
		#self.createWidgets()

	def on_pre_enter(self):
		self.redo()

	def reviewLesson(self, widget, *args):
		self.loadLabel.text = "Gathering files: "
		r = srs.setupNewLesson(deck = args[0])
		def t():
			for n,i in enumerate(r):
				if 'audio-' in i.split(',')[1]: continue
				self.loadLabel.text = "Gathering files: {}/{}".format(n+1,len(r))
				#audio.preload(i.split(','))
			self.controller.switch_to(reviewLesson.reviewLesson(self, r))
		threading.Thread(target = t, daemon = True).start()
		self.loadLabel.text = ""
		
	def learnLesson(self, widget, *args):
		self.loadLabel.text = "Gathering files: "
		r = srs.setupNewLesson(deck = args[0], review = False)
		def t():
			for n,i in enumerate(r):
				if 'audio-' in i.split(',')[1]: continue
				self.loadLabel.text = "Gathering files: {}/{}".format(n+1,len(r))
				#audio.preload(i.split(','))	
			self.controller.switch_to(learnLesson.learnLesson(self, r))
		threading.Thread(target = t, daemon = True).start()
		self.loadLabel.text = ""	
		
	def DecksAndLevels(self, widget):
		self.controller.switch_to(DecksAndLevels.DecksAndLevels(self))

	def analytics(self, widget):
		self.controller.switch_to(Analytics.Analytics(self))

	def settings(self, widget):
		self.controller.controller.open_settings()

	def add_w(self, widget):
		self.Grid.add_widget(widget)
			
	def createWidgets(self):
		decks = Decks(self, orientation = 'lr-tb', size_hint_y = None)
		decks.bind(minimum_height=decks.setter('height'))

		self.scv = ScrollView()
		self.scv.add_widget(decks)
		self.add_w(self.scv)

		bl = BoxLayout(orientation = 'vertical')
		bl.add_widget(OtherWidgets(self, cols = 2, rows = 2))

		vals = [self.controller.langs[x] for x in self.controller.langs]
		dropdown = DropDown()
		for i in vals:
			label = Button(text = i, size_hint_y = None, height=40)
			label.bind(on_release = lambda lbl:dropdown.select(lbl.text))
			dropdown.add_widget(label)

		mainD = Button(text = self.curlang, size_hint_x = 1, size_hint_y = None, height = 50)
		mainD.bind(on_release=dropdown.open)

		def set(t,q,x): setattr(t,q,x); self.chooseLang(x)
		dropdown.bind(on_select=lambda instance, x: set(mainD, 'text', x))

		self.loadLabel = Label(text= '', size_hint_y = .5)
		bl.add_widget(self.loadLabel)
		bl.add_widget(Label(text='Language', size_hint_y = None))
		bl.add_widget(mainD)
		bl.add_widget(Widget())
		self.add_w(bl)

	def chooseLang(self, x):
		if not x == self.curlang:
			self.curlang = x
			self.redo()

	def redo(self):
		self.Grid.clear_widgets()
		self.createWidgets()