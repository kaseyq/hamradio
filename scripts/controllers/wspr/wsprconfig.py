#wsprconfig
#callsign = None
#grid = None
#power = None



from jsons import JsonSerializable

class WSPRConfig(JsonSerializable) :
    Callsign: str
    Grid:str
    Power:str

    def __init__(self) :
        self.Callsign = "KK7NTW"
        self.Grid = "CN87"

 #       self.Grid = "CN87qo"
#        print(self.Grid)
        self.Power = "00"

        return
    
