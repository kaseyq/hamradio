from jsons import JsonSerializable

class RigConfig(JsonSerializable) :
    URL: str
    TunePower: int
    LogLevel: int
    def __init__(self) :
        self.URL = "http://10.0.0.52:12345"
        self.TunePower = 5
        self.LogLevel = 99