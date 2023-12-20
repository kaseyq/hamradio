
import time

from ._scriptaction import ScriptAction

class TuneEntry() :
    def __init__(self, MemoryIndex, SWR, Step ) :
        self.MemoryIndex = MemoryIndex
        self.SWR = SWR
        self.Step = Step
    def FormatForDisplay(self) :
        return "SWR = %s at %s step" %(str(self.SWR), str(self.Step))


class TuneAction(ScriptAction) :
    _name = "Tune"

    def InitAction(self, args = []) :
        self._verbose("InitAction")

        #TODO: config values
        self.MaxTuneSteps = 10
        self.MinFineTuneSWR = 0
        self.MinMemoryBypassSWR = 6
        self.SWRMeasurementCount = 10
        self._tempMemoryIndicies = []

        #self.TempMemoryIndicies = [7,8,9]



        return
    
    def _start(self) :
        self._verbose("_start")

        self._rig().TunePowerOn()
        self._rig().TurnOnPTT()
        self._tone().StartTone()
        self._sleep(1)

        #self.StartTune()
        self.Tune()

        while self._running == True :
            self._sleep(0.1)

        self._stop()

        return

    def _stop(self) :
        self._verbose("_stop")
        #self._running = False

        self._rig().TurnOffPTT()
        self._rig().TunePowerOff()
        self._tone().StopTone()

        return

    def MeasureSWR(self) :
        self._verbose("MeasureSWR")
        return self._rig().MeasureSWROverTime(self.SWRMeasurementCount)
        

    def TempMemoryIndicies(self) :
        if len(self._tempMemoryIndicies) == 0 :
            self._tempMemoryIndicies = self._tuner().GetAllTempMemoryIndicies()

        return self._tempMemoryIndicies

    def AddTuneEntry(self, tuneResults) :
        self._verbose("AddTuneEntry - Start")

        resultIndex = len(tuneResults)

        #print("resultIndex = " + str(resultIndex))
        #print("len(self.TempMemoryIndicies()) = " + str(len(self.TempMemoryIndicies())))
        memoryIndex = self.TempMemoryIndicies()[resultIndex]

        self._tuner().SetTempMemory(memoryIndex)

        tuneResults.append(TuneEntry(memoryIndex, self.MeasureSWR(), self._tuner().CurrentStep()))

        self._important(tuneResults[len(tuneResults) - 1].FormatForDisplay())

        self._verbose("AddTuneEntry - Done")
        return tuneResults
        
    def Move(self, direction, steps) :
        self._verbose("Move - Start")

        for step in range(steps) :
            self._tuner().MoveMin(direction)
            self._tuner().WaitForIdle()

        self._verbose("Move - Done")
        return
        
    def TuneFromEntry(self, entry) :
        self._verbose("TuneFromEntry")
        self._tuner().TuneFromMemory(entry.MemoryIndex)
        self._tuner().WaitForIdle()
        return
        
    def StepTune(self, steps, bias = 0) :
        self._verbose("StepTune - Start")
        #print("Step Tune : Start : %s Steps" %(str(steps)))
    

        # if bias == 0, nothing
        # bias >= 1, move more right
        # bias <= 1, move more left

        minDir = -1
        minDirSteps = steps

        maxDir = 1
        maxDirSteps = steps

        if bias > 0 :
            minDir = 1
            minDirSteps = steps
            maxDir = 1
            maxDirSteps = steps * 2
        elif bias < 0 :
            maxDir = -1
            maxDirSteps = steps
            minDir = -1
            minDirSteps = steps * 2

        ret = None
        
        tuneResults = []
        
        self._tuner().WaitForIdle()

        # starting info
        tuneResults = self.AddTuneEntry(tuneResults)
 
        # minimum direction aka left
        self.Move(minDir, minDirSteps)
        tuneResults = self.AddTuneEntry(tuneResults)
        
        # reset to start
        self.TuneFromEntry(tuneResults[0])
        
        # maximum direction aka right
        self.Move(maxDir, maxDirSteps)
        tuneResults = self.AddTuneEntry(tuneResults)
                
        for i in range(len(tuneResults)) :
            self._info("%s = %s" %(str(i), str(tuneResults[i].FormatForDisplay())))
            
            if ret == None or tuneResults[i].SWR < ret.SWR :
                ret = tuneResults[i]
        
        if ret != None :
            self._tuner().TuneFromMemory(ret.MemoryIndex)
            self._tuner().WaitForIdle()

        self._verbose("StepTune - Done")
        return ret

    def FineTune(self) :
        self._info("FineTune - Start")
        ret = None
        prev = None
        
        iterations = max(int(self.MeasureSWR() * 0.5), 1)


        steps = 1
        bias = 0
        
        for iteration in range(iterations) :
            prev = ret
            ret = self.StepTune(steps, bias)
            
            if ret != None :
                if ret.SWR <= self.MinFineTuneSWR :
                    break
                elif prev != None :
                    if prev.Step == ret.Step :
                        steps = min(steps + 1, self.MaxTuneSteps)
                    else:
                        steps = 1
                        #steps = max(steps - 1, 1)
                else :
                    steps = max(steps - 1, 1)                
            else :
                steps = steps + 1
                           
            steps = min(steps, self.MaxTuneSteps)
        
            if ret != None and prev != None :
                bias = ret.Step - prev.Step # to avoid checking the same steps
            else :
                bias = 0

            if steps <= 0 :
                break

        self._info("FineTune - Done")
        return
        
    def Tune(self) :
        self._info("Tune - Start")

        startEntry = TuneEntry(7, self.MeasureSWR(), self._tuner().CurrentStep())

        self._important(startEntry.FormatForDisplay())

        #TODO: check memory entries for current freq in meters
        #TODO: move meter conversion to config and pass khz to tuner, let it decide which memory
        
        bypassMemorySWR = 1

        if startEntry.SWR > bypassMemorySWR :
            self._info("Memory Tune - Start")

            meters = self._rig().GetFrequencyInMeters()

            memIndex = self._tuner().GetMemoryIndexFromName(str(meters) + "m")
            self._tuner().TuneFromMemory(memIndex)

            self._info("Memory Tune - tune to memory " + str(memIndex))
            memoryEntry = TuneEntry(memIndex, self.MeasureSWR(), self._tuner().CurrentStep())
            
            self._info("Memory Tune - start SWR = " + str(startEntry.SWR))
            self._info("Memory Tune - memory " + str(memIndex) + " SWR " + str(memoryEntry.SWR))

# This wasn't working
#            if startEntry.SWR < memoryEntry.SWR :
#                self._tuner().TuneFromMemory(startEntry.MemoryIndex)

            self._info("Memory Tune - Done")
        else :
            self._info("Skipping Memory Tune - SWR is " + str(startEntry.SWR))
        


        if startEntry.SWR >= self.MinFineTuneSWR :
            self.FineTune()
        
        self._running = False



        finishedEntry = TuneEntry(-1, self.MeasureSWR(), self._tuner().CurrentStep())

        step = self._tuner().CurrentStep()
        swr = self.MeasureSWR()

        self._important("start = %s"%(startEntry.FormatForDisplay()))
        self._important("done  = %s"%(finishedEntry.FormatForDisplay()))
       # print("SWR = %s at %s step" %())
       # print("Step %s")
        
        self._info("Tune - Done")
        
        return
        
    
    
    
