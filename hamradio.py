import sys

from scripts.common._controls import Controls
from scripts.actions.tuneaction import TuneAction
from scripts.actions.rotatetoaction import RotateToAction
from scripts.actions.frequencyaction import FrequencyAction
from scripts.actions.poweraction import PowerAction

from scripts.controllers.rig.rigcontroller import RigController
from scripts.controllers.rotator.rotatorcontroller import RotatorController
from scripts.controllers.tone.tonecontroller import ToneController
from scripts.controllers.tuner.tunercontroller import TunerController
from scripts.common._logger import Logger
from scripts.common._optionsparser import OptionsParser


class HamRadio() :
	_logger: object
	_optionsParser: object
	_controls: object
	_actionMap = {
		"Tune" : TuneAction,
		"RotateTo" : RotateToAction,
		"Frequency" : FrequencyAction,
		"Power" : PowerAction
	}

	def __init__(self, logger = None) :

		if logger == None:
			self._logger = Logger()


		self._optionsParser = OptionsParser(self._logger)
		self._controls = Controls()
		self._controls._logger = self._logger
		self._controls._mock =  False


		self._optionsParser.RegisterOption("a", self.ActionHandler)
		self._optionsParser.RegisterOption("v", self.VerboseHandler, True)
		self._optionsParser.RegisterOption("m", self.MockHandler, True)

		return

	def RunFromArgs(self, args):
		self._optionsParser.ParseAndExecute(args)
		return


	def VerboseHandler(self, arguments) :
		self._controls._logger.LogLevel = self._controls._logger.VerboseLevel
		return

	def MockHandler(self, arguments) :
		self._controls._mock = True
		return

	def ActionHandler(self, arguments) :
		name = arguments[0]
		args = []

		if len(arguments) >= 1 :
			args = arguments[1:len(arguments)]

		ScriptAction = self._actionMap[name]

		if ScriptAction != None :
			ScriptAction(self._controls, args, True)

		return
 
if __name__ == "__main__":
	main(sys.argv)