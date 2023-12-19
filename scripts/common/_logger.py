from datetime import datetime
import os.path
from pathlib import Path

class Logger() :
	_level: int
	_mock: bool

	ExceptionLevel = 0
	ErrorLevel = 1
	WarnLevel = 2
	ImportantLevel = 3
	InfoLevel = 40
	DevLevel = 50
	VerboseLevel = 99

	LogLevels = [
	{ "level" : 0, "name": "Exception", "abv": "EX!"},
	{ "level" : 1, "name": "Error", "abv": "ERR"},
	{ "level" : 2, "name": "Warn", "abv": "WRN"},
	{ "level" : 3, "name": "Important", "abv": "IMP"},
	{ "level" : 40, "name": "Info", "abv": "INF"},
	{ "level" : 50, "name": "Dev", "abv": "DEV"},
	{ "level" : 99, "name": "Verbose", "abv": "VRB"}]

	def __init__(self, Mock = False, logLevel = 40) :
		self._level = logLevel
		return

	def _logLevelAbbreviation(self, level) :
		ret = "log %s" %(str(level))

		count = len(self.LogLevels)
		index = count 
		while index >= 0 :
			index -= 1
			if level <= self.LogLevels[index]["level"] :
				ret = self.LogLevels[index]["abv"]
			else :
				break

		return ret

	def SetLogLevel(self, level) :

		self.Log
		_level = level


		return

	def Log(self, message, level) :
		
		formattedLogEntry = str(datetime.now()) + " | " + self._logLevelAbbreviation(level) + " | " + str(message)

		if level <= self._level :
			print(formattedLogEntry)

		self._appendLogEntry(formattedLogEntry)

		return

	def Exception(self, message) :
		self.Log(message, self.ExceptionLevel)

	def Error(self, message) :
		self.Log(message, self.ErrorLevel)
		return

	def Warn(self, message) :
		self.Log(message, self.WarnLevel)
		return

	def Important(self, message) :
		self.Log(message, self.ImportantLevel)
		return

	def Info(self, message) :
		self.Log(message, self.InfoLevel)
		return

	def Dev(self, message) :
		self.Log(message, self.DevLevel)
		return

	def Verbose(self, message) :
		self.Log(message, self.VerboseLevel)
		return

	def _appendLogEntry(self, entry) :
		self._writeLogEntry("\n" + str(entry))

	def _getFilePath(self) : 
		fileName = "hamradio.log"

		curPath = os.path.realpath(__file__)
		curDir = os.path.dirname(curPath)

		filepath = os.path.join(curDir, os.path.pardir, os.path.pardir)

		return os.path.join(filepath, fileName)

	def _writeLogEntry(self, logs) :        
		fileHandle = open(self._getFilePath(), "a")
		fileHandle.write(logs)
		fileHandle.close()