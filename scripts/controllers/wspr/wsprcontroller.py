#!/usr/bin/python3

try:
    import RPi.GPIO as GPIO
except ImportError :
    print("ignore")
    #import GPIO as GPIO

import time
import sys
#from optparse import OptionParser
from random import randrange

# locals
try:
    from .wsprconfig import WSPRConfig
except ImportError :
    from wsprconfig import WSPRConfig

# locals
try:
    from .genwsprcode import Genwsprcode
    #from .genwsprcode import g
except ImportError :
    print("ignore")
    #from genwsprcode import Genwsprcodeas as g
    #from genwsprcode import g

from ...common._basecontroller import BaseController

class WSPRController(BaseController) :
    _name = "WSPR Controller"
    _configName = "wspr_config"
    _configClass = WSPRConfig
    _mock = False

    # set variables
    W_CLK=18
    FQ_UD=23
    DATA=24
    RESET=25
    freq_shift=12000/8192
    offset=0
    WORD1='00000001'#W0 multiplier6x, power up
    WORD0='00000101'#W0 power down, multiplier6x    


    
    #wspr_freq={ '2190m' : '137500',
    #            '630m' : '475700',
    #            '160m' : '1838100',
    #            '80m' : '3594100',
    #            '60m' : '5288700', 
    #            '40m' : '7040100',
    #            '30m' : '10140200',
    #            '20m' : '14097100', 14.09560
    #            '17m' : '18106100',
    #            '15m' : '21096100',
    #            '12m' : '24926100',
    #            '10m' : '28126100',
    #            '6m' : '50294500',
    #            '2m' : '144490000'
    #           }

    callsign = None
    grid = None
    power = None
    frequency = None
    symbols = None

    def _initialize(self) :
        #self._mock = mock
        self._setup()
        self.frequency = 14.0956 * 10000
        self.callsign = self._c().Callsign
        self.grid = self._c().Grid
        self.power = self._c().Power

        return

    # setup GPIO
    def _setup(self):

        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(W_CLK,GPIO.OUT)
        #GPIO.setup(FQ_UD,GPIO.OUT)
        #GPIO.setup(DATA,GPIO.OUT)
        #GPIO.setup(RESET,GPIO.OUT) 
        #GPIO.output(DATA,0)
        return

    def _reset(self) :
        #GPIO.output(RESET,1)
        #GPIO.output(RESET,0)
        #GPIO.output(W_CLK,1)
        #GPIO.output(W_CLK,0)
        #GPIO.output(FQ_UD,1)
        #GPIO.output(FQ_UD,0)
        return

    #def _AD9851(self, freq, WORD, symbol):
    #    if freq > 70000000:
    #        self._print('AD9851: frequency must be lower than 70 mHz',file=sys.stderr) 
    #        sys.exit(-1)
    #    fsk=symbol*self.freq_shift #frequency shift key
    #    freq_word_int=int((freq+fsk)*(2**32)/(6*30e6+self.offset)) ##6xrefclock turned on in WORD0 
    #    FREQWORD='{0:032b}'.format(freq_word_int)
        
        #SERIALWORD=WORD+FREQWORD
        #for i in range(39,-1,-1):
        #    GPIO.output(W_CLK,0)
        #    if int(SERIALWORD[i]):
        #        GPIO.output(DATA,1)
        #    GPIO.output(W_CLK,1)
        #    GPIO.output(DATA,0)
        #    GPIO.output(W_CLK,0)
        #GPIO.output(FQ_UD,1)
        #GPIO.output(FQ_UD,0)
     #   return()


    def Transmit(self) :
        symbols= Genwsprcode(self.callsign,self.grid,self.power)
        symbols=symbols.rstrip(',')
        symbols=symbols.split(',')

        self._transmit(symbols)

        return

    def _transmit(self, symbols) :
        frequency=self.frequency+randrange(-200,200)

        #if opts.offset:
        #    frequency=frequency+randrange(-80,81)

        self._print('Start of transmission on: %s' %(time.strftime('%H:%M:%S',time.gmtime(time.time()))))
        self._print('Frequency: {0:,.0f} Hz'.format(self.frequency))

        for symbol in symbols: #modulate the symbols
            #self.play(self.frequency,self.WORD1,int(x))
            print(symbol)

            startToneFq = 0
            endToneFq = 0
            #tonefq = self.frequency + symbol
            duration = (1/self.freq_shift)-time.time() % (1/self.freq_shift)


            if symbol == str(0):
                startToneFq = -2.197265625
            elif symbol == str(1) :
                startToneFq = -0.732421875
            elif symbol == str(2) :
                startToneFq = 0.732421875
            elif symbol == str(3) :
                startToneFq = 2.197265625

            startToneFq = startToneFq + 500
            endToneFq = startToneFq + 1.46484375

#The channel symbol output corresponds to lowest to highest frequencies, from 0 to 3, with 1.46484375 (= 12000/8192) Hz frequency shift, respectively.
#The channel spacing diagram from the center frequency:
#Symbol 0: -2.197265625 Hz ( = -18000/8192 Hz)
#Symbol 1: -0.732421875 Hz ( = -6000/8192 Hz)
#Symbol 2: +0.732421875 Hz ( = +6000/8192 Hz)
#Symbol 3: +2.197265625 Hz ( = +18000/8192 Hz)
#Transmission rate: 1.46484375 baud = 0.682666667 second/symbol = 8192/12000 second
            print("Start Tone = " + str(startToneFq)) 

            print("End Tone = " + str(endToneFq)) 
            print("Duration = " + str(duration))

            self._controls.ToneControl().PlayShiftTone(startToneFq, endToneFq, duration)

            self._sleep(duration)
            
            #self._controls.ToneControl().StopTone()

        self._reset()
        self._print('End of transmission on: %s'%(time.strftime('%H:%M:%S',time.gmtime(time.time()))))

    def play(self, freq, WORD, symbol) :


        return
        
  