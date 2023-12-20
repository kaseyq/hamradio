import time

from ._scriptaction import ScriptAction


class WSPRTransmit(ScriptAction) :
   _name = "WSPRTransmit"

   def InitAction(self, args = []) :
        

        #self.Frequency = float(args[0])
        return
    
   def _start(self) :
       
     # self._sleep(120-self.TimeWindow())


      # do stuff
      self._important("WSPRTransmit on " + str(self._rig().GetFrequencyMegahertz()))

      self._controls.WSPRControl().Transmit()
         #self._rig().SetFrequencyMegahertz(self.Frequency)
#        self._important("Frequency is : " + str(self._rig().GetFrequencyMegahertz()))


      self.Stop()

      return

   def _stop(self) :
      # stop doing stuff
      return

   def TimeWindow(self):
      return (time.time() % 120)


     