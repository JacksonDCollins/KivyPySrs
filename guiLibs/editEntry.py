from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class editEntry(Popup):
	def __init__(self, controller, line, **kw):
		super(editEntry, self).__init__(**kw)
		self.line = line[:]
		self.newLine = line[:]
		self.controller = controller
		self.layout = GridLayout(cols = 2)
		self.selectButtons = GridLayout(rows = 1)

		self.createWidgets()

		self.layout.add_widget(self.selectButtons)

		b = Button(text='Exit')
		b.bind(on_release=self.dismiss)

		self.layout.add_widget(b)
		self.content = self.layout

	def createWidgets(self):
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

		self.langEntry = Label(text = "-")
		self.entries.append(self.langEntry)

		ignore = [self.attemptsLabel, self.dayLastAttemptLabel, self.lastAttemptResultLabel, self.attemptStreakLabel, self.deckLabel, self.levelLabel]
		for n,w in enumerate(self.labels):
			self.entries[n].text = self.newLine[n]
			if w in ignore: continue

			self.layout.add_widget(w)
			self.layout.add_widget(self.entries[n])
			
		if self.ignoreCheck.text == 'no':
			self.ignoreCheck.active = False
		elif self.ignoreCheck.text == 'yes':
			self.ignoreCheck.active = True
		self.ignoreCheck.bind(active = self.ignoreCheckFunc)
		
		
		self.listenButton = Button(text = "Listen", height = 600/8)#
		self.listenButton.bind(on_release = self.listen)
		self.selectButtons.add_widget(self.listenButton)
		
		self.saveButton = Button(text = "Save", height = 600/8)
		self.saveButton.bind(on_release = self.saveEdits)
		self.selectButtons.add_widget(self.saveButton)

		self.deleteEntryButton = Button(text = "Delete entry", height = 600/8)
		self.deleteEntryButton.bind(on_release = lambda w: self.deleteEntry(self.line[10]))
		self.selectButtons.add_widget(self.deleteEntryButton)

	def ignoreCheckFunc(self, w, v):
		if v:
			w.text = "yes"
		else:
			w.text = "no"

	def saveEdits(self, w):
		for n,w in enumerate(self.entries):
			self.newLine[n] = w.text
		self.dismiss()
		self.controller.editWord(self.line, self.newLine)

	def listen(self, w):
		self.controller.audioController.play(self.line)

	def deleteEntry(self, ID):
		self.dismiss()
		self.controller.deleteWord(self.line)
'''
class meditEntry(tk.Toplevel):
	def __init__(self, master, line):
		tk.Toplevel.__init__(self, master)
		self.geometry("500x500")
		self.master = master
		self.createWidgets()

	def createWidgets(self):
		self.labels = []
		self.entries = []

		self.textLabel = tk.Label(self, text = "Entry")
		self.labels.append(self.textLabel)

		self.textEntry = rusEntry.Entry(self)
		self.entries.append(self.textEntry)

		self.transLabel = tk.Label(self, text = "Translation")
		self.labels.append(self.transLabel)

		self.transEntry = rusEntry.Entry(self)
		self.entries.append(self.transEntry)

		self.tagsLabel = tk.Label(self, text = "Tags")
		self.labels.append(self.tagsLabel)

		self.tagsEntry = tk.Entry(self)
		self.entries.append(self.tagsEntry)

		self.learnedLabel = tk.Label(self, text = "Learned")
		self.labels.append(self.learnedLabel)

		self.learnedEntry = tk.Label(self, text = "-")
		self.entries.append(self.learnedEntry)

		self.attemptsLabel = tk.Label(self, text = "Attmpts")
		self.labels.append(self.attemptsLabel)

		self.attemptsEntry = tk.Label(self, text = "-")
		self.entries.append(self.attemptsEntry)

		self.successfulAttemptsLabel = tk.Label(self, text = "Successful attempts")
		self.labels.append(self.successfulAttemptsLabel)

		self.successfulAttemptsEntry = tk.Label(self, text = "-")
		self.entries.append(self.successfulAttemptsEntry)

		self.dayLastAttemptLabel = tk.Label(self, text = "Day of last attempt")
		self.labels.append(self.dayLastAttemptLabel)

		self.dayLastAttemptEntry = tk.Label(self, text = "-")
		self.entries.append(self.dayLastAttemptEntry)

		self.lastAttemptResultLabel = tk.Label(self, text = "Result of last attempt")
		self.labels.append(self.lastAttemptResultLabel)

		self.lastAttemptResultEntry = tk.Label(self, text = "-")
		self.entries.append(self.lastAttemptResultEntry)

		self.dayToReviewLabel = tk.Label(self, text = "Day of next review")
		self.labels.append(self.dayToReviewLabel)

		self.dayToReviewEntry = tk.Label(self, text = "-")
		self.entries.append(self.dayToReviewEntry)

		self.attemptStreakLabel = tk.Label(self, text = "Attempt streak")
		self.labels.append(self.attemptStreakLabel)

		self.attemptStreakEntry = tk.Label(self, text = "-")
		self.entries.append(self.attemptStreakEntry)

		self.idLabel = tk.Label(self, text = "ID")
		self.labels.append(self.idLabel)

		self.idLabel2 = tk.Label(self, text = "-")
		self.entries.append(self.idLabel2)

		self.deckLabel = tk.Label(self, text = "Deck")
		self.labels.append(self.deckLabel)

		self.deckEntry = tk.Entry(self)
		self.entries.append(self.deckEntry)

		self.levelLabel = tk.Label(self, text = "Level")
		self.labels.append(self.levelLabel)

		self.levelEntry = tk.Entry(self)
		self.entries.append(self.levelEntry)

		self.ignoreLabel = tk.Label(self, text = "Ignore")
		self.labels.append(self.ignoreLabel)

		self.ignoreEntry = tk.Label(self, text = "-")
		self.entries.append(self.ignoreEntry)

		self.langLabel = tk.Label(self, text = "Language")
		self.labels.append(self.langLabel)

		self.langEntry = tk.Entry(self)
		self.entries.append(self.langEntry)

		for n,w in enumerate(self.labels):
			w.grid(row = n, column = 1)
		for n,w in enumerate(self.entries):
			w.grid(row = n, column = 2, sticky = 'w', columnspan = 999)
			w['width'] = 55
			if w == self.ignoreEntry:
				w['width'] = 50

			if w['text'] == "-":
				w['text'] = self.master.line[n]
			else:
				w.insert(0, self.master.line[n].replace("commaChar", ","))

		self.ignoreCheck = tk.Checkbutton(self, command = self.ignoreCheckFunc)
		self.ignoreCheck.grid(column = 875, row = 13, sticky = 'e')
		if self.ignoreEntry['text'] == "yes":
			self.ignoreCheck.select()
		else:
			self.ignoreCheck.deselect()

		self.saveButton = tk.Button(self, text = "Save", command = self.saveEdits)
		self.saveButton.grid(column = 0, columnspan = 2)

	def ignoreCheckFunc(self):
		if self.ignoreEntry['text'] == "no":
			self.ignoreEntry['text'] =  "yes"
		else:
			self.ignoreEntry['text'] = "no"

	def saveEdits(self):
		self.master.lineEdited = True
		for n,w in enumerate(self.entries):
			try:
				self.master.line[n] = w.get().replace(",", "commaChar")
			except:
				self.master.line[n] = w['text']
'''