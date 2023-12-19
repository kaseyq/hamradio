from jsons import JsonSerializable

ConfigFileName = "rotator_config"


#class RotatorMemoryEntry(JsonSerializable):
#    Identifier: str
#    Command: str
#    Degrees: float
#    TickMove: float
#    
#    def __init__(self, Identifier, Command, Degrees, TickMove = 0.77 ) :
#        self.Identifier = Identifier
#        self.Command = Command
#        self.Degrees = Degrees
#        self.TickMove = TickMove#
#
#        return
    

class RotatorConfig(JsonSerializable):

    MinTicks: int
    MaxTicks: int
    TicksToDegrees: float
    MinTick: int
    TickDuration: float
    InitPositionDuration: float
    ValidCommands: []
    RemoteName: str
    MoveLeftCommand: str
    MoveRightCommand: str
    InitialPositionCommand: str
    Memories: []
    #Ticks: int
    Degrees: float
    PositionInitialized: bool

    DegreesPerTicks: []
    

    def __init__(self) :
        
        self.MinTicks = 0
        self.MaxTicks = 474

        self.TicksToDegrees = 0.759301442672741

        self.MinTick = 1
        self.TickDuration = 1.0
        self.MaxMemoryDuration = 60
        self.InitPositionDuration = 60
        
        self.ValidCommands = [
            "left",
            "right",
            "prog_memory",
            "initial",
            "memory_a",
            "memory_b",
            "memory_c",
            "memory_d",
            "memory_e",
            "memory_f",
            "memory_g",
            "memory_h",
            "memory_i",
            "memory_j",
            "memory_u",
            "memory_l"
        ]
        
        self.RemoteName = "rca_rotator"
        self.MoveLeftCommand = "left"
        self.MoveRightCommand = "right"
        
        self.InitialPositionCommand = "initial"
        
        self.Memories = [
            {"Identifier": "a", "Command": "memory_a", "Degrees": 0},
            {"Identifier": "b", "Command": "memory_b", "Degrees": 20},
            {"Identifier": "c", "Command": "memory_c", "Degrees": 50},
            {"Identifier": "d", "Command": "memory_d", "Degrees": 90},
            {"Identifier": "e", "Command": "memory_e", "Degrees": 120},
            {"Identifier": "f", "Command": "memory_f", "Degrees": 150},
            {"Identifier": "g", "Command": "memory_g", "Degrees": 180},
            {"Identifier": "h", "Command": "memory_h", "Degrees": 210},
            {"Identifier": "i", "Command": "memory_i", "Degrees": 240},
            {"Identifier": "j", "Command": "memory_j", "Degrees": 280},
            {"Identifier": "u", "Command": "memory_u", "Degrees": 320},
            {"Identifier": "l", "Command": "memory_l", "Degrees": 360},
        ]
        #end: config values
        
        #start: state values
        #self.Ticks = 0
        self.Degrees = 0.0
        self.PositionInitialized = False
        #end: state values
        
        return