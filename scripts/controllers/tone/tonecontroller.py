import math
#import time
#from multiprocessing.dummy import Pool
from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio
from time import sleep
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
import numpy as np
import random
#import matplotlib.pyplot as plt
    
class ToneController(BaseController) :
    _name = "Tone Controller"
    _configName = "tone_config"
    _configClass = ToneConfig
    _poolSize = 10

    _playTone = False
    
    _pyAudio = object
    _playTone = False
    _stream = None
    _output = None
   
    _frequency = 440.00
    _duration = 1.0
    _volume = 1
    _sample_rate = 22050
    _stream = None
    _pyAudio = None

    #override
    def _initialize(self) :
        
        return
    
    def PlayShiftTone(self, frequency0 = 440.00, frequency1 = 550.0, duration = 1, volume = 1, sample_rate = 44100, baud_rate = 300) :

        #22050
        #44100

        if self._pyAudio == None :
            self._pyAudio = PyAudio()


        samples_per_bit = 1.0 / baud_rate * sample_rate

        bits_in_tones = [frequency0, frequency1] * 100

        bit_arr = np.array(bits_in_tones)


        symbols_freqs = np.repeat(bit_arr, samples_per_bit)
        t = np.arange(0, len(symbols_freqs) / sample_rate, 1.0 / sample_rate)
       

        #n_samples = float(sample_rate * duration)
        
        
        #if self._stream == None :
        stream = self._pyAudio.open(format=self._pyAudio.get_format_from_width(1), # 8bit
                        channels=1, # mono
                        rate=sample_rate,
                        output=True)

        #sampling_rate = 44100
        #baud_rate = 300



        s = lambda t: volume * math.sin(2 * math.pi * (frequency0 + ((t/n_samples) * (frequency1 - frequency0))) * t / sample_rate)
        #s = lambda t: np.sin(2.0 * np.pi * symbols_freqs * (t))


       #    t * 127 + 128
       # (int(s(t) * 0x7f + 0x80) 

        #s = lambda t: self._volume * math.sin(2 * math.pi * frequency0 * t / self._sample_rate)

        samples = (int(s(t) * 0x7f + 0x80) for t in xrange(samples_per_bit * bits_in_tones))

        #samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
        
        elapsed = 0.0

        #while elapsed < duration :
            #print(str(s(elapsed)*sample_rate))
            
            #output = izip(*s(elapsed)*sample_rate)

            #output = izip(*s(elapsed)*sample_rate)

            #izip(*[samples]*sample_rate)

            #stream.write(output)


            #time.sleep(0.001)
            #elapsed += 0.001


        for buf in izip(*[samples]*sample_rate): # write several samples at a time
            #self._output = bytes(bytearray(buf))
            stream.write(bytes(bytearray(buf)))

        
        stream.stop_stream()
        stream.close()
#        self._pyAudio.terminate()
        return

    def StartTone(self, frequency = 440.00, volume = 1, sample_rate = 22050, duration = 1.0):
        if self._playTone != False :
            return

        self._frequency = frequency
        self._volume = volume
        self._sample_rate = sample_rate
        self._duration = duration
            
        self._playTone = True
        

        
        if self._mock == True:
            return
            
        if self._pyAudio == None :
            self._pyAudio = PyAudio()
    
        self._info("StartTone")
        
        n_samples = int(self._sample_rate * self._duration)
        
        
        if self._stream == None :
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
        self._stream = None

        return

if __name__ == "__main__" :
    Mock = True
    emitter = ToneController(Mock)
    emitter.StartTone()

    time.sleep(3)
    
    emitter.StopTone()
    
