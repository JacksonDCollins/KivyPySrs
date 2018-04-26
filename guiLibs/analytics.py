from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.graphics import *

import helpLibs.consts as consts
import helpLibs.mycsv as mycsv
import helpLibs.srs as srs

import guiLibs.mainMenu

import threading
from datetime import timedelta as td
import math

class Analytics(Screen):
	def __init__(self, controller, **kw):
		super(Analytics, self).__init__(**kw)
		self.controller = controller.controller
		self.root = controller
		
		self.layout = GridLayout(cols = 1)
		self.add_widget(self.layout)

	def convertStrTimeAddDays(self, date, days = 0):
		k = srs.convertToTime(date) + td(days = days)
		return "{}/{}/{}".format(k.day, k.month, k.year), k

	def drawBar(self):
		c_width = self.canvas.size[0]
		c_height = self.canvas.size[1]
		# stretch enough to get all data items in
		x_stretch = 35
		x_width = 35
		# gap between left canvas edge and y axis
		x_gap = 35
		text_height = 100
		
		l = 0
		for j in self.root.controller.days:
			if len(self.root.controller.days[j]) > l:
				l = len(self.root.controller.days[j])
		self.canvas.highest = l
		
		s = 0
		t = 0
		m = 0
		for x, j in enumerate(self.root.controller.days):
			y = len(self.root.controller.days[j])
			x = x-t
			if y == 0:
				t += 1
				continue

			p = (self.convertStrTimeAddDays(j), self.convertStrTimeAddDays(mycsv.curdate))
			if (p[0][1] - p[1][1]).days > consts.month():
				break
			else:
				m = m + 1
				s = s + len(self.root.controller.days[j])

			#calculate reactangle coordinates (integers) for each bar
			width = x_width# x * x_stretch + x * x_width + x_gap
			height = (y/l) * (c_height - text_height)
			xCo = x * x_stretch + x * x_width #+ x_width + x_gap
			yCo = text_height #c_height
			# draw the bar
			self.canvas.addBar(len(self.root.controller.days[j]), str(j), str(y)) #[xCo, yCo, width, height])

		hours = math.floor(self.root.controller.hoursLearn)
		minutes = math.floor(self.root.controller.minutesLearn)
		seconds = math.floor(self.root.controller.secondsLearn)

		line = ("Words reviewed today: {} in {}:{}:{}\nWords learned today: {}".format(self.root.controller.donetoday, hours, minutes, seconds,self.root.controller.learnedtoday))
		self.ldonetoday.text = line

		m = consts.month()
		if s/m > (len(self.root.controller.toReview) + self.root.controller.donetoday):
			s = (len(self.root.controller.toReview) + self.root.controller.donetoday) *m
		self.recommendedDaily = math.ceil(s/m)
		self.lrecommendedDaily = Label(text ="Today you should review {} words".format(self.recommendedDaily), size_hint_y= None, padding_y = 10)
		self.layout.add_widget(self.lrecommendedDaily)
		self.lrecommendedDaily.texture_update()
		self.lrecommendedDaily.height = self.lrecommendedDaily.texture_size[1]

	def on_pre_enter(self):
		self.createWidgets()
		
	def on_enter(self):
		self.drawBar()

	def on_leave(self):
		self.layout.clear_widgets()

	def createWidgets(self):
		def t(s, v):
			s.texture_update()
			s.height = s.texture_size[1]

		buttonGoBack = Button(text = "Go Back", size_hint_y=None, height = 30)
		buttonGoBack.bind(on_release=self.goMainMenu)
		self.layout.add_widget(buttonGoBack)

		self.l = Label(text = "REVIEW FORECAST",size_hint_y = None, padding_y = 10)
		self.layout.add_widget(self.l)
		self.l.texture_update()
		self.l.height = self.l.texture_size[1]

		self.canvas = Graph(size_hint_y = 1)
		self.layout.add_widget(self.canvas)

		self.ldonetoday = Label(size_hint_y = None, padding_y = 10)
		self.layout.add_widget(self.ldonetoday)
		self.ldonetoday.bind(text = t)
		

	def goMainMenu(self, *args):
		self.controller.switch_to(guiLibs.mainMenu.mainMenu(self.controller))

class Graph(StackLayout):
	def __init__(self, **kw):
		super(Graph, self).__init__(**kw)
		self.inner = GridLayout(rows=1, size_hint=(None,1))
		self.inner.bind(minimum_width=self.inner.setter('width'))

		self.scroll = ScrollView(size_hint=(1,1), do_scroll_x=True, do_scroll_y=False, scroll_type = ['bars','content'], bar_width = 20)
		self.scroll.add_widget(self.inner)
		self.scroll.bind(scroll_x=self.reBars)

		self.add_widget(self.scroll)

		self.bars = []
		self.highest = 0
		with self.canvas.before:
		    Color(1, 1, 1, 1) # green; colors range from 0-1 instead of 0-255
		    self.rect = Rectangle(size=self.size,
		                           pos=self.pos)

		self.bind(pos=self.update_rect, size=self.update_rect)

	def reBars(self, a, p, *c):
		x = len(self.bars)
		x_stretch = 35
		x_width = 35
		furthest = x * x_stretch + x * x_width

		f = (p*furthest) - (p*self.size[0])

		for i in self.bars:
				i.scroll(x=f)

	def update_rect(self, instance = None, value = None):
		self.inner.clear_widgets()
		x = len(self.bars)
		x_stretch = 35
		x_width = 35
		furthest = x * x_stretch + x * x_width
		d = (furthest/2)*(2/3)
		if d < self.size[0]:
			d *= (self.size[0]/(d+1))
			d += (d/self.size[0])*self.size[0]

		self.inner.add_widget(Widget(size = (d,1), size_hint=(None,None)))

		self.rect.pos = self.pos
		self.rect.size = self.size
		for i in self.bars:
				i.resize(h=self.size[1])
			
	def addBar(self, mheight, y, j):
		x = len(self.bars) + 1
		x_stretch = 35
		x_width = 35
		x_gap = 35
		text_height = 100

		xCo = x * x_stretch + x * x_width #+ x_width + x_gap
		yCo = text_height #c_height
		width = x_width
		height = (mheight/self.highest * self.height) - (text_height * (mheight/self.highest)) - (yCo * (mheight/self.highest))

		coords = (xCo, yCo, width, height)
		
		with self.inner.canvas:
			Color(1, 0, 0, 1)
			bar = mRect(labels = (y,j), par = self.inner, isBar = True, pos = (xCo, yCo), size=(width, height))
			self.bars.append(bar)


class mRect(Rectangle):
	def __init__(self, labels = (None, None), par = None, isBar = False, **kw):
		super(mRect, self).__init__(**kw)
		self.root = par
		self.isBar = isBar
		self.mylabels = []

		self.origPos = self.pos
		self.origHeight = self.size[1]
		self.origWidth = self.size[0]
		self.origParHeight = self.root.size[1]
		self.makeLabels(labels)
		
	def scroll(self, x = 0, y = 0):
		self.pos = (self.origPos[0] - x, self.origPos[1] - y)
		for label in self.mylabels:
			label.scroll(x=x)

	def resize(self, h):
		if self.isBar:
			self.size = (self.size[0], self.origHeight * (h/self.origParHeight))
		for label in self.mylabels:
			label.resize()

	def makeLabels(self, labels):
		with self.root.canvas:
			myLabel = CoreLabel(text = labels[0], color = (0,0,0,1))
			myLabel.refresh()
			tex = myLabel.texture
			tex_size = list(tex.size)
			
			self.mylabels.append(halfRect(self, 'bottom', texture=tex, size=tex_size, pos=((self.pos[0]-tex_size[0]/2)+self.size[0]/2,self.pos[1]-tex_size[1])))

			myLabel = CoreLabel(text = labels[1], color = (0,0,0,1))
			myLabel.refresh()
			tex = myLabel.texture
			tex_size = list(tex.size)

			label = halfRect(self, 'top', texture=tex, size=tex_size, pos=((self.pos[0]-tex_size[0]/2)+self.size[0]/2,self.pos[1]+tex_size[1]+self.size[1]))
			self.mylabels.append(label)

class halfRect(Rectangle):
	def __init__(self, par, mtype, **kw):
		super(halfRect, self).__init__(**kw)
		self.root = par
		self.mtype = mtype
		self.origPos = self.pos

	def resize(self):
		if self.mtype == 'top':
			self.pos = ((self.root.pos[0]-self.texture.size[0]/2)+self.root.size[0]/2,self.root.pos[1]+self.texture.size[1]+self.root.size[1])
		elif self.mtype == 'bottom':
			self.pos = ((self.root.pos[0]-self.texture.size[0]/2)+self.root.size[0]/2,self.root.pos[1]-self.texture.size[1])

	def scroll(self, x = 0):
		self.pos = (self.origPos[0] - x, self.pos[1])