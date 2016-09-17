from datetime import datetime
import atexit

class Debug():
	debugEnabled = True
	logFile = ''

	@staticmethod
	def OpenLogFile():
		if Debug.logFile == '':
			open('log', 'w').close()
			Debug.logFile = open('log', 'a')
			Debug.logFile.write(str('\n -----' + str(datetime.now()) + '-----\n'))
	@staticmethod
	def CloseLogFile():
		if Debug.logFile != '':
			Debug.logFile.close()

	@staticmethod
	def Log(*args):
		Debug.Print(*args)
		if Debug.debugEnabled:
			Debug.OpenLogFile()
			Debug.logFile.write(str(str(datetime.now()) + '  '))
			for arg in args:
				Debug.logFile.write(str(arg))
			Debug.logFile.write('\n')
	@staticmethod
	def Print(*args):
		if Debug.debugEnabled:
			print(str(datetime.now()), ' ', end='')
			for arg in args:
				print(str(arg), end='')
			print()

atexit.register(Debug.CloseLogFile)