import math
#import time
#from multiprocessing.dummy import Pool
from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio

try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

# locals
try:
    from .toneconfig import ToneConfig
#    from ....common._basecontroller import BaseController
except ImportError :
    from toneconfig import ToneConfig    
#    from ....common._basecontroller import BaseController
    
from ...common._basecontroller import BaseController

    
class ToneController(BaseController) :
    _name = "Tone Controller"
    _configName = "tone_config"
    _configClass = ToneConfig
    _poolSize = 10

    _playTone = False
    _frequency = 440.00
    _duration = 1
    _volume = 1
    _sample_rate = 22050
    _pyAudio = object
    _playTone = False
    _stream = None
    _output = None
   
    #override
    def _initialize(self) :
        self._pyAudio = PyAudio()
        return
    
    def StartTone(self):
        if self._playTone != False :
            return
            
        self._playTone = True
        
        
        if self._mock == True:
            return
            
        self._info("StartTone")

        #frequency = 440.00
        #duration = 1
        #volume = 1
        #sample_rate = 22050
        
        n_samples = int(self._sample_rate * self._duration)
        
        
        self._stream = self._pyAudio.open(format=self._pyAudio.get_format_from_width(1), # 8bit
                        channels=1, # mono
                        rate=self._sample_rate,
                        output=True)
                        
        s = lambda t: self._volume * math.sin(2 * math.pi * self._frequency * t / self._sample_rate)
        samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
        
        for buf in izip(*[samples]*self._sample_rate): # write several samples at a time
            self._output = bytes(bytearray(buf))
            self.HandleAsyncTone()
            break
            
    def HandleAsyncTone(self, result=None) :
        self._print("HandleAsyncTone", 99)
        if self._mock == True :
            return
            
        if self._playTone == True :
            self._requestsPool.apply_async(self.AsyncTonePlay, callback=self.HandleAsyncTone)
        else:
            self.CloseStream()
            
        return
    
    def AsyncTonePlay(self) :
        self._print("AsyncTonePlay", 99)
        if self._mock == True:
            return
            
        if self._playTone == True :
            self._stream.write(self._output)
        else :
            self.CloseStream()

        return

    def StopTone(self) :
        self._info("StopTone")
        if self._playTone != True :
            return
        
        self._playTone = False
                
    def CloseStream(self) :
        self._info("CloseStream")
        self._stream.stop_stream()
        self._stream.close()
        self._pyAudio.terminate()

        return

if __name__ == "__main__" :
    Mock = True
    emitter = ToneController(Mock)
    emitter.StartTone()

    time.sleep(3)
    
    emitter.StopTone()
    
