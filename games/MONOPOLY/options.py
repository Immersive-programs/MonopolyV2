import os
class Options:
    def __init__(self,loader):
        loader.ControlCallback = self.__control
        self.Loader = loader
        self.selsectors = 1
        self.selsected = -1
        self.color = 1
        self.y = 0
        self.startbalance = 1500
        self.edit = False
        self.autosave = True
        self.path = '/games/MONOPOLY/'
        self.__loadsettings()
        self.__showmenu()
        
    def __showmenu(self):
        self.Loader.Display.fill(0)
        if self.selsected == 0: self.color = not self.color
        self.Loader.Display.fill_rect(0,  self.y + 10, 128, 19, not self.color)
        if self.Loader.lang:
            self.Loader.Display.ctext('MONOPOLY OPTIONS', 0, 1, 1)
            self.Loader.Display.ctext('BASIC CAPITAL:', 0, self.y + 11, self.color)
            money = str(self.startbalance)+'$'
            self.Loader.Display.ctext(money, (16-len(money))*8, self.y + 21, self.color)
            if self.edit:
                self.Loader.Display.ctext('NEW:', 0, self.y + 21, self.color)
        else:
            self.Loader.Display.ctext('ОПЦИИ  МОНОПОЛИИ', 0, 1, 1)
            self.Loader.Display.ctext('БАЗОВЫЙ КАПИТАЛ:', 0, self.y + 11, self.color)
            money = str(self.startbalance)+'$'
            self.Loader.Display.ctext(money, (16-len(money))*8, self.y + 21, self.color)
            if self.edit:
                self.Loader.Display.ctext('НОВЫЙ:', 0, self.y + 21, self.color)
        self.color = 1
        if self.selsected == 1: self.color = not self.color
        self.Loader.Display.fill_rect(0, self.y + 30, 128, 9, not self.color)
        self.Loader.Display.ctext('AUTOSAVE: '+str(self.autosave), 0, self.y + 31, self.color)
        self.color = 1
        self.Loader.Display.show()
    
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
    
    def __savesettings(self):
        settings = open(self.path + 'options.conf','w')
        settings.write('money:' + str(self.startbalance) + ':\n')
        settings.write('autosave:' + str(self.autosave) + ':\n')
        settings.close()
        
    def __addnumber(self,number):
        if self.startbalance == 0:
            self.startbalance = number
        else:
            newbalance = int(str(self.startbalance)+str(number))
            if len(str(newbalance)) <= 4:
                self.startbalance = newbalance
        self.__showmenu()
        
    def __control(self,command):
        if self.edit:
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
        else:
            if command == 3 and self.selsected > 0:
                self.selsected -= 1
                if self.selsected > 3:
                    self.y +=10
                self.__showmenu()
            elif command == 7 and not self.selsected == self.selsectors:
                self.selsected += 1
                if self.selsected > 4:
                    self.y -=10
                self.__showmenu()
        if command == 12:
            if self.selsected == 0:
                if self.edit:
                    self.edit = False
                    self.__savesettings()
                else:
                    self.edit = True
                self.__showmenu()
            if self.selsected == 1:
                self.autosave = not self.autosave
                self.__savesettings()
                self.__showmenu()
        elif command == 14:
            if not self.edit:
                self.Loader.setcontrolmenu()
            else:
                if len(str(self.startbalance)) == 1:
                    self.startbalance = 0
                else:
                    self.startbalance = int(str(self.startbalance)[:-1])
                self.__showmenu()                