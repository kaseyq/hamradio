import time
from multiprocessing.dummy import Pool

try:
    from ._configfile import ConfigFile
except ImportError :
    from _configfile import ConfigFile

class BaseController() :
    _configFile: object
    _name: str
    _configName: str
    _configClass: object
    _configFile: object
    _mock: bool
    _busy: bool
    _poolSize = int
    _requestsPool: object
    _c =  object
    _logger = object


    def __init__(self, mock = False, logger = None) :
        self._logger = logger
        self._busy = False
        self._mock = mock
        self._configFile = ConfigFile(self._configClass, self._configName)
        self._requestsPool = Pool(self._poolSize)

        self._initialize()

        self._configFile.Write()
        self._info("Initialized")

        return


    def _initialize(self) :
        # override 
        return

    def _formatFloat(self, value) :
        return float("{:.2f}".format(value))

    def _printDetails(self) :
        # override
        return

    def _c(self) :
        return self._configFile.Config

    def _cv(self, key) :
        return self._configFile.Config[key]

    def _printState(self) :
        if self._busy == True :
            self._info("Busy")
        else :
            self._info("Idle")
        return

    def _print(self, message, loglevel = 10) :
        if self._logger != None :
            self._logger.Log(message, loglevel)
        #if self._logLevel >= loglevel :
        #    print(self._name + " | "+ str(message))
        return

    def _log(self, message, loglevel = 40) :
        if self._logger != None :
            self._logger.Log(message, loglevel)
        return

    def _verbose(self, message) :
        self._print(message, 40)
        return

    def _important(self, message) :
        self._print(message, 1)
        return

    def _info(self, message) :
        self._print(message, 10)
        return

    def _warn(self, message) :
        self._print(message, 2)
        return

    def _error(self, message) :
        self._print(message, 1)
        return

    def _sleep(self, duration) :

        loglevel = 99

        if duration >= 5 :
            loglevel = 1

        self._log("Wait " + str(self._formatFloat(duration)) + " seconds", loglevel)
        time.sleep(duration)

        return

    def Test(self) :
        # override

        return
    