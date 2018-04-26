import helpLibs.consts as consts
import helpLibs.mainGui as mainGui

def start(debug = False):
	if debug:
		app = mainGui.mApp()
		app.run()
	else:
		app = mainGui.mApp()
		app.run()
		mainGui.makeBackup()

if __name__ == '__main__': start()