from py_irsend import irsend

# locals
try:
    from .rotatorconfig import RotatorConfig
#    from ....common._basecontroller import BaseController
except ImportError :
    from rotatorconfig import RotatorConfig    
#    from ....common_basecontroller import BaseController

from ...common._basecontroller import BaseController


class RotatorController(BaseController) :
    _name = "Rotator Controller"
    _configName = "rotator_config"
    _configClass = RotatorConfig
    _poolSize = 90

    # overriden
    def _initialize(self) :
        self._initializePosition(False)

        return
    
    def _initializePosition(self, write = True, force = False) :
        if force == True or self._c().PositionInitialized != True :
            self._info("Initializing Position")
            self._busy = True
            self._sendCommandAsync(self._c().InitialPositionCommand)
            self._sleep(self._c().InitPositionDuration)        
            
            self._setDegrees(0)
            self._c().PositionInitialized = True

            self._busy = False

            if write == True :
                self._configFile.Write()

            self._info("Initialized Position")
        return

    # overriden
    def _printDetails(self) :
        self._printDegrees()
        self._printState()
        return

    def _printDegrees(self) :
        self._info("%s degrees" %(self._getDisplayDegrees()))
        return
        
    def _normalizeDirection(self, direction) :
        if direction < 0 :
            direction = -1
        else :
            direction = 1
            
        return direction

    def Degrees(self) :

        return self._getDisplayDegrees()
        
    def _getDisplayDegrees(self) :
        return float("{:.2f}".format(self._getDegrees()))
    
    def _getDegrees(self) :
        return self._configFile.Config.Degrees
       
    def _setDegrees(self, degrees) :
        self._printDegrees()
        priorDegrees = self._c().Degrees

        self._c().Degrees = degrees

        if priorDegrees != degrees :
            self._configFile.Write()
            self._printDegrees()

        return
    
    def _sendCommandAsync(self, cmd) :
        self._requestsPool.apply_async(self._sendCommand, [cmd])
        
        return
        
    def _sendCommand(self, cmd) :
    
        #TODO: check self.Config.ValidCommands
        
        if self._mock == True :
            self._verbose("Mock IR Command: %s %s" %(str(self._c().RemoteName),str(cmd)))
        else :
            irsend.send_once(self._c().RemoteName, [cmd])
        
        return
    
    def _getMemoryEntry(self, memoryId):
        ret = None
        for memoryEntry in self._c().Memories :
            if memoryEntry["Identifier"] == memoryId :
                ret = memoryEntry
                break
        return ret
    
    def _moveToMemory(self, memoryEntry) :
        
        self.WaitForIdle()     
        self._busy = True
        
        if self._getDegrees() == memoryEntry["Degrees"] :
            self._busy = False
            return

        self._sendCommandAsync(memoryEntry["Command"])
        
        self._busy = True

        delta = abs(self._getDegrees() - memoryEntry["Degrees"])

        self._print("Memory Degrees " + str(memoryEntry["Degrees"]))

        self._print("Delta = " + str(delta))

        duration = float(0)

        if abs(delta) > 0 :
           duration = (delta/360) * self._c().MaxMemoryDuration
        
        self._sleep(duration)
        
        self._setDegrees(memoryEntry["Degrees"])
        
        self._busy = False
                
        return

    def _move(self, degreeMove) :
        self._print("Move " + str(self._formatFloat(degreeMove)) + " degrees")

        self._busy = True
            
        direction = self._normalizeDirection(degreeMove)
        
        cmd = None
        
        if direction == -1 :
            cmd = self._c().MoveLeftCommand
        else :
            cmd = self._c().MoveRightCommand
        
        pendingDegrees = self._getDegrees() + degreeMove

        self._sendCommandAsync(cmd)

        self._sleep(self._c().TickDuration)

        self.Busy = False        

        self._setDegrees(pendingDegrees)

        return


    def _findClosestMemoryDegrees(self, degrees) :

        ret = None
        retDelta = 999999
        
        memCount = len(self._c().Memories)


        for i in range(memCount) :
            curMemory = self._c().Memories[i]
            
            curDelta = abs(degrees - curMemory["Degrees"])

            if ret == None or curDelta == 0:
                retDelta = curDelta
                ret = curMemory

                if curDelta == 0 :
                    break

            if curDelta < retDelta :
                retDelta = curDelta
                ret = curMemory

        return ret

    def ResetPosition(self, degrees) :
        self._initializePosition(True, False)

        return

    def MoveToDegreesWithMemory(self, degrees) :
        self._info("start")
        
        delta = degrees - self._getDegrees()

        if abs(delta) > self._c().TicksToDegrees :
            memoryEntry = self._findClosestMemoryDegrees(degrees)
            
            if memoryEntry != None and abs(degrees - memoryEntry["Degrees"]) < abs(delta) :
                self._moveToMemory(memoryEntry)

            delta = degrees - self._getDegrees()

            direction = self._normalizeDirection(delta)

            moveDegrees = direction * self._c().TicksToDegrees

            if abs(delta) >= moveDegrees :

                moves = int((abs(delta) / abs(moveDegrees)) + 0.5)

                for move in range(moves) :
                    self._move(moveDegrees)

            self._configFile.Write()

        self._info("done")

        return


    def WaitForIdle(self) :
        while self._busy == True :
            self._sleep(self._c().TickDuration)
            
        return

        
    def Test(self) :
    
        tickDelay = 1.5
        totalCount = 0
        totalDuration = 0

        maxCount = 465

        while totalCount <= maxCount :
            self._sendCommandAsync(self._c().MoveRightCommand)
            #self._print("wait " + str(tickDelay)+"s")
            self._sleep(tickDelay)
            totalCount += 1
            self._info ("Count " + str(totalCount))
        return

if __name__ == "__main__" :
    rotator = RotatorController()
    rotator.Test()
