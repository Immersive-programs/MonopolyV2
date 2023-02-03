from machine import Pin, SoftSPI, PWM, Timer
from matrixkeyboard import MatrixKeyboard
from ir_rx.nec import NEC_8
from buzzer import Buzzer
import NFC_PN532 as nfc
import math
import os

"""IR remote control buttons ID"""
IR0      = 'R16'
IR1      = 'R0c'
IR2      = 'R18'
IR3      = 'R5e'
IR4      = 'R08'
IR5      = 'R1c'
IR6      = 'R5a'
IR7      = 'R42'
IR8      = 'R52'
IR9      = 'R4a'
IR_BACK  = 'R09'
IR_PLAY  = 'R43'
IR_PlUS  = 'R15'
IR_MINUS = 'R07'
IR_NEXT  = 'R40'
IR_PREV  = 'R44'
IR_100   = 'R19'
IR_200   = 'R0d'

class Loader:
    def __init__(self, Display):
        self.Display = Display
              
        self.R = PWM(Pin(20))
        self.G = PWM(Pin(19))
        self.B = PWM(Pin(18))
        
        self.R.freq(500)
        self.G.freq(500)
        self.B.freq(500)
        
        self.setrgb(0.05, 0, 0)
        
        self.Buzzer = Buzzer(Pin(0))
        self.beep = self.Buzzer.beep
               
        sspi = SoftSPI(baudrate=1000000,sck=Pin(6), mosi=Pin(7), miso=Pin(8))
        self.pn532 = nfc.PN532(sspi, Pin(9, Pin.OUT, value = 1))
        self.pn532.SAM_configuration()
        
        self.games = []
        self.settingsgames = []
        self.lang = True
        self.invert = False
        self.sound = True
        self.contrast = 37
        self.__loadsettings()
        self.Beeper.isenabled = self.sound
        
        self.Display.set_contrast(self.contrast)
        
        if self.invert:
            self.Display.reverse()
            
        self.__searchgames()
           
        if not self.lang:
            self.Display.loadsymbols('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ') 
     
        self.__showmenu(True)
        self.beep([[500,100],[20,50],[1100,100],[20,50],[500,100]])        
        
        self.ControlCallback = self.__control
        self.IR = NEC_8(Pin(28, Pin.IN), self.__IR)
        self.keyboard = MatrixKeyboard([10,11,12,13], [14,15,17,16], self.__sendcommand)
        
    def reloadIR(self):
        self.IR = NEC_8(Pin(28, Pin.IN), self.__IR)
        
    def setdefaultcontrol(self):
        """Returns control of the main menu"""
        self.reloadIR()
        self.ControlCallback = self.__control
        
    def setcontrolmenu(self):
        """Returns to controlmenu"""
        from settingsmenu import SettingsMenu
        SettingsMenu(self)
        del SettingsMenu
        
    def setrgb(self,r,g,b):
        """Sets brightness RGB Leds"""
        self.R.duty_u16(round(65535 * r))
        self.G.duty_u16(round(65535 * g))
        self.B.duty_u16(round(65535 * b))
        
    def ellipse(self,x,y,dx,dy,col,s=False):
        """Draws ellipse"""
        bx = dx/2
        by = dy/2
        for i in range((dx+dy)*4):
            ax = round(x + bx + math.sin(i) * bx)
            ay = round(y + by + math.cos(i) * by)
            self.Display.pixel(ax,ay,col)
            if i < (dx+dy) * 1.7 and s and i % 2 == 0:
                self.Display.show()
          
    def __loadsettings(self):
        if not 'settings.conf' in os.listdir('/'):
            open('settings.conf','x').close()
            
        settings = open('settings.conf')
        while True:
            line = settings.readline()
            if not line:
                break
            
            read = line.split(':')
            if len(read) > 1:
                if   read[0] == 'lang':
                    self.lang = read[1]   == 'True\n'
                elif read[0] == 'invert':
                    self.invert = read[1] == 'True\n'
                elif read[0] == 'sound':
                    self.sound = read[1]  == 'True\n'
                elif read[0] == 'contrast':
                    self.contrast = int(read[1][:-1])
        settings.close()        
        
    def __searchgames(self):
        if 'games' in os.listdir('/'):
            self.games = os.listdir('games')
            for name in self.games:
                try:
                    for path in os.listdir('games/'+name):
                        if path == 'options.py':
                            self.settingsgames.append(name)
                except:
                    print("not found folder:"+name)
            self.__genlinksgames()
        
    def __genlinksgames(self):
        """Сrutch for dynamic linking games"""
        if not 'temppaths.py' in os.listdir('/'):
            open('temppaths.py','x').close()
        temppaths = open('temppaths.py')
        games = temppaths.readline().replace('#','').split(':')
        if '\n' in games:
            games.remove('\n')
        settingsgames = temppaths.readline().replace('#','').split(':')
        if '\n' in settingsgames:
            settingsgames.remove('\n')
        temppaths.close()
        if not games == self.games or not settingsgames == self.settingsgames:
            temppaths = open('temppaths.py','w')
            temppaths.write('#'+':'.join(self.games)+':\n')
            temppaths.write('#'+':'.join(self.settingsgames)+':\n')
            temppaths.write('class TempPaths:\n')
            temppaths.write('    def start(name,Loader):\n')
            for game in self.games:
                temppaths.write('        if name == \''+game+'\':\n')
                temppaths.write('            from games.'+game+'.run import Run\n')
                temppaths.write('            Run(Loader)\n')
            for settingsgame in self.settingsgames:
                temppaths.write('        if name == \''+settingsgame+'o\':\n')
                temppaths.write('            from games.'+settingsgame+'.options import Options\n')
                temppaths.write('            Options(Loader)\n')
            temppaths.close
            
    def __showmenu(self,f = False):
        self.Display.fill(0)
        if self.lang:
            self.Display.ctext('TERMINAL V2:', 0, 1, 1)
            self.Display.ctext('PLAY>A', 39, 16, 1)
            self.Display.ctext('CONTROL>B', 28, 27, 1)
            self.Display.ctext('SETTINGS>C', 23, 38, 1)
            self.Display.ctext('MAKERS>D', 31, 49, 1)
        else:
            self.Display.ctext('ТЕРМИНАЛ V2:', 0, 1, 1)
            self.Display.ctext('ИГРАТЬ>A', 33, 16, 1)
            self.Display.ctext('УПРАВЛЕНИЕ>B', 16, 27, 1)
            self.Display.ctext('НАСТРОЙКИ>C', 20, 38, 1)
            self.Display.ctext('АВТОРЫ>D', 33, 49, 1)
        self.ellipse(2,10,123,52,1,f)
        self.Display.show()
        self.setrgb(0.01,0.05,0.05)
        
    def __control(self,command):
        if command == 3:
            from gamemenu import GameMenu
            GameMenu(self)
            del GameMenu
        elif command == 7:
            from сontrolmenu import ControlMenu
            ControlMenu(self)
            del ControlMenu
        elif command == 11:
            from settingsmenu import SettingsMenu
            SettingsMenu(self)
            del SettingsMenu
        elif command == 15:
            from aboutmenu import AboutMenu
            AboutMenu(self)
            del AboutMenu
                  
    def __sendcommand(self, command):
        if   command == IR1 or command      == 'K11':
            self.ControlCallback(0)
        elif command == IR2 or command      == 'K12':
            self.ControlCallback(1)
        elif command == IR3 or command      == 'K13':
            self.ControlCallback(2)
        elif command == IR_PlUS or command  == 'K14':
            self.ControlCallback(3)
        elif command == IR4 or command      == 'K21':
            self.ControlCallback(4)
        elif command == IR5 or command      == 'K22':
            self.ControlCallback(5)
        elif command == IR6 or command      == 'K23':
            self.ControlCallback(6)
        elif command == IR_MINUS or command == 'K24':
            self.ControlCallback(7)
        elif command == IR7 or command      == 'K31':
            self.ControlCallback(8)
        elif command == IR8 or command      == 'K32':
            self.ControlCallback(9)
        elif command == IR9 or command      == 'K33':
            self.ControlCallback(10)
        elif command == IR_NEXT or command  == 'K34':
            self.ControlCallback(11)
        elif command == IR_PLAY or command  == 'K41':
            self.ControlCallback(12)
        elif command == IR0 or command      == 'K42':
            self.ControlCallback(13)
        elif command == IR_BACK or command  == 'K43':
            self.ControlCallback(14)
        elif command == IR_PREV or command  == 'K44':
            self.ControlCallback(15)
        elif command == IR_100:
            self.ControlCallback(16)
        elif command == IR_200:
            self.ControlCallback(17)
                    
    def __IR(self,data, addr, ctrl):
        self.__sendcommand('R{:02x}'.format(data))
