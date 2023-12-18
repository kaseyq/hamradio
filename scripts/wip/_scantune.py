#!/usr/bin/env python
import time

from rigcontroller import RigController
from tunercontroller import TunerController
from rotatorcontroller import RotatorController
from emittone import EmitTone

class ScanTune() :
    def __init__(self, Mock = False, RigControl = None, TunerControl = None, RotatorControl = None, ToneEmitter = None ) :
        self.Mock = Mock
        
        self.RigControl = RigControl
        self.TunerControl = TunerControl
        self.RotatorControl = RotatorControl
        self.ToneEmitter = ToneEmitter
        
        self.MinSWR = 6
        self.MeasurementCount = 10
        
        
        if self.RigControl  == None :
            self.RigControl = RigController(Mock)
        
        if self.TunerControl  == None :
            self.TunerControl = TunerController(Mock)
        
        if self.RotatorControl == None :
            self.RotatorControl = RotatorController(Mock)
            
        if self.ToneEmitter == None :
            self.ToneEmitter = EmitTone(Mock)
        return
    
    def MeasureSWR(self) :
        return self.RigControl.MeasureSWROverTime(self.MeasurementCount)
       
        
    
        
    def StartTune(self) :
        self.RigControl.TunePowerOn()
        self.RigControl.TurnOnPTT()
        self.ToneEmitter.StartTone()
        time.sleep(1)
        return
        
    def EndTune(self) :
        self.RigControl.TurnOffPTT()
        self.RigControl.TunePowerOff()
        self.ToneEmitter.StopTone()
        
        return
        
    def Tune(self) :
        print("Tune : Start")

        self.StartTune()
        
    
        
        self.EndTune()
        
        
        print("Tune : Complete")
        
        return
        
    def Test(self) :
        #print(self.RigControl.Test())

        return
        
if __name__ == "__main__" :
    print("Scan Tune Main")
    Mock = True
    scanTune = ScanTune(Mock)
    scanTune.Tune()
    
