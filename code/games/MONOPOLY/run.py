from machine import Timer
from time import sleep
import os

class Run:
    def __init__(self,loader):
        loader.ControlCallback = self.__control
        self.path = '/games/MONOPOLY/'
        self.Loader = loader
        self.selsectors = -1
        self.selsected = -1
        self.color = 1
        self.showselsected = False
        self.autosave = True
        self.m = False
        self.y = 0
        self.moneybuf = 0
        self.moneybufsend = 0
        self.startbalance = 1500
        self.buffcard = ''
        self.balance = []
        self.players = []
        self.names = []
        self.idnames = []
        
        self.__loadsettings()
        self.__loadsnames()
        
        self.stagelist = {}
        self.stagelist[0] = self.__addplayercard
        self.stagelist[2] = self.__transfercard
        self.stagelist[3] = self.__transfercard
        self.stagelist[5] = self.__operationcard
        self.stage = 0
        
        self.r, self.g, self.b = 0, 0.05, 0.4
        self.rgbmode = 0
        self.Loader.setrgb(self.r,self.g,self.b)
        
        self.timer = Timer()
        self.rgbtimer = Timer()
        self.timer.init(mode=Timer.PERIODIC, period=200, callback=self.__cardsearch)
        self.rgbtimer.init(mode=Timer.PERIODIC, period=100, callback=self.__ledchange)
        
        self.Loader.beep([[500,300],[20,100],[600,300]])
        
        self.restore = 'save.conf' in os.listdir(self.path)
        if self.restore and self.autosave:
           self.__showrestore()
        else:
            self.__showmenu()
        
    def __showrestore(self):
        self.Loader.Display.fill(0)
        self.Loader.Display.ctext('----------------', 0, 1, 1)
        self.Loader.Display.ctext('|              |', 0, 11, 1)
        self.Loader.Display.ctext('|              |', 0, 21, 1)
        self.Loader.Display.ctext('|              |', 0, 31, 1)
        self.Loader.Display.ctext('|              |', 0, 41, 1)
        self.Loader.Display.ctext('----------------', 0, 51, 1)
        if self.Loader.lang:
            self.Loader.Display.ctext('  RESUME GAME?', 0, 21, 1)
        else:
            self.Loader.Display.ctext(' ЗАГРУЗИТЬИГРУ?', 0, 21, 1)
            
        if self.selsected == -1: self.color = not self.color
        self.Loader.Display.fill_rect(16, 30, 24, 9, not self.color)
        if self.Loader.lang:
            self.Loader.Display.ctext('YES', 16, 31, self.color)
        else:
            self.Loader.Display.ctext('ДА', 20, 31, self.color)
        self.color = 1    
        if self.selsected == 0: self.color = not self.color
        self.Loader.Display.fill_rect(88, 30, 24, 9, not self.color)
        if self.Loader.lang:
            self.Loader.Display.ctext('NO', 92, 31, self.color)
        else:
            self.Loader.Display.ctext('НЕТ', 88, 31, self.color)
        self.color = 1
            
        self.Loader.Display.show()
         
    def __operationmenu(self):
        self.Loader.Display.fill(0)
        self.Loader.Display.ctext('----------------', 0, 31, 1)
        self.Loader.Display.ctext('              <|', 0, 41, 1)
        self.Loader.Display.ctext('----------------', 0, 51, 1) 
        if self.Loader.lang:
            self.Loader.Display.ctext('BRING THE CARD', 6, 1, 1)
            self.Loader.Display.ctext('MONEY', 39, 21, 1)
        else:
            self.Loader.Display.ctext('ПОДНЕСИТЕ КРАРТУ', 0,  1, 1)
            self.Loader.Display.ctext('СРЕДСТВ', 39, 21, 1)
        total = 0
        if self.m:
            total = self.moneybufsend - self.moneybuf
        else:
            total = self.moneybufsend + self.moneybuf
        if total > 0:
            self.r, self.g, self.b = 0, 0.4, 0.05
            self.rgbmode = 5
            self.Loader.setrgb(self.r,self.g,self.b)
            self.Loader.Display.ctext('|>+' + str(total) + '$', 0, 41, 1)
            if self.Loader.lang:
                self.Loader.Display.ctext('TO GET', 36, 11, 1)
            else:
                self.Loader.Display.ctext('ДЛЯ ПОЛУЧЕНИЯ', 17, 11, 1)
        else:
            self.rgbmode = 3
            self.r, self.g, self.b = 0.05, 0, 0.4
            self.Loader.setrgb(self.r,self.g,self.b)
            self.Loader.Display.ctext('|>' + str(total) + '$', 0, 41, 1)
            if self.Loader.lang:
                self.Loader.Display.ctext('TO DEBITING', 19, 11, 1)
            else:
                self.Loader.Display.ctext('ДЛЯ СПИСАНИЯ', 24, 11, 1)       
        self.Loader.Display.show()

    def __transfermenu(self):
        self.Loader.Display.fill(0)
        if self.Loader.lang:
            self.Loader.Display.ctext('BRING THE CARD', 6, 1, 1)
            self.Loader.Display.ctext('MONEY', 39, 21, 1)
            if self.stage == 2:
                self.Loader.Display.ctext('TO DEBITING', 19, 11, 1)
            else:
                self.Loader.Display.ctext('TO GET', 36, 11, 1)
        else:
            self.Loader.Display.ctext('ПОДНЕСИТЕ КРАРТУ', 0, 1, 1)
            self.Loader.Display.ctext('СРЕДСТВ', 39, 21, 1)
            if self.stage == 2:
                self.Loader.Display.ctext('ДЛЯ СНЯТИЯ', 24, 11, 1)
            else:
                self.Loader.Display.ctext('ДЛЯ ПОЛУЧЕНИЯ', 17, 11, 1)

        self.Loader.Display.ctext('----------------', 0, 31, 1)
        self.Loader.Display.ctext('              <|', 0, 41, 1)
        if self.stage == 2:
            self.Loader.Display.ctext('|>-' + str(self.moneybuf) + '$', 0, 41, 1)
        else:    
            self.Loader.Display.ctext('|>+' + str(self.moneybuf) + '$', 0, 41, 1)
        self.Loader.Display.ctext('----------------', 0, 51, 1) 
        self.Loader.Display.show()
        
    def __inputmenu(self):
        self.Loader.Display.fill(0)
        if self.stage == 1:
            if self.Loader.lang:
                self.Loader.Display.ctext('TRANSFER AMOUNT:', 3, 1, 1)
                self.Loader.Display.ctext('PLAY/* > NEXT', 0, 41, 1)
                self.Loader.Display.ctext('PREV/D > CANSEL', 0, 51, 1)
            else:
                self.Loader.Display.ctext('ПЕРЕВОД СУММЫ:', 0, 1, 1)
                self.Loader.Display.ctext('PLAY/*ПРОДОЛЖИТЬ', 0, 41, 1)
                self.Loader.Display.ctext('PREV/D ОТМЕНИТЬ', 0, 51, 1)
        if self.stage == 4:
            if self.m:
                total = self.moneybufsend - self.moneybuf
            else:
                total = self.moneybufsend + self.moneybuf
            self.Loader.Display.fill_rect(0, 40, 128, 9, not self.color)
            if self.Loader.lang:
                self.Loader.Display.ctext('BANK OPERATION:', 0, 1, 1)
                self.Loader.Display.ctext('|TOTAL>' + str(total) + '$', 0, 41, 1)
            else:
                self.Loader.Display.ctext('ОПЕРАЦИЯ БАНКА:', 0, 1, 1)
                self.Loader.Display.ctext('|ИТОГО>' + str(total) + '$', 0, 41, 1)
            self.Loader.Display.ctext('              <|', 0, 41, 1) 
            self.Loader.Display.ctext('----------------', 0, 51, 1)
 
        self.Loader.Display.ctext('----------------', 0, 11, 1)
        self.Loader.Display.fill_rect(0, 20, 128, 9, not self.color)
        self.Loader.Display.ctext('              <|', 0, 21, 1)
        if self.stage == 4:
            if self.m:
                self.Loader.Display.ctext('|>-' + str(self.moneybuf) + '$', 0, 21, 1)
            else:
                self.Loader.Display.ctext('|>+' + str(self.moneybuf) + '$', 0, 21, 1)
        else:
            self.Loader.Display.ctext('|>' + str(self.moneybuf) + '$', 0, 21, 1)
        self.Loader.Display.ctext('----------------', 0, 31, 1)
        
        self.Loader.Display.show()
        
    def __showmenu(self):
        self.Loader.Display.fill(0)
        if self.Loader.lang:
            self.Loader.Display.ctext('PLAYERS: | MONEY', 0, self.y + 1, 1)
        else:
            self.Loader.Display.ctext('ИГРОКИ:  |БАЛАНС', 0, self.y + 1, 1)
            
        for count, player in enumerate(self.players):
            if self.selsected == count and self.showselsected: self.color = not self.color
            self.Loader.Display.fill_rect(0, self.y + (count+1) * 10, 128, 9, not self.color)
            if not self.names[count] == 'None':
                self.Loader.Display.ctext(self.names[count], 0, self.y + (count+1) * 10 + 1, self.color)
            else:
                if self.Loader.lang:
                    self.Loader.Display.ctext('PLAYER>' + str(count+1), 0, self.y + (count+1) * 10 + 1, self.color)
                else:
                    self.Loader.Display.ctext('ИГРОК>' + str(count+1), 0, self.y + (count+1) * 10 + 1, self.color)
            self.Loader.Display.ctext(str(self.balance[count])+'$', (16-len(str(self.balance[count]))-1)*8, self.y + (count+1) * 10 + 1, self.color)
            self.color = 1
        
        if len(self.players) < 2:
            if self.Loader.lang:
                self.Loader.Display.ctext('TO GET STARTED', 6, 31, 1)
                self.Loader.Display.ctext('BRING THE CARDS', 3, 41, 1)
            else:
                self.Loader.Display.ctext('ДЛЯ НАЧАЛА ИГРЫ', 3, 31, 1)
                self.Loader.Display.ctext('ПОДНЕСИТЕ КАРТЫ', 3, 41, 1)
        self.Loader.Display.show()
        
    def __endsuccess(self,timer):
        self.stage = 0
        self.r, self.g, self.b = 0, 0.05, 0.4
        self.rgbmode = 0
        self.Loader.setrgb(self.r,self.g,self.b)
        self.__showmenu()
        
    def __success(self):
        self.stage = 99
        self.rgbmode = 99
        self.Loader.setrgb(0,0.8,0)
        self.Loader.Display.fill(0)
        self.Loader.ellipse(34,1,61,61,1)
        self.Loader.ellipse(35,2,59,59,1)
        self.Loader.ellipse(36,3,57,57,0)
        self.Loader.ellipse(37,4,55,55,1)
        self.Loader.ellipse(38,5,53,53,1)
        self.Loader.Display.line(64,50,50,36,1)
        self.Loader.Display.line(64,49,51,36,1)
        self.Loader.Display.line(64,48,52,36,1)
        self.Loader.Display.line(64,47,53,36,1)
        self.Loader.Display.line(64,46,54,36,1)
        
        self.Loader.Display.line(65,50,80,20,1)
        self.Loader.Display.line(65,49,79,20,1)
        self.Loader.Display.line(65,47,78,20,1)
        self.Loader.Display.line(65,45,77,20,1)
        self.Loader.Display.show()
        if self.autosave:
            self.__savescore()
        Timer().init(mode=Timer.ONE_SHOT, period=2000, callback=self.__endsuccess)
 
    def __operationcard(self, uuid):
        if uuid in self.players:
            total = 0
            if self.m:
                total = self.moneybufsend - self.moneybuf
                self.Loader.beep([[300,250]])
            else:
                total = self.moneybufsend + self.moneybuf
                self.Loader.beep([[800,200]])
            self.balance[self.players.index(uuid)] += total
            self.__success()
        
    def __transfercard(self, uuid):
        if uuid in self.players:
            if self.stage == 2:
                self.buffcard = uuid
                self.stage = 3
                self.r, self.g, self.b = 0, 0.4, 0.05
                self.rgbmode = 5
                self.Loader.setrgb(self.r,self.g,self.b)
                self.Loader.beep([[300,250]])
                self.__transfermenu()
            elif self.stage == 3:
                if not uuid in self.buffcard:
                    self.Loader.beep([[800,200]])
                    self.balance[self.players.index(uuid)]          += self.moneybuf
                    self.balance[self.players.index(self.buffcard)] -= self.moneybuf
                    self.__success()
                     
    def __addplayercard(self, uuid):
        if not uuid in self.players:
            self.selsectors +=1
            self.players.append(uuid)
            self.balance.append(self.startbalance)
            if len(self.idnames) > 0:
                for uid in self.idnames:
                    if uuid == uid[0]:
                        self.names.append(uid[1])
                if len(self.names) < len(self.players):
                    self.names.append('None')
            else:
                self.names.append('None')
            self.Loader.beep([[700,150]])
        self.selsected = self.players.index(uuid)
        if self.selsected > 4:
            self.y = 10 * (4 - self.selsected)
        else:
            self.y = 0
        self.showselsected = True
        self.__showmenu()
        
    def __cardsearch(self, timer):
        if self.Loader.IR.edge == 0 and self.stage in self.stagelist:
            uid = self.Loader.pn532.read_passive_target(timeout=0.01)
            if not uid is None:
                uuid = "0x%02x%02x%02x%02x" % (uid[0], uid[1], uid[2], uid[3])
                self.stagelist[self.stage](uuid)
            else:
                if self.showselsected:
                    self.showselsected = False
                    self.__showmenu()
                               
    def __ledchange(self, timer):
        if self.rgbmode == 0:
            self.g += 0.01
            self.b -= 0.01
            self.Loader.setrgb(self.r,self.g,self.b)
            if self.g >= 0.3: self.rgbmode = 1
        if self.rgbmode == 1:
            self.g -= 0.01
            self.b += 0.01
            self.Loader.setrgb(self.r,self.g,self.b)
            if self.g <= 0.05: self.rgbmode = 0
        if self.rgbmode == 3:
            self.r += 0.01
            self.b -= 0.01
            self.Loader.setrgb(self.r,self.g,self.b)
            if self.r >= 0.3: self.rgbmode = 4
        if self.rgbmode == 4:
            self.r -= 0.01
            self.b += 0.01
            self.Loader.setrgb(self.r,self.g,self.b)
            if self.r <= 0.05: self.rgbmode = 3
        if self.rgbmode == 5:
            self.b += 0.01
            self.g -= 0.01
            self.Loader.setrgb(self.r,self.g,self.b)
            if self.b >= 0.3: self.rgbmode = 6
        if self.rgbmode == 6:
            self.b -= 0.01
            self.g += 0.01
            self.Loader.setrgb(self.r,self.g,self.b)
            if self.b <= 0.05: self.rgbmode = 5
        
    def __loadsettings(self):
        if not 'options.conf' in os.listdir(self.path):
            open(self.path + 'options.conf','x').close()
        settings = open(self.path + 'options.conf')
        while True:
            line = settings.readline()
            if not line:
                break
            read = line.split(':')
            if '\n' in read:
                read.remove('\n')
            if len(read) > 1:
                if read[0] == 'money':
                    self.startbalance = int(read[1])
                if read[0] == 'autosave':
                    self.autosave = read[1] == 'True'
        settings.close()
        
    def __addnumber(self,number):
        if self.moneybuf == 0:
            self.moneybuf = number
        else:
            newbalance = int(str(self.moneybuf)+str(number))
            if len(str(newbalance)) <= 4:
                self.moneybuf = newbalance
        self.__inputmenu()
        
    def __loadsnames(self):
        if 'name.conf' in os.listdir(self.path):
            name = open(self.path + 'name.conf')
            while True:
                line = name.readline()
                if not line:
                    break
                read = line.split(':')
                if '\n' in read:
                    read.remove('\n')
                self.idnames.append(read)
        
    def __loadscore(self):
        save = open(self.path + 'save.conf')
        while True:
            line = save.readline()
            if not line:
                break
            read = line.split(':')
            if '\n' in read:
                read.remove('\n')
            self.balance.append(int(read[0]))
            self.players.append(read[1])
            self.names.append(read[2])
        save.close()
    
    def __savescore(self):
        if not 'save.conf' in os.listdir(self.path):
            open(self.path + 'save.conf','x').close()
        save = open(self.path + 'save.conf','w')
        for i in range(len(self.balance)):
            save.write(str(self.balance[i]) + ':' + self.players[i] + ':' + self.names[i] + ':\n')
        save.close()
    
    def __control(self,command):
        if self.restore:
            if   command == 12:
                if self.selsected == -1:
                    self.__loadscore()
                    self.restore = False
                    self.__showmenu()
                    self.selsected = -1
                if self.selsected == 0:
                    self.restore = False
                    self.selsected = -1
                    os.remove(self.path + 'save.conf') 
                    self.__showmenu()      
            elif command == 3:
                self.selsected = -1
                self.__showrestore()
            elif command == 7:
                self.selsected = 0
                self.__showrestore()
            elif command == 14:
                self.Loader.setdefaultcontrol()
                self.timer.deinit()
                self.rgbtimer.deinit()
                del self.timer
                del self.rgbtimer
                self.Loader.__showmenu()
        else:
            if self.stage == 1 or self.stage == 4:
                if   command == 0:
                    self.__addnumber(1)
                elif command == 1:
                    self.__addnumber(2)
                elif command == 2:
                    self.__addnumber(3)
                elif command == 4:
                    self.__addnumber(4)
                elif command == 5:
                    self.__addnumber(5)
                elif command == 6:
                    self.__addnumber(6)
                elif command == 8:
                    self.__addnumber(7)
                elif command == 9:
                    self.__addnumber(8)
                elif command == 10:
                    self.__addnumber(9)
                elif command == 13:
                    self.__addnumber(0)
                elif command == 16:
                    self.__addnumber(100)
                elif command == 17:
                    self.__addnumber(200)
                elif command == 14:
                    if len(str(self.moneybuf)) == 1:
                        self.moneybuf = 0
                    else:
                        self.moneybuf = int(str(self.moneybuf)[:-1])
                    self.__inputmenu()
                elif command == 15:
                    self.stage = 0
                    self.rgbmode = 0
                    self.Loader.beep([[500,100]])
                    self.Loader.setrgb(self.r,self.g,self.b)
                    self.__showmenu()
                elif command == 12:
                    self.Loader.beep([[750,100]])
                    if self.stage == 1:
                        if not self.moneybuf == 0:
                            self.stage = 2
                            self.rgbmode = 3
                            self.r, self.g, self.b = 0.05, 0, 0.4
                            self.Loader.setrgb(self.r,self.g,self.b)
                            self.__transfermenu()
                    if self.stage == 4:
                        if not self.moneybuf == 0 or not self.moneybufsend == 0:
                            self.stage = 5
                            self.__operationmenu()
            if self.stage == -1:
                if command == 12:
                    self.Loader.beep([[400,300],[20,100],[300,300]])
                    self.Loader.setdefaultcontrol()
                    self.timer.deinit()
                    self.rgbtimer.deinit()
                    del self.timer
                    del self.rgbtimer
                    self.Loader.__showmenu()
                if command == 14:
                    self.rgbmode = 0
                    self.Loader.setrgb(self.r,self.g,self.b)
                    self.__showmenu()
                    self.stage = 0
            elif self.stage == 0:
                if len(self.players) > 1:
                    if command == 3:
                        self.Loader.beep([[1000,100]])
                        self.rgbmode = -1
                        self.Loader.setrgb(0,0.6,0)
                        self.stage = 4
                        self.m = False
                        self.moneybuf = 0
                        self.moneybufsend = 0
                        self.__inputmenu()
                    elif command == 7:
                        self.Loader.beep([[1000,100]])
                        self.rgbmode = -1
                        self.Loader.setrgb(0,0.6,0)
                        self.stage = 4
                        self.m = True
                        self.moneybuf = 0
                        self.moneybufsend = 0
                        self.__inputmenu()
                    elif command == 12:
                        self.Loader.beep([[1000,100]])
                        self.buffcard = ''
                        self.rgbmode = -1
                        self.Loader.setrgb(0,0,0.6)
                        self.stage = 1
                        self.moneybuf = 0
                        self.moneybufsend = 0
                        self.__inputmenu()
                if command == 14:
                    self.rgbmode = -1
                    self.Loader.setrgb(0.4,0,0)
                    self.stage = -1
                    self.Loader.Display.fill(0)
                    self.Loader.Display.ctext('----------------', 0, 11, 1)
                    if self.Loader.lang:
                        self.Loader.Display.ctext('|  EXIT | BACK |', 0, 21, 1)
                        self.Loader.Display.ctext('| PLAY/*| EQ/# |', 0, 31, 1)
                    else:
                        self.Loader.Display.ctext('ВЫЙТИ |ВЕРНУТЬСЯ', 0, 21, 1)
                        self.Loader.Display.ctext('PLAY/*|   EQ/#', 0, 31, 1)
                    self.Loader.Display.ctext('----------------', 0, 41, 1)
                    self.Loader.Display.show()
            elif self.stage == 2 or self.stage == 3 or self.stage == 5:
                if command == 15:
                    self.r, self.g, self.b = 0, 0.05, 0.4
                    self.stage = 0
                    self.rgbmode = 0
                    self.Loader.setrgb(self.r,self.g,self.b)
                    self.Loader.beep([[500,100]])
                    self.__showmenu()
            elif self.stage == 4:
                if command == 3:
                        if self.m:
                            self.moneybufsend -= self.moneybuf
                        else:
                            self.moneybufsend += self.moneybuf
                        self.moneybuf = 0
                        self.m = False
                        self.__inputmenu()
                if command == 7:
                        if self.m:
                            self.moneybufsend -= self.moneybuf
                        else:
                            self.moneybufsend += self.moneybuf
                        self.moneybuf = 0
                        self.m = True
                        self.__inputmenu()