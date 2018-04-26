import io
import os
from datetime import datetime, timedelta
import helpLibs.consts as consts

date = str(datetime.strptime("{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year), "%d/%m/%Y"))
curdate = "{}/{}/{}".format(date.split("-")[2].split(" ")[0], date.split("-")[1], date.split("-")[0])

ml = None
def start():
	global ml
	if not os.path.isfile(consts.workdoc()):
		with open(consts.workdoc(), 'w', encoding = 'utf-8') as t:
			t.write('0SENTENCE,1TRANSLATION,2TAGS,3LEARNED,4ATTEMPTS,5SUCCESFUL ATTEMPS,6DAY LAST ATTEMPT,7LAST ATTEMPT RESULT,8DAY TO REVIEW,9ATTEMPT STREAK,10ID,DECK11,LEVEL12,IGNORE13,LANGUAGE14')
		t.close()
	with open(consts.workdoc(), 'r+', encoding = "utf-8") as f:
		ml = f.read().split("\n")
		print("accessed", datetime.now())

def initt():
	tmpdoc = consts.cwd() + "\\tmpsentences.csv"
	try:
		with open(tmpdoc, 'r+', encoding = "utf-8") as t:
			return tmpdoc
	except:
		with open(tmpdoc, 'w', encoding = "utf-8") as t:
			return tmpdoc

def read(workdoc = None, row = None, option = None):
	if workdoc == None:
		crow = 0
		returnlist = []
		lines = ml
		if row == None:
			if option == None:
				return lines
			elif not option == None:
				for line in lines:
					returnlist.append(line.split(",")[option])
				return returnlist
		elif not row == None:
			if option == None:
				for line in lines:
					if crow == row:
						return line
					crow += 1
			elif not option == None:
				for line in lines:
					if crow == row:
						return line.split(",")[option]
					crow += 1
				return lines
	elif workdoc == consts.workdoc():
		with open(workdoc, 'r+', encoding='utf-8') as p:
			return p.read().split("\n")[1:]
	else:
		with open(workdoc, 'r+', encoding='utf-8') as p:
			return p.read()

def clearlines(workdoc = consts.workdoc(), mstr = None, option = None):
	with open(initt(), 'r+', encoding = "utf-8") as t:
		lines = ml
		t.write(deletework(lines, mstr, option))
	exit(initt(), workdoc)

def deletework(lines, mstr, option):
	returnline = []

	if not type(mstr) == tuple and not type(option) == tuple:
		for line in lines:
			line = line.split(',')
			if line[option] == mstr:
				pass #print(line)
			else:
				returnline.append(",".join(line))
	else:
		for line in lines:
			line = line.split(',')
			if line[option[0]] == mstr[0]:
				if line[option[1]] == mstr[1]:
					pass
				else:
					returnline.append(",".join(line))
			else:
				returnline.append(",".join(line))
				
	return "\n".join(returnline)

def write(workdoc = consts.workdoc(), mstr = None, row = None, option = None, lesson = False, review = False, learn = False, new = False):
	with open(initt(), 'r+', encoding = "utf-8") as t:
		lines = ml
		t.write(writework(lines, mstr, row, option, lesson, review, learn, new))			
	exit(initt(), workdoc)


def writework(lines, mstr, row, option, lesson, review, learn, new):
	returnline = []
	crow = 0
	linecount = len(lines)

	if lesson == False:
		if row == None:
			for line in lines:
				line = line.split(",")
				if line[option] == mstr[0]:
					line[option] = mstr[1]
					returnline.append(','.join(line))
					if not option == 11:
						writeHistory(line, 'edit')
					else:
						try:
							os.rename("{}\\{}\\{}".format(consts.cwd(), consts.fname(), mstr[0], consts.hwdoc()),"{}\\{}\\{}".format(consts.cwd(), consts.fname(), mstr[1], consts.hwdoc()))
						except: pass
				else:
					returnline.append(','.join(line))
		else:
			for line in lines:
				line = line.split(",")
				if (line[11], line[12]) == row:
					line[option] = mstr
					returnline.append(','.join(line))
					writeHistory(line, 'edit')
				else:
					returnline.append(','.join(line))
	else:
		if new == False:
			for line in lines:
				line = line.split(',')
				a,b = doLoop(mstr, line)
				
				if b:
					returnline.append(','.join(a))
					if review:
						pass
						#writeHistory(a, 'review')
					else:
						if learn:
							writeHistory(a, 'learn')
						else:
							writeHistory(a, 'edit')
				else:
					returnline.append(','.join(line))
		else:
			for line in lines:
				returnline.append(line)
			for line in mstr:
				returnline.append(','.join(line))
				writeHistory(line, 'new')
					
	return "\n".join(returnline)

def writeHistory(hline, tag = "None"):
	if not tag == 'review':
		fdir = "{}\\{}\\{}".format(consts.cwd(), consts.fname(), hline[11])
		if not os.path.isdir(fdir):
			os.makedirs(fdir)
		with open("{}\\{}\\{}{}".format(consts.cwd(), consts.fname(), hline[11], consts.hwdoc()), 'a', encoding = 'utf-8') as h:
			hline.append(tag)
			date = str(datetime.strptime("{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year), "%d/%m/%Y"))
			curdate = "{}/{}/{}".format(date.split("-")[2].split(" ")[0], date.split("-")[1], date.split("-")[0])
			hline.append(curdate)
			h.write(','.join(hline) + "\n")
		h.close()
	else:
		for i in hline:
			fdir = "{}\\{}\\{}".format(consts.cwd(), consts.fname(), i[11])
			if not os.path.isdir(fdir):
				os.makedirs(fdir)
			with open("{}\\{}\\{}{}".format(consts.cwd(), consts.fname(), i[11], consts.hwdoc()), 'a', encoding = 'utf-8') as h:
				i[15] = tag
				date = str(datetime.strptime("{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year), "%d/%m/%Y"))
				curdate = "{}/{}/{}".format(date.split("-")[2].split(" ")[0], date.split("-")[1], date.split("-")[0])
				i[16] = curdate
				h.write(','.join(i) + "\n")
			h.close()

def doLoop(mstr, line):
	if type(mstr) is list:
		for i in mstr:
			i = i.split(',')
			if i[10] == line[10]:
				return i, True
		return line, False
	else:
		i = mstr.split(",")
		if i[10] == line[10]:
			return i, True
		return line, False


def exit(tmpdoc, workdoc):
	os.remove(workdoc)
	os.rename(tmpdoc, workdoc)
	start()

start()

