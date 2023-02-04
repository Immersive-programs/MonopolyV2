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

# Сreated by nquest
#   github: https://github.com/nquest/micropython-st7565
# Modified by Immersive-programs
#   github: https://github.com/Immersive-programs/micropython-st7565

from micropython import const
from time import sleep_ms, sleep_us
import framebuf

# LCD Commands definition
CMD_DISPLAY_ON = const(0xa4)
CMD_DISPLAY_OFF = const(0xAF)
CMD_SET_START_LINE = const(0x40)
CMD_SET_PAGE = const(0xB0)
CMD_COLUMN_UPPER = const(0x10)
'''CMD_COLUMN_LOWER:
    set 0x04 for the correct display on the GMG-12864-06D
    установленно 0x04 для коректного отображания на дисплее GMG-12864-06D'''
CMD_COLUMN_LOWER = const(0x04)#default / стандартное 0x00
CMD_SET_ADC_NORMAL = const(0xA0)
CMD_SET_ADC_REVERSE = const(0xA1)
CMD_SET_COL_NORMAL = const(0xC0)
CMD_SET_COL_REVERSE = const(0xC8)
CMD_SET_DISPLAY_NORMAL = const(0xA6)
CMD_SET_DISPLAY_REVERSE = const(0xA7)
CMD_SET_ALLPX_ON = const(0xA5)
CMD_SET_ALLPX_NORMAL = const(0xA4)
CMD_SET_BIAS_9 = const(0xA2)
CMD_SET_BIAS_7 = const(0xA3)
CMD_DISPLAY_RESET = const(0xE2)
CMD_NOP = const(0xE3)
CMD_TEST = const(0xF0)  # Exit this mode with CMD_NOP
CMD_SET_POWER = const(0x28)
CMD_SET_RESISTOR_RATIO = const(0x20)
CMD_SET_VOLUME = const(0x81)

# Display parameters
DISPLAY_W = const(128)
DISPLAY_H = const(64)
DISPLAY_CONTRAST = const(0x25)
DISPLAY_RESISTOR_RATIO = const(5)
DISPLAY_POWER_MODE = 7

class ST7565(framebuf.FrameBuffer):
    """ST7565 Display controller driver"""
    def __init__(self, spi, a0, cs, rst):
        self.spi = spi
        self.rst = rst
        self.a0 = a0
        self.cs = cs
        self.width = DISPLAY_W
        self.height = DISPLAY_H
        self.buffer = bytearray(1024)
        self.invertp = False # pixels
        self.invertx = False # x
        self.inverty = False # y 
        self.invertr = False # render
        super().__init__(
            self.buffer,
            self.width,
            self.height,
            framebuf.MONO_VLSB)
        self.display_init()

    def display_init(self):
        self.reset()
        sleep_ms(1)
        for cmd in (
            CMD_DISPLAY_OFF,  # Display off
            CMD_SET_BIAS_9,  # Display drive voltage 1/9 bias
            CMD_SET_ADC_REVERSE,  # Reverse SEG
            CMD_SET_COL_NORMAL,  # Commmon mode normal direction
            CMD_SET_RESISTOR_RATIO + DISPLAY_RESISTOR_RATIO,  # V5 R ratio
            CMD_SET_VOLUME,  # Contrast
            DISPLAY_CONTRAST,  # Contrast value
                CMD_SET_POWER + DISPLAY_POWER_MODE):
            self.write_cmd(cmd)
        self.show()
        self.write_cmd(CMD_DISPLAY_ON)

    def write_cmd(self, cmd):
        self.a0(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.a0(1)
        self.cs(0)
        
        invx = self.invertx
        invy = self.inverty 
        
        '''mirrors the string by sending bytes in reverse order
        отзеркаливает строку отправляя байты в обратном порядке'''
        if invx or invy:
            for i in range(128):
                if invx: i = 127 - i #reverse i
                dec = buf[i]#gets dec
                if dec and invy:
                    dec = self._reversebyte(dec)#reverse byte
                self.spi.write(bytearray([dec]))
        else:
            self.spi.write(buf)
        self.cs(1)

    def set_contrast(self, value):
        if 0x1 <= value <= 0x3f:
            for cmd in (
                CMD_SET_VOLUME,
                    value):
                self.write_cmd(cmd)
                
    def reverse(self, value = None):#flips all pixels on display / переворачивает все пиксели на дисплее
        if value != None:
            self.invertp = ~value
        self.write_cmd((CMD_SET_DISPLAY_REVERSE,
                        CMD_SET_DISPLAY_NORMAL)[self.invertp])
        self.invertp = ~self.invertp
        
    def invert_y(self, value = None):#inverts the y axis when outputting / инвертирует ось y при выводе
        if value != None:
            self.inverty = ~value
        self.inverty = ~self.inverty
    
    def invert_x(self, value = None):#inverts the x axis when outputting / инвертирует ось x при выводе
        if value != None:
            self.invertx = ~value
        self.invertx = ~self.invertx
    
    def invert_render(self, value = None):#inverts the render when outputting / инвертирует рендеринг при выводе
        if value != None:
            self.invertr = ~value
        self.invertr = ~self.invertr
        
    def flip_framebuff(self):#flips all bytes along the x and y axes in the buffer / переворачивает все байты по осям х и у в буфере
        buffer = self.buffer[0:1024]#gets a copy of the buffer / получает копию буфера
        for i in range(1024):
            dec = buffer[1023-i]
            if dec:
                dec = self._reversebyte(dec)#reverse byte
            self.buffer[i] = dec
    
    def flip_y_framebuff(self): #flips all bytes along the y axes in the buffer / переворачивает все байты по осям у в буфере
        c = 0
        buffer = self.buffer[0:1024]#gets a copy of the buffer / получает копию буфера
        for i in range(8):
            buf = buffer[(7-i)*128:(7-i+1)*128]
            for b in range(128):
                dec = buf[b]
                if dec:
                    dec = self._reversebyte(dec)#reverse byte
                self.buffer[c] = dec
                c +=1
    
    def flip_x_framebuff(self):#flips all bytes along the x axes in the buffer /  переворачивает все байты по осям x в буфере
        c = 0
        for i in range(8):
            buf = self.buffer[i*128:(i+1)*128]
            for b in range(128):
                self.buffer[c] = buf[127-b]
                c +=1

    def reset(self):
        self.rst(0)
        sleep_us(1)
        self.rst(1)
    
    def show(self):
        viewbuffer = memoryview(self.buffer) #alleviated using a memoryview / облегчить с помощью memoryview
        for i in range(8):
            '''inverts the layer sending counter to change the initial rendering side
            инвертиует счетчик отправки слоёв для изменения начальной стороны отрисовки'''
            if self.invertr: i = 7-i 
            for cmd in (
                CMD_SET_START_LINE,
                CMD_SET_PAGE + i,
                CMD_COLUMN_UPPER,
                CMD_COLUMN_LOWER):
                self.write_cmd(cmd)
            if self.inverty:
                '''sends parts of the buffer in reverse order which reverses the displayed pages
                отправляет части буфера в обратном порядке, что переворачивает отображаемые страницы'''
                self.write_data(viewbuffer[(7-i)*128:(7-i+1)*128])
            else:
                self.write_data(viewbuffer[i*128:(i+1)*128])#normal
         
    def _reversebyte(self,byte):#flips a byte / переворачивает байт
        '''example: 0x11010100 -> 0x00101011'''
        bitstring = bin(byte)[2:10]#gets bitstring /получает битовую строку
        bitstring = "".join(reversed(bitstring))#reverse line / реверс строки
        bitstring += '0'*(8-len(bitstring))#adds missing zeros / добавляет недостающие нули
        return int(bitstring,2) #collect bytes and return/ собираем байт и возвращаем
