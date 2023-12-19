#!/usr/bin/env python
import time

from ..common._controls import Controls


class ScriptAction() :
    _running: bool
    _name: str
    _controls: object
    _running: bool
    _args: []
    _logLevel: int

    def __init__(self, controls, args = [], autorun = True) :
        self._logLevel = 40
        self._running = False
        self._controls = controls
        #self.IsRunning = False
        self._args = args

        self._info(self._args)


        self.InitAction(self._args)

        if autorun == True :
            self.Start()

    def InitAction(self) :
        #override
        return

    def IsRunning(self) :
        return _running

    def Start(self) :
        self._info("Start")
        ret = False

        if self._running == False :
            self._running = True
            self._start()
            ret = True
            
            
        return ret

    def Stop(self) :
        self._print("Stop")
        ret = False
        if self._running == True :
            self._running = False
            self._stop()
            ret = True
            
        return ret

    def _start(self) :
        
        #override in sub class

        return

    def _stop(self) :

        #override in sub class

        return

    def _print(self, message, loglevel = 10) :
        self._logger().Log(message, loglevel)

        #if self._logLevel >= loglevel :
        #    print(self._name + " | "+ str(message))
        return

    def _verbose(self, message) :
        self._logger().Verbose(message)
        return

    def _important(self, message) :
        self._logger().Important(message)
        return

    def _info(self, message) :
        self._logger().Info(message)
        return

    def _warn(self, message) :
        self._logger().Warn(message)
        return

    def _error(self, message) :
        self._logger().Error(message)
        return

    def _sleep(self, duration) :

        loglevel = self._logger().VerboseLevel

        if duration >= 3 :
            loglevel = self._logger().ImportantLevel

        self._logger().Log("Wait " + str(duration) + " seconds", loglevel)

        time.sleep(duration)

        return


    def _logger(self) :
        return self._controls.Logger()

    def _rig(self) :
        return self._controls.RigControl()

    def _rotator(self) :
        return self._controls.RotatorControl()

    def _tuner(self) :
        return self._controls.TunerControl()

    def _tone(self) :
        return self._controls.ToneControl()

        
if __name__ == "__main__" :
    print("Script Action Main")
    Mock = True
    _controls = Controls(Mock, RigController(Mock), TunerController(Mock), RotatorControl(Mock), ToneController(Mock))
    action = ScriptAction(_controls)
    

