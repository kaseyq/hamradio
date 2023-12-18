import xmlrpc.client

# locals
try:
    from .rigconfig import RigConfig
except ImportError :
    from rigconfig import RigConfig    

from ...common._basecontroller import BaseController



class RigController(BaseController) :
    _name = "Rig Controller"
    _configName = "rig_config"
    _configClass = RigConfig
    _poolSize = 90
    _rpcProxy: object
    _restorePower: int

    #overriden
    def _initialize(self,) :
        self._rpcProxy = xmlrpc.client.ServerProxy(self._c().URL)
        return
   

    def GetPower(self) :
        if self._mock == True :
            self._verbose("Mock self._rpcProxy.rig.get_power()")
            ret = 100
        else:
            ret = self._rpcProxy.rig.get_power()
        return ret
        
    def SetPower(self, power) :
        if self._mock == True :
            self._verbose("Mock self._rpcProxy.rig.set_power()")
        else:
            self._rpcProxy.rig.set_power(power)
        
        return
        
    def GetSWR(self) :
    
        if self._mock == True :
            self._verbose("Mock self._rpcProxy.rig.get_swrmeter()")
            ret = 1
        else :
            ret = self._rpcProxy.rig.get_swrmeter()
        
        return ret
        
    def GetFrequency(self) :
        if self._mock == True :
            self._print("Mock self._rpcProxy.rig.get_vfo()")
            ret = 14
        else :
            ret = self._rpcProxy.rig.get_vfo()
        return ret
                
    def TunePowerOn(self) :
        self._info("Tune Power On")

        self._restorePower = self.GetPower()
            
        self.SetPower(self._c().TunePower)
        return
        
    def TunePowerOff(self) :
        self._info("Tune Power Off")
        self.SetPower(self._restorePower)
        return
    
    def TurnOnPTT(self) :
        self._info("TX ON")
        if self._mock == True :
            self._verbose("Mock self._rpcProxy.rig.set_ptt(1)")
        else :
        #if self._rpcProxy.rig.get_ptt() != 1 :
            self._rpcProxy.rig.set_ptt(1)
        
        self._sleep(0.5)
        return
    
    def TurnOffPTT(self) :
        self._info("TX OFF")
        if self._mock == True :
            self._print("Mock self._rpcProxy.set_ptt(0)")
        else :
            self._rpcProxy.rig.set_ptt(0)
        return

    def SetFrequencyMegahertz(self, frequencyMhz) :

        freq = frequencyMhz * 1000000

        if self._mock == True :
            self._print("Mock self._rpcProxy.rig.set_vfo()" + str(freq))
            ret = 14
        else :
            ret = self._rpcProxy.rig.set_vfo(freq)
        #return ret
        return
    
    def GetFrequencyMegahertz(self) :
        freq = self.GetFrequency()
        ret = float(freq) / 1000000
        
        return ret
        
    def GetFrequencyInMeters(self) :
        ret = 0
        
        frequencyMhz = self.GetFrequencyMegahertz()
        
        #TODO: config file
        if frequencyMhz <= 15 and frequencyMhz > 13 :
            ret = 20
        elif frequencyMhz <= 13 and frequencyMhz > 9 :
            ret = 30
        elif frequencyMhz <= 9 and frequencyMhz > 6 :
            ret = 40
    
        return ret
        
    def MeasureSWROverTime(self, measurements) :
        ret = 100
        rawSWR = 0
        swrCount = 0
        
#        time.sleep(0.5)
        self._sleep(0.5)
                    
        for x in range(measurements) :
            self._sleep(0.1)
#            time.sleep(0.1)
            swr = self.GetSWR()
            
            if True : # TODO: check that SWR is > 0 <= 100?
                rawSWR += swr
                swrCount += 1
            
        if swrCount > 0 :
            ret = int(rawSWR / swrCount)

        return ret

    #overriden
    def Test(self) :
        self.TurnOnPTT()
        #print(self._rpcProxy.rig.get_info())
        return

if __name__ == "__main__" :
    #print("RigController Main")
    rig = RigController(True)
    rig.Test()
