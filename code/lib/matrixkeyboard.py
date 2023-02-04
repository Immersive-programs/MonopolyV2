from machine import Pin, Timer

class MatrixKeyboard:
    def __init__(self, pinin, pinout, command):
        self.pinA = Pin(pinout[0], Pin.OUT, value = 1)
        self.pinB = Pin(pinout[1], Pin.OUT, value = 1) 
        self.pinC = Pin(pinout[2], Pin.OUT, value = 1)
        self.pinD = Pin(pinout[3], Pin.OUT, value = 1)
        self.outpins = [self.pinA, self.pinB, self.pinC, self.pinD]
                
        self.pin1 = Pin(pinin[0], Pin.IN, Pin.PULL_DOWN)
        self.pin2 = Pin(pinin[1], Pin.IN, Pin.PULL_DOWN)
        self.pin3 = Pin(pinin[2], Pin.IN, Pin.PULL_DOWN)
        self.pin4 = Pin(pinin[3], Pin.IN, Pin.PULL_DOWN)
        self.inpins = [self.pin1, self.pin2, self.pin3, self.pin4]
        
        self.unlocktimer = Timer()
        
        self.sendcommand = command
        
        self.__enabletrigger()
        
    def __downcount(self, down):
        downpin = self.inpins[down]
        downs = self.pin1.value()+self.pin2.value()+self.pin3.value()+self.pin4.value()
        if (downs == 1):
            self.pin1.irq(None)
            self.pin2.irq(None)
            self.pin3.irq(None)
            self.pin4.irq(None)
            for count, pin in enumerate(self.outpins):
                if downpin.value() == 1:
                    pin.value(0)
                    if downpin.value() == 0:
                        self.sendcommand('K{0}{1}'.format(count+1,down+1))
                        pin.value(1)
                        break
                    else:
                        pin.value(1)
            downpin.irq(handler = self.__unlocktrigger, trigger = Pin.IRQ_FALLING)
            self.unlocktimer.init(mode=Timer.ONE_SHOT, period=200, callback=lambda x:self.__timeout(downpin))
            
    def __timeout(self, pin):
        if pin.value():
            self.unlocktimer.init(mode=Timer.ONE_SHOT, period=200, callback=lambda x:self.__timeout(pin))
        else:
            self.__enabletrigger()
            
    def __unlocktrigger(self,line):
        self.unlocktimer.init(mode=Timer.ONE_SHOT, period=60, callback=lambda y:self.__enabletrigger())
            
    def __enabletrigger(self):
        self.unlocktimer.deinit()
        self.pin1.irq(handler = lambda l:self.__downcount(0), trigger = Pin.IRQ_RISING)
        self.pin2.irq(handler = lambda l:self.__downcount(1), trigger = Pin.IRQ_RISING)
        self.pin3.irq(handler = lambda l:self.__downcount(2), trigger = Pin.IRQ_RISING)
        self.pin4.irq(handler = lambda l:self.__downcount(3), trigger = Pin.IRQ_RISING)
    
    def deinit(self):
        self.unlocktimer.deinit()
        self.pin1.irq(None)
        self.pin2.irq(None)
        self.pin3.irq(None)
        self.pin4.irq(None)