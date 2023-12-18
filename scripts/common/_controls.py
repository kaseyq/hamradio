from ..controllers.rig.rigcontroller import RigController
from ..controllers.rotator.rotatorcontroller import RotatorController
from ..controllers.tone.tonecontroller import ToneController
from ..controllers.tuner.tunercontroller import TunerController
from ..common._logger import Logger

class Controls() :
	_mock = False
	_logger = None
	_rigControl = None
	_tunerControl = None
	_rotatorControl = None
	_toneControl = None


	#def __int__(self, Mock, Logger = None, RigControl = None, TunerControl = None, RotatorControl = None, ToneControl = None) :
	#	self._mock = Mock
	#	self._rigControl = RigControl
	#	self._tunerControl = TunerControl
	#	self._rotatorControl = RotatorControl
#		self._toneControl = ToneControl
#		self._logger = Logger
#		return
	def Mock(self) :
		return _mock

	def Logger(self) :
		if self._logger == None :
			self._logger = Logger()

		return self._logger


	def RigControl(self) :
		if self._rigControl == None :
			self._rigControl = RigController()

		return self._rigControl

	def TunerControl(self) :
		if self._tunerControl == None :
			self._tunerControl = TunerController()

		return self._tunerControl

	def TunerControl(self) :
		if self._tunerControl == None :
			self._tunerControl = TunerController()

		return self._tunerControl


	def RotatorControl(self) :
		if self._rotatorControl == None :
			self._rotatorControl = RotatorController()

		return self._rotatorControl

	def ToneControl(self) :
		if self._toneControl == None :
			self._toneControl = ToneController()

		return self._toneControl