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
	{ "level" : 3, "name": "Info", "abv": "INF"},
	{ "level" : 40, "name": "Dev", "abv": "DEV"},
	{ "level" : 99, "name": "Verbose", "abv": "VRB"}]

	def __init__(self, Mock = False, logLevel = 40) :
		self._level = logLevel
		return

	def _logLevelAbbreviation(self, level) :
		ret = "Log"
		for x in range(len(self.LogLevels)) :
			if level <= self.LogLevels[x]["level"] :
				ret = self.LogLevels[x]["abv"]
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