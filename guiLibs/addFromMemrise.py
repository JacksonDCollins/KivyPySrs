import tkinter as tk
import tkinter.ttk as ttk
import guiLibs.rusEntry as rusEntry
import helpLibs.memrise as memrise
import threading

class addFromMemrise(tk.Toplevel):
	def __init__(self, master):
		tk.Toplevel.__init__(self, master)
		self.controller = master
		self.name = None
		self.submitted = False
		self.newCourse = None
		self.geometry("400x100")
		self.protocol("WM_DELETE_WINDOW", self.sendNameClose)
		self.createWidgets()

	def createWidgets(self):
		self.titleLabel = tk.Label(self, text = "Enter whole Url of the Memrise course, e.g. https://www.memrise.com/course/12345/example-course/", wraplength = 400)
		self.titleLabel.pack()

		self.updateLabelVar = tk.StringVar()
		self.updateLabel = tk.Label(self, text = "Ready", textvariable = self.updateLabelVar)
		self.updateLabelVar.set("Ready")
		self.updateLabel.pack()

		self.deckNameEntry = rusEntry.Entry(self)
		self.deckNameEntry.pack()

		self.addDeckButton = tk.Button(self, text = "Add", command = self.sendName)
		self.addDeckButton.pack()

	def sendName(self):
		self.name = self.deckNameEntry.get()
		if not self.name == "":
			self.updateLabelVar.set('Retrieving info')
			self.update()
			self.newCourse = memrise.Course(self.name, self.controller.supportedLangsReversed)

			self.updateLabelVar.set('Downloading')
			self.update()
			self.newCourse.dump_course()

			self.updateLabelVar.set('Cleaning it up')
			self.update()
			self.newCourse.fix()

			self.newCourse = self.newCourse.newCourse
			self.submitted = True

	def sendNameClose(self):
		self.name = None
		self.submitted = True