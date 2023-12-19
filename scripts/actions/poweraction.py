import time

from ._scriptaction import ScriptAction


class PowerAction(ScriptAction) :
    _name = "Power"
    Degrees = 0.0

    def InitAction(self, args = []) :
        self.Power = float(args[0])
        return
    
    def _start(self) :
        # do stuff
        self._important("Power is : " + str(self._rig().GetPower()))

        self._rig().SetPower(self.Power)
        self._important("Power is : " + str(self._rig().GetPower()))

        self.Stop()

        return

    def _stop(self) :
        # stop doing stuff
        return

