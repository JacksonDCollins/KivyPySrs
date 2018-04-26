from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

import guiLibs.browseFromMemrise as browseFromMemrise

class newCards(Screen):
	def __init__(self, controller, **kw):
		super(newCards, self).__init__(**kw)
		self.controller = controller
		# b = Button(text = 'Browse from Memrise')
		# b.bind(on_release=self.browseMemrise)
		# self.add_widget(b)
		self.layout = StackLayout()
		self.add_widget(self.layout)
		self.createWidgets()

	def createWidgets(self):
		top = GridLayout(cols = 3, size_hint_y = .5)
		top1 = StackLayout()
		newEntryLabel = Label(text = 'Create new entry')
		top1.add_widget(newEntryLabel)

		top2 = StackLayout()
		newAdditionsLabel = Label(text = 'New additions')
		top2.add_widget(newAdditionsLabel)

		top3 = StackLayout()
		goBackButton = Button(text= 'Go back')
		top3.add_widget(goBackButton)

		top.add_widget(top1)
		top.add_widget(top2)
		top.add_widget(top3)

		self.layout.add_widget(top)

		bot = GridLayout(cols = 3, size_hint_y = .5)
		bot1 = StackLayout()
		newDeckListLabel = Label(text = 'Select deck for new entry')
		bot1.add_widget(newDeckListLabel)

		bot2 = StackLayout()
		newLevelListLabel = Label(text = 'Select level for new entry')
		bot2.add_widget(newLevelListLabel)

		bot3 = StackLayout()
		EntriesListLabel = Label(text = 'Entries in the current level')
		bot3.add_widget(EntriesListLabel)

		bot.add_widget(bot1)
		bot.add_widget(bot2)
		bot.add_widget(bot3)


		self.layout.add_widget(bot)

	def browseMemrise(self, w):
		self.controller.switch_to(browseFromMemrise.browseFromMemrise(self.controller))
