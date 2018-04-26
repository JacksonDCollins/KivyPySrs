from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

import guiLibs.browseFromMemrise as browseFromMemrise

class newCards(Screen):
	def __init__(self, controller, **kw):
		super(newCards, self).__init__(**kw)
		self.controller = controller
		b = Button(text = 'Browse from Memrise')
		b.bind(on_release=self.browseMemrise)
		self.add_widget(b)

	def browseMemrise(self, w):
		self.controller.switch_to(browseFromMemrise.browseFromMemrise(self.controller))
