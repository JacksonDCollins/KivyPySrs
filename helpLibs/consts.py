import json

json_settings = json.dumps([{
	'type':'path',
	'title':'Data directory',
	'desc':'Directory for all PySrs reltaed files and backups',
	'section':'GENERAL',
	'key':'cwd'
	},{
	'type':'numeric',
	'title':'Month value',
	'desc':'Value for calculations in Analytics, leave at 30',
	'section':'GENERAL',
	'key':'month'
	},{
	'type':'path',
	'title':'Work Document',
	'desc':'Path to the document containing all sentences',
	'section':'GENERAL',
	'key':'workdoc'
	},{
	'type':'string',
	'title':'Folder for history files',
	'desc':'Folder for all files critical to presereving history',
	'section':'GENERAL',
	'key':'hwdoc'
	},{
	'type':'string',
	'title':'Data folder name',
	'desc':'Name of the folder for data',
	'section':'GENERAL',
	'key':'fname'
	},{
	'type':'string',
	'title':'Picture folder name',
	'desc':'Name of the picture folder',
	'section':'GENERAL',
	'key':'images'
	},{
	'type':'path',
	'title':'Backup directory',
	'desc':'Directory for storing all backups',
	'section':'GENERAL',
	'key':'backups'
	},{
	'type':'numeric',
	'title':'New words per lesson',
	'desc':'How many new words to learn per lesson',
	'section':'GENERAL',
	'key':'newPerLesson'
	},{
	'type':'numeric',
	'title':'Review words per lesson',
	'desc':'Amount of words to review per review lesson',
	'section':'GENERAL',
	'key':'reviewPerLesson'
	},{
	'type':'string',
	'title':'Default languge',
	'desc':'Defualt language to load courses for on startup',
	'section':'GENERAL',
	'key':'defaultLang'
	}])

import ctypes.wintypes
CSIDL_PERSONAL = 5      # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value

buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

workloc = buf.value + '\PySrs\config'
confile = workloc + '\config.ini'

import os
os.environ['KIVY_HOME'] = workloc
os.environ['KIVY_NO_FILELOG'] = '1'

from kivy.config import Config
Config.read(confile)
Config.setdefaults('GENERAL', {'cwd': workloc,
						 'month': 30,
						 'workdoc': workloc + '\sentences.csv',
						 'hwdoc': '\history.csv',
						 'fname': 'data',
						 'images':'pics',
						 'backups': workloc + '\\backups\\',
						 'reviewPerLesson': 25,
						 'defaultLang': 'None'})

def cwd():
	Config.read(confile)
	return Config['GENERAL']['cwd']
def month():
	Config.read(confile)
	return int(Config['GENERAL']['month'])
def workdoc():
	Config.read(confile)
	return Config['GENERAL']['workdoc']
def hwdoc():
	Config.read(confile)
	return Config['GENERAL']['hwdoc']
def fname():
	Config.read(confile)
	return Config['GENERAL']['fname']
def backups():
	Config.read(confile)
	return Config['GENERAL']['backups']
def newPerLesson():
	Config.read(confile)
	return int(Config['GENERAL']['newPerLesson'])
def reviewPerLesson():
	Config.read(confile)
	return int(Config['GENERAL']['reviewPerLesson'])
def defaultLang():
	Config.read(confile)
	return Config['GENERAL']['defaultLang']
def images():
	Config.read(confile)
	return Config['GENERAL']['images']
def supportedLangs():
	return {'none' : 'None', 'af' : 'Afrikaans', 'sq' : 'Albanian', 'ar' : 'Arabic', 'hy' : 'Armenian', 'bn' : 'Bengali', 'ca' : 'Catalan', 'zh' : 'Chinese', 'zh-cn' : 'Chinese (Mandarin/China)', 'zh-tw' : 'Chinese (Mandarin/Taiwan)', 'zh-yue' : 'Chinese (Cantonese)', 'hr' : 'Croatian', 'cs' : 'Czech', 'da' : 'Danish', 'nl' : 'Dutch', 'en' : 'English', 'en-au' : 'English (Australia)', 'en-uk' : 'English (United Kingdom)', 'en-us' : 'English (United States)', 'eo' : 'Esperanto', 'fi' : 'Finnish', 'fr' : 'French', 'de' : 'German', 'el' : 'Greek', 'hi' : 'Hindi', 'hu' : 'Hungarian', 'is' : 'Icelandic', 'id' : 'Indonesian', 'it' : 'Italian', 'ja' : 'Japanese', 'km' : 'Khmer (Cambodian)', 'ko' : 'Korean', 'la' : 'Latin', 'lv' : 'Latvian', 'mk' : 'Macedonian', 'no' : 'Norwegian', 'pl' : 'Polish', 'pt' : 'Portuguese', 'ro' : 'Romanian', 'ru' : 'Russian', 'sr' : 'Serbian', 'si' : 'Sinhala', 'sk' : 'Slovak', 'es' : 'Spanish', 'es-es' : 'Spanish (Spain)', 'es-us' : 'Spanish (United States)', 'sw' : 'Swahili', 'sv' : 'Swedish', 'ta' : 'Tamil', 'th' : 'Thai', 'tr' : 'Turkish', 'uk' : 'Ukrainian', 'vi' : 'Vietnamese', 'cy' : 'Welsh'}
