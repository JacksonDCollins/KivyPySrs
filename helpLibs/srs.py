import os
from datetime import datetime, timedelta
import helpLibs.mycsv as mycsv
import helpLibs.audio as audio
import time
import tkinter as tk
import math
import random
from PIL import Image, ImageTk
import helpLibs.consts as consts
import threading
from kivy.clock import Clock


def findTo(r = None, workdoc = consts.workdoc(), *args):
	toReview = []
	rList = []
	lList = []
	tList = []
	curdate = datetime.strptime("{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year), "%d/%m/%Y")
	lines = mycsv.read()
	
	if len(args):
		if r == "review":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == "no":
					d = convertToTime(lines[i].split(",")[8])
					if d <= curdate:
						if lines[i].split(",")[11] == args[0]:
							if lines[i].split(",")[3] == "yes":
								toReview.append(lines[i])
		elif r == "learn":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					if lines[i].split(",")[11] == args[0]:
						if not lines[i].split(",")[3] == "yes":
							toReview.append(lines[i])
		elif r == "total":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					if lines[i].split(",")[11] == args[0]:
						toReview.append(lines[i])
	else:
		if r == "review":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					d = convertToTime(lines[i].split(",")[8])
					if d <= curdate:
						if lines[i].split(",")[3] == "yes":
							toReview.append(lines[i])
		elif r == "learn":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					if not lines[i].split(",")[3] == "yes":
						toReview.append(lines[i])
		elif r == "total":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					toReview.append(lines[i])
		elif r == None: 	
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					d = convertToTime(lines[i].split(",")[8])
					if d <= curdate:
						if lines[i].split(",")[3] == "yes":
							rList.append(lines[i])

					if not lines[i].split(",")[3] == "yes":
						lList.append(lines[i])

					tList.append(lines[i])
			toReview = [rList, lList, tList]
	return toReview

def findDecksAndLevels():
	decks = {}
	lines = mycsv.read()
	j = 0
	for i in lines:
		if j == 1:
			i = i.split(",")
			if not i[11] in decks:
				decks[i[11]] = {}
			if not i[12] in decks[i[11]]:
				decks[i[11]][i[12]] = []
			decks[i[11]][i[12]].append(i)
		else: j = 1
	return decks

def setupNewLesson(deck = None, workdoc = consts.workdoc(), review = True):
	reviewPerLesson = consts.reviewPerLesson()
	newPerLesson = consts.newPerLesson()
	if review:
		selectedReview = []
		tr = findTo("review", workdoc, deck)
		sr = findTo("review")
		if not deck == None:
			if len(tr) >= reviewPerLesson:
				for i in tr:
					if len(selectedReview) < reviewPerLesson:
						selectedReview.append(i)
					else:
						for n,j in enumerate(selectedReview):
							if convertToTime(j.split(',')[8]) > convertToTime(i.split(',')[8]):
								if i not in selectedReview:
									selectedReview[n] = i
			else:
				selectedReview = tr
			return selectedReview
		else:
			if len(sr) >= reviewPerLesson:
				for i in sr:
					if len(selectedReview) < reviewPerLesson:
						selectedReview.append(i)
					else:
						for n,j in enumerate(selectedReview):
							if convertToTime(j.split(',')[8]) > convertToTime(i.split(',')[8]):
								if i not in selectedReview:
									selectedReview[n] = i
			else:
				selectedReview = sr
			return selectedReview
	else:
		selectedLearn = []
		tl = findTo("learn", workdoc, deck)
		for i in tl:
			if len(selectedLearn) < newPerLesson:
				selectedLearn.append(i)
		return selectedLearn

def convertToTime(date):
	return datetime.strptime("{}/{}/{}".format(date.split("/")[0],date.split("/")[1],date.split("/")[2]), "%d/%m/%Y")