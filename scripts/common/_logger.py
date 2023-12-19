from datetime import datetime

class Logger() :
	_level: int
	_mock: bool

	ExceptionLevel = 0
	ErrorLevel = 1
	WarnLevel = 2
	InfoLevel = 3
	DevLevel = 40
	VerboseLevel = 99

	LogLevels = [
	{ "level" : 0, "name": "Exception", "abv": "EX!"},
	{ "level" : 1, "name": "Error", "abv": "ERR"},
	{ "level" : 2, "name": "Warn", "abv": "WRN"},
	{ "level" : 3, "name": "Important", "abv": "WRN"},
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

	def Log(self, message, level) :
		#a = LogLevels[]
		if level <= self._level :
			print(str(datetime.now()) + " | " + self._logLevelAbbreviation(level) + " | " + str(message))
		return

	def Exception(self, message) :
		self.Log(message, self.ExceptionLevel)

	def Error(self, message) :
		self.Log(message, self.ErrorLevel)
		return

	def Warn(self, message) :
		self.Log(message, self.WarnLevel)
		return

	def Info(self, message) :
		self.Log(message, self.InfoLevel)
		return

	def Dev(self, message) :
		self.Log(message, self.DevLevel)
		return