import os.path
from pathlib import Path
import jsons

class ConfigFile() :
    Name: str
    Ext: str
    Dir: str
    Config: object
    Clazz: object

    def __init__(self, Clazz, Name, Ext = ".config.json", Dir = "configs") :
        self.Clazz = Clazz
        self.Name = Name
        self.Ext = Ext
        self.Dir = Dir
        self.Config = None
        self.Read()

    def GetFilePath(self):
        
        fileName = self.Name + self.Ext
        
        curPath = os.path.realpath(__file__)
        curDir = os.path.dirname(curPath)
        
        rootPath = os.path.join(curDir, os.path.pardir, os.path.pardir)

        configDirectoryPath = os.path.join(rootPath, self.Dir)
        return os.path.join(configDirectoryPath, fileName)
                
        
    def Write(self) :

        #if config != None :
        #    self.Config = config

        configFilePath = self.GetFilePath()

        #print("configfile.Write " + configFilePath)
        
        jsonData = jsons.dumps(self.Config)
        #print(jsonData)
        
        Path(os.path.dirname(configFilePath)).mkdir(parents=True, exist_ok=True)
        
        fileHandle = open(configFilePath, "w+")
        fileHandle.write(jsonData)
        fileHandle.close()
        
        return    


    def Read(self) :
        configFilePath = self.GetFilePath()
        
        #print("configfile.Read " + configFilePath )

        if os.path.isfile(configFilePath) == True :
            fileHandle = open(configFilePath, "r")
            fileData = fileHandle.read()
            fileHandle.close()
            self.Config = jsons.loads(fileData, self.Clazz)

        if self.Config == None :
            self.Config = self.Clazz()

        return
