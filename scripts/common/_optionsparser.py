class ParsedOption() :
	Name = None
	Arguments = []

class RegisteredOption():
	Name = None
	Callback = None
	CallFirst = False

class OptionsParser() :
	_logger: object
	_registeredOptions = dict()

	_optionSeperators = ["-"]

	def __init__(self, logger) :
		self._logger = logger
		#self._registeredOptions = {}

	def RegisterOption(self, name, callback, callFirst = False) :
		#if name in self._registeredOptions == False :

		option = RegisteredOption()
		option.Name = name
		option.Callback = callback
		option.CallFirst = callFirst

		self._registeredOptions[name] = option
		return

	def ParseAndExecute(self, opts) :

		parsedOptions = self.Parse(opts)
		self._executeRegisteredOptions(parsedOptions)


	def Parse(self, opts) :
		parsedOptions = []

		for index in range(len(opts)) :

			option = opts[index]

			if self._isOption(option) == True :
				self._logger.Info( "Parse Option %s = %s" %(str(index), option))
				entry = ParsedOption()
				entry.Name = option[1:len(option)]
				entry.Arguments = self._parseArgs(index, opts)

				self._logger.Info( "name = %s, args = %s" %(str(entry.Name), str(entry.Arguments)))

				parsedOptions.append(entry)
				#logger.Info( "Parse Option %s = %s" %(str(index), option))
#			else :
#				#ignore

		return parsedOptions

	def _parseArgs(self, index, opts) :
		ret = []
		index += 1 #start with the next value

		while index < len(opts) :
			arg = opts[index]

			#only grab values until next option
			if self._isOption(arg) == False :
				self._logger.Info( "Parse Arguments %s = %s" %(str(index), arg))

				ret.append(arg)
			else :
				break

			index += 1

		return ret

	def _isOption(self, value) :
		ret = False
		for sep in self._optionSeperators :
			if value.startswith(sep) : 
				ret = True
				break

		return ret

	def _executeRegisteredOptions(self, parsedOptions) :

		self._executeOptions(parsedOptions, True)
		self._executeOptions(parsedOptions, False)

		return


	def _executeOptions(self, parsedOptions, callFirst) :

		self._logger.Info(self._registeredOptions)
		for parsedOption in parsedOptions :

			if parsedOption.Name in self._registeredOptions and self._registeredOptions[parsedOption.Name].CallFirst == callFirst :
				self._logger.Info("calling option %s callback with %s" %(parsedOption.Name, str(parsedOption.Arguments)))
				self._registeredOptions[parsedOption.Name].Callback(parsedOption.Arguments)

		return
