#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Сreated by Immersive-programs:
#   github: https://github.com/Immersive-programs/micropython-toneplayback
from machine import PWM, Timer
class Buzzer:
    """Tone playback"""
    
    def __init__(self, pin):
        self.beeper = PWM(pin)
        self.beeptimer = Timer()
        self.beeps = []
        self.isenabled = True
        self.isbeeping = False
    
    def __beep(self):
        """Воспроизводит последовательность звуковых сигналов"""
        if self.isenabled:
            if len(self.beeps) > 0:
                self.isbeeping = True
                self.beeptimer.init(mode=Timer.ONE_SHOT, period=self.beeps[0][1], callback=lambda x: self.__beep())
                if self.beeps[0][0] <= 20:
                    self.beeper.duty_u16(1)
                else:
                    self.beeper.duty_u16(32768)
                self.beeper.freq(self.beeps[0][0])
                del self.beeps[0]
            else:
                self.beeper.freq(20)
                self.beeper.duty_u16(0)
                self.beeptimer.deinit()
                self.isbeeping = False

    def beep(self,beeps):
        """Добавляет и запускает последовательность звуковых сигналов"""
        self.beeps += beeps
        if not self.isbeeping:
           self.__beep()
                    
    def deinit(self):
        self.beeper.deinit()
        self.beeptimer.deinit()
