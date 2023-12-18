import time

from ._scriptaction import ScriptAction


class FrequencyAction(ScriptAction) :
    _name = "Frequency"
    Degrees = 0.0

    def InitAction(self, args = []) :
        self.Frequency = float(args[0])
        
        #self.RigControl = self._controllers.RigControl
        #self.TunerControl = self._controllers.TunerControl
        #self.RotatorControl = self._controllers.RotatorControl
        #self.ToneControl = self._controllers.ToneControl
        
        return
    
    def _start(self) :
        # do stuff
        self._rig().SetFrequencyMegahertz(self.Frequency)

        return

    def _stop(self) :
        # stop doing stuff
        return


    
    
    
