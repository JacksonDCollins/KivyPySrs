import helpLibs.mainGui as mainGui

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-2d6f6fb1de93.json', scope)


gc = gspread.authorize(credentials)

wks = gc.open("PySrs").sheet1
print(len(wks.get_all_values()))
wks.update_cell(2001,1,' try')

# https://github.com/burnash/gspread

def start(debug=False):
	if debug:
		app = mainGui.mApp()
		app.run()
	else:
		app = mainGui.mApp()
		app.run()
		mainGui.makeBackup()

if __name__ == '__main__': start()
