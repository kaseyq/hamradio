from jsons import JsonSerializable

ConfigFileName = "tuner_config"

class TunerConfig(JsonSerializable) :
    URL: str
    MinMoveDuration: float
    MinWaitDuration: float
    MaxSpeed: int
    MinSpeed: int
    Initialized: bool
    Precision: int
    LogLevel: int
    MinStep: int
    MaxStep: int
    MemoryEntries :[] 
    MaxMemoryEntryCount: int
    MaxTempMemories: int

    def __init__(self) :
        self.URL = "http://10.0.0.64"
        self.MinMoveDuration = 0.5
        self.MinWaitDuration = 0.5
        self.MaxSpeed = 4000
        self.MinSpeed = 0
        self.Initialized = False
        self.Precision = 20
        self.LogLevel = 99
        self.MinStep = 0
        self.MaxStep = 1
        self.MemoryEntries = []
        self.MaxMemoryEntryCount = 10
        self.MaxTempMemories = 3

        #self.Memory = TunerMemory()
        self.MemoryEntries.append({"Index":0, "Name":"20m", "Temp":False})
        self.MemoryEntries.append({"Index":1, "Name":"30m", "Temp":False})
        self.MemoryEntries.append({"Index":2, "Name":"40m", "Temp":False})
        self.MemoryEntries.append({"Index":3, "Name":"?", "Temp":False})
        self.MemoryEntries.append({"Index":4, "Name":"?", "Temp":False})
        self.MemoryEntries.append({"Index":5, "Name":"?", "Temp":False})
        self.MemoryEntries.append({"Index":6, "Name":"?", "Temp":False})
        self.MemoryEntries.append({"Index":7, "Name":"TEMP0", "Temp":True})
        self.MemoryEntries.append({"Index":8, "Name":"TEMP1", "Temp":True})
        self.MemoryEntries.append({"Index":9, "Name":"TEMP2", "Temp":True})
        return

    def GetMemoryByName(self, name):
        ret = None
        
        for i in range(self.MaxMemoryEntryCount) :
            if self.MemoryEntries[i] != None and name == self.MemoryEntries[i]["Name"]:
                ret = self.MemoryEntries[i]
                break
                
        return ret
    
    def GetMemoryByIndex(self, index) :
        ret = None
        for i in range(self.MaxMemoryEntryCount) :
            if self.MemoryEntries[i] != None and index == self.MemoryEntries[i]["Index"] :
                ret = self.MemoryEntries[i]
                break

        return ret

    def SetMemory(self, index, name) :
        self.SetMemoryEntry({"Index" : index, "Name" :name})
        return
        
    def SetMemoryEntry(self, entry) :
        self.MemoryEntries[entry["Index"]] = entry
        return

    def GetAllTempMemoryIndicies(self) :
        ret = []
        for entry in self.MemoryEntries :
            if "Temp" in entry and entry["Temp"] == True :
                ret.append(entry["Index"])

        return ret
    
        