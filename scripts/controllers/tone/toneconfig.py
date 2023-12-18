from jsons import JsonSerializable


class ToneConfig(JsonSerializable):
	Something: str
	def __init__(self) :
		self.Something = "Something"
		return