import requests

# locals
try:
    from .tunerconfig import TunerConfig
except ImportError :
    from tunerconfig import TunerConfig

from ...common._basecontroller import BaseController

class TunerController(BaseController) :
    _name = "Tuner Controller"
    _configName = "tuner_config"
    _configClass = TunerConfig
    _poolSize = 90
    _maxAsyncUpdates = 30
    _asyncUpdateStateCount = 0
    _asyncUpdateCurStepCount = 0
    _speed = 0
    _edge = False
    _curStep = 0
    _leftEdge = False
    _rightEdge = False

    # overriden
    def _initialize(self) :

        if self._c().Initialized == False :
            self.UpdateMinStep()
            self.UpdateMaxStep()
        
        self.UpdateCurStep()
        self.UpdateState()
        
        self.SetSpeed(self._c().MinSpeed)
        
        for x in range(self._maxAsyncUpdates) :
            self.AsyncUpdateState()
            self.AsyncUpdateCurStep()
            self._sleep(0.25)
            
        if self._c().Initialized == False :
            self.MeasurePrecision()
            self._c().Initialized = True
                   
        self._busy = False

        return
    
    
    # tuner state requests
    def UpdateState(self) :
        #self._print( "UpdateState - Start", 99)
        #print("MechanicalTuner::UpdateState() : Start")

        # sync
        URL = self._c().URL + "/tuneStatus"
        responseText = ""
        
        if self._mock == True :
            self._info("Mock " + URL)
        else :
            r = requests.get(url = URL)
            responseText = r.text
            
        #self._info("responseText = " + responseText)

        if "Idle" in responseText :
            self._busy = False

        else :
            self._busy = True
            self._info("Busy = True")

        #self._info("_busy = " + str(self._busy))

        if "Edge" in responseText :
            self._edge = True
            
            if self._curStep == self._c().MinStep :
                self._leftEdge = True
                self._rightEdge = False
            else :
                self._leftEdge = False
                self._rightEdge = True
            
        else :
            self._edge = False
            self._leftEdge = False
            self._rightEdge = False

        #self._print( "UpdateState - Done", 99)
        
        return

    def CurrentStep(self) :
        return self._curStep
        
    # speed is 0 to 4000
    def SetSpeed(self, speed) :
        # sync
        
        URL = self._c().URL + "/slider?value=" + str(speed)
        
        if self._mock == True :
            self._print("Mock " + URL)
        else :
            r = requests.get(url = URL)
        
        self._speed = speed
                
        self._info("Speed = %s" %(str(self._speed)))

        return

    def UpdateCurStep(self) :
        # sync
    
        URL = self._c().URL + "/cur-step"
        
        prevStep = self._curStep
                
        if self._mock == True :
            self._print("Mock " + URL)
        else :
            r = requests.get(url = URL)
            self._curStep = int(r.text)
        
        if prevStep != self._curStep :
            self._info("CurStep = %s" %(str(self._curStep)))

        return

    def UpdateMinStep(self) :
        # sync
        URL = self._c().URL + "/min-step"
        
        if self._mock == True :
            self._verbose("Mock " + URL)
        else :
            r = requests.get(url = URL)
            self._c().MinStep = int(r.text)

        self._info("MinStep = " + str(self._c().MinStep))

        return

    def UpdateMaxStep(self) :
        # sync        
        URL = self._c().URL + "/max-step"
        
        
        if self._mock == True :
            self._print("Mock " + URL )
        else :
            r = requests.get(url = self._c().URL + "/max-step")
            self._c().MaxStep = int(r.text)

        self._info("MaxStep = " + str(self._c().MaxStep))
        return
    
    def SetMemory(self, index, name, temp = False) :

        self._info("SetMemory")
        # sync
        self.WaitForIdle()
        
        self._c().SetMemory(index, name, temp)
            
        payload = {"M"+str(index): name}
        headersObj = {"Content-Type": "application/x-www-form-urlencoded"}
        URL = self._c().URL + "/set-memory"
        
        if self._mock == True :
            self._print("Mock " + URL)
        else :
            r = requests.post(url = URL, data = payload, headers = headersObj )

        self._verbose("Set Memory : index = %s, name = %s, step = %s" %(str(index), str(name), str(self._curStep)))
        

        self._configFile.Write()
        
        return
    
    def SetTempMemory(self, tempIndex) :    
        self._info("SetTempMemory")
        self.SetMemory(tempIndex, "temp" + str(tempIndex), True)
        return

    def GetAllTempMemoryIndicies(self) :
        return self._c().GetAllTempMemoryIndicies()
    
    # region: tuner move requests
    def MoveMin(self, direction) :
        self._info("MoveMin() : %s : Start" %(str(direction)))

        self.WaitForIdle()
        
        startStep = self._curStep
        startURL = ""
        stopURL = ""

        if direction > 0 :
            direction = 1
            startURL = self._c().URL + "/rightOn"
            stopURL = self._c().URL + "/rightOff"
            
        else :
            direction = -1
            startURL = self._c().URL + "/leftOn"
            stopURL = self._c().URL + "/leftOff"
            

        self._busy = True

        if self._mock == True :
            self._verbose("Mock self._requestsPool.apply_async(requests.get, [startURL])")
        else :
            self._requestsPool.apply_async(requests.get, [startURL])
        

        while self._curStep == startStep :
            self._sleep(0.000000001)
        
        if self._mock == True :
            self._verbose("Mock  requests.get(url = stopURL)")

        else :
            r = requests.get(url = stopURL)
        
        self.WaitForIdle()

        self._info("MoveMin() : %s : End" %(str(direction)))

        return

    def GetMemoryIndexFromName(self, name) :
        ret = 0
        memEntry = self._c().GetMemoryByName(name)
        if memEntry != None :
            ret = memEntry["Index"]

        return ret

    def TuneFromMemoryName(self, name) :
        memEntry = self._c().GetMemoryByName(name)
        
        if memEntry != None :
            self.TuneFromMemory(memEntry["Index"])
        return
        
    def TuneFromMemory(self, memoryIndex) :
        #sync
        self._print("Tuning to memory %s" %(str(memoryIndex)))

        self.WaitForIdle()
        
        self.SetSpeed(self._c().MaxSpeed)

        dataObj = {"M" + str(memoryIndex): "MemBtn" + str(memoryIndex)}

        headersObj = {"Content-Type": "application/x-www-form-urlencoded"}

        self._busy = True
        URL = self._c().URL + "/from-memory"
    
        if self._mock == True :
            self._verbose("Mock " + URL)
        else :
            r = requests.post(url = URL, data =dataObj, headers = headersObj)
        
        
        self.WaitForIdle()
        self.SetSpeed(self._c().MinSpeed)

        self._info("Tuned to Memory %s" %(str(memoryIndex)))
        
        return

    def HandleAsyncUpdateState(self, result) :
        self._asyncUpdateStateCount = max(self._asyncUpdateStateCount - 1, 0)
        self.RunAsyncState()
        
        return
        
    def AsyncUpdateState(self) :
    
        if self._asyncUpdateStateCount <= self._maxAsyncUpdates :
        
            self._asyncUpdateStateCount += 1
            self._requestsPool.apply_async(self.UpdateState, callback=self.HandleAsyncUpdateState)
        
        return
        
    def HandleAsyncUpdateCurStep(self, result) :
    
        self._asyncUpdateCurStepCount = max(self._asyncUpdateCurStepCount - 1, 0)
        self.RunAsyncCurStep()
        return

    def AsyncUpdateCurStep(self) :
        if self._asyncUpdateCurStepCount <= self._maxAsyncUpdates :
            self._asyncUpdateCurStepCount += 1
            self._requestsPool.apply_async(self.UpdateCurStep, callback=self.HandleAsyncUpdateCurStep)
            
        return
        
    def RunAsyncCurStep(self):
        while self._asyncUpdateCurStepCount <= self._maxAsyncUpdates :
            self.AsyncUpdateCurStep()
            self._sleep(0.1)
    
    def RunAsyncState(self):
        while self._asyncUpdateStateCount <= self._maxAsyncUpdates :
            self.AsyncUpdateState()
            self._sleep(0.1)
    
    def WaitForIdle(self) :
        #self._print("WaitForIdle() : Start", 99)
        self._sleep(self._c().MinWaitDuration)

        
        
        while self._busy == True :
        #for x in range(1000) : #TODO
            self._sleep(self._c().MinWaitDuration)
            #if x > 1 and self._busy == False :
            #    break
        #self._print("WaitForIdle() : End", 99)
        return
        

    def MeasurePrecision(self) :
        print("Measure Precision : Start")
        self.WaitForIdle()
        
        previousStep = self._curStep
        
        testStepCountMax = 10
        testStepCount = 0
        testStepDeltaRaw = 0
        #testStepDeltaAvg = 0
        
        testDirection = -1
        
        # make sure there's enough buffer to avoid the edges
        if self._leftEdge or self._curStep - 200 <= self._c().MinStep :
            self.MoveMin(1)
            self.MoveMin(1)
        elif self._rightEdge or self._curStep + 200 >= self._c().MaxStep :
            self.MoveMin(-1)
            self.MoveMin(-1)
        
        #TODO: Make sure it's not at edge
        for x in range(testStepCountMax) :
            
            if testDirection < 0 :
                testDirection = 1
            else :
                testDirection = -1
        
            print("Measure Precision : %s : Start" %(str(x)))
            self.MoveMin(testDirection)
            self.WaitForIdle()
            
            if self._edge == False :
                delta = abs(self._curStep - previousStep)
                if delta > 0 :
                    print("Precision : %s" %(str(delta)))
                    testStepDeltaRaw += delta
                    testStepCount += 1
            
            print("Measure Precision : %s : End" %(str(x)))
            
        if testStepCount > 0 :
            self._c().Precision = int(( testStepDeltaRaw / testStepCount ) * 0.1)
            print("Precision : %s" %(str(self._c().Precision)))
        
        else :
            print("Precision Measurement Failed")
            
        print("Measure Precision : Stop")

        return


if __name__ == "__main__" :
    Mock = True
    tuner = TunerController(Mock)
    
    
