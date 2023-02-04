from customsymbols import CustomSymbols
from machine import Pin, SPI
from st7565 import ST7565
from loader import Loader
import sys
import os

DRST = Pin(1, Pin.OUT)
DRS  = Pin(4, Pin.OUT)
DCS  = Pin(5, Pin.OUT)
DSPIbus = SPI(0, baudrate=2000000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

class ST7565(ST7565, CustomSymbols): pass
sys.path.append("menu")
if 'symbols' in os.listdir('/'):
    sys.path.append("symbols")

Display = ST7565(DSPIbus, DRS, DCS, DRST)
Display.set_contrast(0x25)

Display.fill(0)
Display.ctext('Immersive',   10, 20, 1)
Display.ctext('Electronics', 30, 35, 1)
Display.show()

Loader(Display)





