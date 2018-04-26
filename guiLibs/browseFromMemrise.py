import tkinter as tk
import helpLibs.memrise as memrise
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
import queue

from kivy.uix.screenmanager import Screen
from kivy.uix.listview import ListView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
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
from kivy.uix.image import AsyncImage

def doTWork(self, func, args = {}, kwargs = {}, after = None, daemon = False):
	t = threading.Thread(target = func, args = args, kwargs = kwargs)
	t.daemon = daemon
	t.start()
	if not daemon:
		while t.isAlive():
			Clock.tick()
	if after: after()

def getH(text, width):
			m = ToggleButton(text=text, padding_y = 10)
			m.text_size[0] = width
			m.texture_update()
			s = m.texture_size[1]
			return s

class ListboxWidget(ScrollView):
	def __init__(self, layout = None, l1 = 0, mp = 0, **kw):
		super(ListboxWidget, self).__init__(**kw)
		self.resultsFrame = StackLayout(size_hint_y = None)
		self.gridlayout = layout
		self.l1 = l1
		self.curGrid = None
		self.resultsFrame.bind(minimum_height=self.resultsFrame.setter('height'))
		self.add_widget(self.resultsFrame)

	def getH(text, width):
		m = ToggleButton(text=text, padding_y = 10)
		m.text_size[0] = width
		m.texture_update()
		s = m.texture_size[1]
		return s

	def add_grid_widget(self, w):
		if not self.curGrid:
			self.curGrid = GridLayout(rows = 1, size_hint_y = None)
			self.resultsFrame.add_widget(self.curGrid)
			self.curGrid.add_widget(w)
			self.curGrid = GridLayout(cols = 3, size_hint_y = None)
		elif len(self.curGrid.children) == 3:
			self.curGrid = GridLayout(cols = 3, size_hint_y = None)
			self.resultsFrame.add_widget(self.curGrid)
			self.curGrid.add_widget(w)
		else:
			self.curGrid.add_widget(w)
		



class browseFromMemrise(Screen):
	def __init__(self, controller, **kw):
		super(browseFromMemrise, self).__init__(**kw)
		self.controller = controller
		self.mname = None
		self.newCourse = None
		self.submitted = None
		
		self.layout = GridLayout(cols = 2)
		self.add_widget(self.layout)
		self.createWidgets()
		
	def on_enter(self):
		self.loadingLabel.text = 'Loading'
		self.populate()

	def createWidgets(self):
		LeftLayout = StackLayout(size_hint_x = .25)
		self.langsLBoxDict = {}
		self.langsLBox = ListboxWidget(scroll_type = ['bars','content'], bar_width = 20, size_hint_y = None)
		LeftLayout.add_widget(self.langsLBox)
		
		self.langsLBoxDict2 = {}
		self.langsLBox2 = ListboxWidget(scroll_type = ['bars','content'], bar_width = 20, size_hint_y = None)
		LeftLayout.add_widget(self.langsLBox2)

		self.langsLBoxDict3 = {}
		self.langsLBox3 = ListboxWidget(scroll_type = ['bars','content'], bar_width = 20, size_hint_y = None)
		#self.layout.add_widget(self.langsLBox3)

		self.loadMoreButton = Button(text ='Load more', size_hint_y = None)#, command = self.loadMoreFunc)
		self.loadMoreButton.bind(on_release=self.loadMoreFunc)
		LeftLayout.add_widget(self.loadMoreButton)

		self.loadingLabel = Label(text = 'Ready', size_hint_y = None)
		LeftLayout.add_widget(self.loadingLabel)

		self.layout.add_widget(LeftLayout)

		self.coursesHolder = ListboxWidget(scroll_type = ['bars','content'], bar_width = 20, size_hint_y = 1, size_hint_x = .75, mp = 100)
		self.layout.add_widget(self.coursesHolder)

	def t(self): self.browser.loadMore()
	def loadMoreFunc(self, w):
		self.loadingLabel.text = 'Loading'
		self.showCourses(page = self.browser.loadMore())
		self.loadingLabel.text = 'Ready'

	def k(self): self.browser = memrise.CourseBrowser()	
	def populate(self):
		doTWork(self, self.k)
		self.langsLBox.resultsFrame.clear_widgets()
		for i in self.browser.coursesDict:
			b = ToggleButton(text = i, group = self.langsLBox, size_hint_y = None, halign = 'center', valign = 'center')
			b.text_size[0] = self.langsLBox.resultsFrame.size[0]
			b.height = getH(i, self.langsLBox.resultsFrame.size[0])
			b.i = i
			b.bind(on_release = self.lBoxSelect)#self.popLevelsLView(self.levelsLBox, self.deckLevels[a.i], a.i))
			self.langsLBox.resultsFrame.add_widget(b)
		self.loadingLabel.text = 'Ready'

	#def p(self, b): self.browser.loadCourses(self.browser.allLangsHrefs[b])
	def lBoxSelect(self,e):
		if e.parent.parent == self.langsLBox:
			self.langsLBox2.resultsFrame.clear_widgets()
			for i in self.browser.coursesDict[e.i]:
				b = ToggleButton(text = i, group = self.langsLBox2, size_hint_y = None, halign = 'center', valign = 'center')
				b.text_size[0] = self.langsLBox2.resultsFrame.size[0]
				b.height = getH(i, self.langsLBox2.resultsFrame.size[0])
				b.i = i
				b.bind(on_release = self.lBoxSelect)#self.popLevelsLView(self.levelsLBox, self.deckLevels[a.i], a.i))
				self.langsLBox2.resultsFrame.add_widget(b)

		if e.parent.parent == self.langsLBox2:
			self.loadingLabel.text = 'Loading'
			#doTWork(self, self.p, kwargs = {'b':e.i}, after = lambda: self.showCourses(self.browser.allLangsHrefs[e.i]))
			self.browser.loadCourses(e.i)
			self.showCourses(url = self.browser.allLangsHrefs[e.i])
			self.loadingLabel.text = 'Ready'

	def showCourses(self, url = None, page = None):
		if not page:
			toAdd = self.browser.getCourses(url)
		else:
			toAdd = self.browser.getCourses(page = page)
		
		col = 0
		row = 0
		
		self.coursesHolder.resultsFrame.clear_widgets()

		for n,i in enumerate(toAdd):
			p = courseHolder(self, i, size_hint_y = None)
			self.coursesHolder.resultsFrame.add_widget(p)
			self.coursesHolder.resultsFrame.add_widget(Widget(size_hint_y = None, height = 100))
			


class courseHolder(StackLayout):
	def __init__(self, controller, *args, **kw):
		super(courseHolder, self).__init__(**kw)
		self.controller = controller
		self.code = args[0]

		Ctype = None
		t = self.code.attrs['class'][0]
		if t == 'featured-course-box':
			Ctype = 'featured'
		elif t == 'course-box-wrapper':
			Ctype = 'normal'
		
		self.renderCourseFrame(Ctype, self.code)

	def downloadCourse(self, url):
		self.controller.sendName(url)

	def renderCourseFrame(self, Ctype, code):
		if Ctype == 'featured':
			courseName = code.find('div.details', first = True).find('h2', first = True).text
			coursePicture = code.find('div.picture-wrap', first = True).find('img', first = True).attrs['src']
			courseDesc = code.find('div.description', first = True).text
			courseLearning = code.find('div.stats', first = True).find('span.stat')[0].text
			courseDuration = code.find('div.stats', first = True).find('span.stat')[1].text
			courseAuthor = code.find('div.details-wrap', first = True).find('strong', first = True).text
			courseUrl = code.absolute_links.pop() #code.attrs['href']
			
			
			leftL = GridLayout(cols = 1, size_hint_y = 1)
			rightL = GridLayout(cols = 1, size_hint_y = 1)

			courseNameLabel = Label(text = courseName, halign = 'center', valign = 'center')
			rightL.add_widget(courseNameLabel)
			courseNameLabel.text_size = courseNameLabel.size
			
			coursePictureFrame = AsyncImage(source = coursePicture)
			leftL.add_widget(coursePictureFrame)
			
			#doTWork(self.controller, downloadPic, kwargs={'coursePicture':coursePicture,'size':(128,128)}, after = self.update, daemon = True)

			
			courseLearningLabel = Label(text = 'Learning: {}'.format(courseLearning), size_hint_y = .2)
			rightL.add_widget(courseLearningLabel)


			courseDurationLabel = Label(text = 'Duration: {}'.format(courseDuration), size_hint_y = .2)
			rightL.add_widget(courseDurationLabel)

			courseAuthorLabel = Label(text = 'Author: {}'.format(courseAuthor), size_hint_y = .2)
			rightL.add_widget(courseAuthorLabel)

			courseDownloadButton = Button(text = 'Download', height = 10)
			courseDownloadButton.bind(on_release = lambda w: self.downloadCourse(courseUrl)) #, command = lambda: self.downloadCourse(courseUrl))
			leftL.add_widget(courseDownloadButton)

			g = GridLayout(cols = 2)
			g.add_widget(leftL)
			g.add_widget(rightL)
			

			courseDescLabel = Label(text = courseDesc, halign = 'center', valign = 'center')

			self.add_widget(g)
			self.add_widget(courseDescLabel)

		elif Ctype == 'normal':
			
			courseName = code.find('a[class = "inner"]', first = True).text
			coursePicture = code.find('div[class = "course-box-picture"]', first = True).attrs['style']
			coursePicture = coursePicture.split('"')[1].split('"')[0]
			courseLearning = code.find('div.stats', first = True).find('span.stat')[0].text
			courseDuration = code.find('div.stats', first = True).find('span.stat')[0].text
			try: courseAuthor = code.find('span[class = "author pull-right"]', first = True).find('a', first = True).text
			except:	courseAuthor = 'UserDeleted'
			courseUrl = code.find('a[class = "inner"]', first = True).attrs['href']

			leftL = GridLayout(cols = 1, size_hint_y = 1)
			rightL = GridLayout(cols = 1, size_hint_y = 1)

			courseNameLabel = Label(text = courseName, halign = 'center', valign = 'center')
			rightL.add_widget(courseNameLabel)
			courseNameLabel.text_size = courseNameLabel.size
			
			coursePictureFrame = AsyncImage(source = coursePicture)
			leftL.add_widget(coursePictureFrame)
			
			#doTWork(self.controller, downloadPic, kwargs={'coursePicture':coursePicture,'size':(128,128)}, after = self.update, daemon = True)

			
			courseLearningLabel = Label(text = 'Learning: {}'.format(courseLearning), size_hint_y = .2)
			rightL.add_widget(courseLearningLabel)


			courseDurationLabel = Label(text = 'Duration: {}'.format(courseDuration), size_hint_y = .2)
			rightL.add_widget(courseDurationLabel)

			courseAuthorLabel = Label(text = 'Author: {}'.format(courseAuthor), size_hint_y = .2)
			rightL.add_widget(courseAuthorLabel)

			courseDownloadButton = Button(text = 'Download', height = 10)#, command = lambda: self.downloadCourse(courseUrl))
			courseDownloadButton.bind(on_release = lambda w: self.downloadCourse(courseUrl))
			leftL.add_widget(courseDownloadButton)

			g = GridLayout(cols = 2)
			g.add_widget(leftL)
			g.add_widget(rightL)

			self.add_widget(g)