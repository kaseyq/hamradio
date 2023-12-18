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
        self.RotatorControl = self._controls.RotatorControl
        #self.ToneControl = self._controls.ToneControl

        
        return
    
    def _start(self) :
        self.RotatorControl.MoveToDegreesWithMemory(self.Degrees)
        # do stuff
        return

    def _stop(self) :
        # stop doing stuff
        return
    
    
    
