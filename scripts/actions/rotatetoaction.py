import time

from ._scriptaction import ScriptAction


class RotateToAction(ScriptAction) :
    _name = "RotateTo"
    Degrees = 0.0

    def InitAction(self, args = []) :
        self.Degrees = float(args[0])
        
        #print("Degrees = " + )
        #self.RigControl = self._controls.RigControl
        #self.TunerControl = self._controls.TunerControl
        #self.RotatorControl = self._controls.RotatorControl
        #self.ToneControl = self._controls.ToneControl

        
        return
    
    def _start(self) :

        self._important("start = %s"%(str(self._rotator().Degrees())))

        self._rotator().MoveToDegreesWithMemory(self.Degrees)
        while self._rotator()._busy == True :
            self._sleep(0.1)
            self._important("Degrees = %s"%(str(self._rotator().Degrees())))

        self.Stop()
 
        return

    def _stop(self) :
        self._important("Degrees = %s"%(str(self._rotator().Degrees())))


        #self._important("start = %s"%(str(self._rotator().Degrees)))
        # stop doing stuff
        return
    
    
    
