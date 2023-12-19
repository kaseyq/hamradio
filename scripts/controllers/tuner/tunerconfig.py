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
        self.MaxMemoryEntryCount = 10
        self.MaxTempMemories = 3

        self.MemoryEntries = [{"Index":0, "Name":"20m", "Temp":False},
        {"Index":1, "Name":"30m", "Temp":False},
        {"Index":2, "Name":"40m", "Temp":False},
        {"Index":3, "Name":"?", "Temp":False},
        {"Index":4, "Name":"?", "Temp":False},
        {"Index":5, "Name":"?", "Temp":False},
        {"Index":6, "Name":"?", "Temp":False},
        {"Index":7, "Name":"TEMP0", "Temp":True},
        {"Index":8, "Name":"TEMP1", "Temp":True},
        {"Index":9, "Name":"TEMP2", "Temp":True}]
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

    def SetMemory(self, index, name, temp) :
        self.SetMemoryEntry({"Index" : index, "Name" :name, "Temp": temp})
        return
        
    def SetMemoryEntry(self, entry) :
        self.MemoryEntries[entry["Index"]] = entry
        return

    def GetAllTempMemoryIndicies(self) :
        ret = []

        #print("self.MemoryEntries len = " + str(len( self.MemoryEntries )))
        for entry in self.MemoryEntries :
            #print(entry)
            if "Temp" in entry and entry["Temp"] == True :
                ret.append(entry["Index"])

        return ret
    
        