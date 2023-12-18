import time

from .rigcontroller import RigController
from .tunercontroller import TunerController
from .rotatorcontroller import RotatorController
from .tonecontroller import ToneController
#from hardware.tunercontroller import TunerController
#from hardware.rotatorcontroller import RotatorController
#from hardware.emittone import EmitTone

class TuneEntry() :
    #TODO:
    def __init__(self, MemoryIndex, SWR, Step ) :
        self.MemoryIndex = MemoryIndex
        self.SWR = SWR
        self.Step = Step

class AutoTune() :

    #TODO:
    def __init__(self, Mock = False, RigControl = None, TunerControl = None, RotatorControl = None, ToneControl = None ) :
        self.Mock = Mock
        
        self.RigControl = RigControl
        self.TunerControl = TunerControl
        self.RotatorControl = RotatorControl
        self.ToneControl = ToneControl
        self.MinSWR = 6
        self.MaxSteps = 10
        self.MeasurementCount = 10
        self.TempMemoryIndex = 7

        if self.RigControl  == None :
            self.RigControl = RigController(Mock)
        
        if self.TunerControl  == None :
            self.TunerControl = TunerController(Mock)
        
        if self.RotatorControl == None :
            self.RotatorControl = RotatorController(Mock)
            
        if self.ToneControl == None :
            self.ToneControl = ToneController(Mock)
        return
    
    def MeasureSWR(self) :
        return self.RigControl.MeasureSWROverTime(self.MeasurementCount)
        
    def AddTuneEntry(self, tuneResults) :
        memoryIndex = self.TempMemoryIndex + len(tuneResults)
        self.TunerControl.SetTempMemory(memoryIndex)
        tuneResults.append(TuneEntry(memoryIndex, self.MeasureSWR(), self.TunerControl.CurrentStep()))
        return tuneResults
        
    def Move(self, direction, steps) :
        for step in range(steps) :
            self.TunerControl.MoveMin(direction)
            self.TunerControl.WaitForIdle()
        return
        
    def TuneFromEntry(self, entry) :
        self.TunerControl.TuneFromMemory(entry.MemoryIndex)
        self.TunerControl.WaitForIdle()
        return
        
    def StepTune(self, steps) :
        #print("Step Tune : Start : %s Steps" %(str(steps)))
    
        ret = None
        
        tuneResults = []
        
        self.TunerControl.WaitForIdle()

        # starting info
        tuneResults = self.AddTuneEntry(tuneResults)
 
        # left info
        self.Move(-1, steps)
        tuneResults = self.AddTuneEntry(tuneResults)
        
        # reset to start
        self.TuneFromEntry(tuneResults[0])
        
        #right info
        self.Move(1, steps)
        tuneResults = self.AddTuneEntry(tuneResults)
        
        #bestEntry = None
        
        for i in range(len(tuneResults)) :
            print("%s SWR = %s" %(str(i), str(tuneResults[i].SWR)))
            
            if ret == None or tuneResults[i].SWR < ret.SWR :
                ret = tuneResults[i]
        
        if ret != None :
            self.TunerControl.TuneFromMemory(ret.MemoryIndex)
            self.TunerControl.WaitForIdle()

        return ret

    def FineTune(self) :
        ret = None
        prev = None

#        startPos = self.TunerControl.CurrentStep()
#        startSWR = self.RigControl.GetSWR()
        

        iterations = int(self.RigControl.GetSWR() * 0.5)
        #maxSteps = 5
        steps = 1
        
        for iteration in range(iterations) :
            prev = ret
            ret = self.StepTune(steps)
            
            if ret != None :
                if ret.SWR < self.MinSWR :
                    break
                elif prev != None :
                    if prev.Step == ret.Step :
                        steps = min(steps + 1, self.MaxSteps)
                    else:
                        steps = max(steps - 1, 1)
                else :
                    steps = max(steps - 1, 1)
            else :
                steps = steps + 1
                           
            steps = min(steps, self.MaxSteps)
        
            if steps <= 0 :
                break

        return
        
    def StartTune(self) :
        self.RigControl.TunePowerOn()
        self.RigControl.TurnOnPTT()
        self.ToneControl.StartTone()
        time.sleep(1)
        return
        
    def EndTune(self) :
        self.RigControl.TurnOffPTT()
        self.RigControl.TunePowerOff()
        self.ToneControl.StopTone()
        
        return
        
    def Tune(self) :
        print("Tune : Start")

        self.StartTune()
        
        
        print("SWR: %s" %(str(self.RigControl.GetSWR())))

        startEntry = TuneEntry(7, self.RigControl.GetSWR(), self.TunerControl.CurrentStep())

        # TODO: generate audio tone for PTT
        
        
        #TODO: check memory entries for current freq in meters
        #TODO: move meter conversion to config and pass khz to tuner, let it decide which memory
        
        
        
        
        bypassMemorySWR = 20

        
        if self.RigControl.GetSWR() > bypassMemorySWR :
        
            meters = self.RigControl.GetFrequencyInMeters()
            memIndex = self.TunerControl.GetMemoryIndexFromName(str(meters) + "m")
            self.TunerControl.TuneFromMemory(memIndex)
            memoryEntry = TuneEntry(memIndex, self.RigControl.GetSWR(), self.TunerControl.CurrentStep())
            
            if startEntry.SWR < memoryEntry.SWR :
                self.TunerControl.TuneFromMemory(startEntry.MemoryIndex)
        
        
        self.FineTune()
        
        #TODO: turn on rig tuning
        #TODO: Rig Tune
        #TODO: fine tune again
    
        
        
        self.EndTune()
        
        
        print("Tune : Complete")
        
        return
        
    def Test(self) :
        print(self.RigControl.Test())

        return
        
if __name__ == "__main__" :
    Mock = True

    #RigControl = RigController(Mock)
    #TunerControl = TunerController(Mock)
    #RotatorControl = RotatorController(Mock)
    #Tone = ToneEmitter(Mock)

#    def _Mock = False, RigControl = None, TunerControl = None, RotatorControl = None, ToneEmitter = None ) :
    print("AutoTune Main")

    AutoTune(
    Mock,
    RigController(Mock),
    TunerController(Mock),
    RotatorController(Mock),
    ToneController(Mock)
    ).Tune()

    
    
    
