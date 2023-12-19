import time

from ._scriptaction import ScriptAction


class RotateToAction(ScriptAction) :
    _name = "RotateTo"
    Degrees = 0.0

    def InitAction(self, args = []) :
        self.Degrees = float(args[0])
        return
    
    def _start(self) :

        self._important("Current = %s degrees"%(str(self._rotator().Degrees())))
        self._important("Target = %s degrees"%(str(self.Degrees)))

        self._rotator().MoveToDegreesWithMemory(self.Degrees)
        
        #while self._rotator()._busy == True :
        #    self._sleep(0.1)
        #    self._important("Degrees = %s"%(str(self._rotator().Degrees())))

        self.Stop()
 
        return

    def _stop(self) :
        self._important("Degrees = %s"%(str(self._rotator().Degrees())))


        #self._important("start = %s"%(str(self._rotator().Degrees)))
        # stop doing stuff
        return
    
    
    
