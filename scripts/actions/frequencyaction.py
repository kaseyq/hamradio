import time

from ._scriptaction import ScriptAction


class FrequencyAction(ScriptAction) :
    _name = "Frequency"
    Degrees = 0.0

    def InitAction(self, args = []) :
        self.Frequency = float(args[0])
        return
    
    def _start(self) :
        # do stuff
        self._important("Frequency is : " + str(self._rig().GetFrequencyMegahertz()))

        self._rig().SetFrequencyMegahertz(self.Frequency)
        self._important("Frequency is : " + str(self._rig().GetFrequencyMegahertz()))


        self.Stop()

        return

    def _stop(self) :
        # stop doing stuff
        return

