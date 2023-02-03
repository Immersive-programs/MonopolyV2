class SettingsMenu:
    
    def __init__(self,loader):
        loader.ControlCallback = self.__control
        self.Loader = loader
        self.selsectors = 3
        self.selsectors += len(self.Loader.settingsgames)
        self.selsected = -1
        self.color = 1
        self.y = 0
        self.__showmenu()
        
    def __showmenu(self):
        self.Loader.Display.fill(0)  
        if self.Loader.lang:
            self.Loader.Display.ctext('SETTINGS:', 0, 1, 1)
        else:
            self.Loader.Display.ctext('НАСТРОЙКИ:', 0, self.y + 1, 1)
                  
        if self.selsected == 0: self.color = not self.color
        self.Loader.Display.fill_rect(0, self.y + 10, 128, 9, not self.color)
        if self.Loader.lang:
            self.Loader.Display.ctext('INVERT COLOR', 0, self.y + 11, self.color)
        else:
            self.Loader.Display.ctext('ИНВЕРТИВРАТЬЦВЕТ', 0, self.y + 11, self.color)
        self.color = 1
        
        if self.selsected == 1: self.color = not self.color
        self.Loader.Display.fill_rect(0, self.y + 20, 128, 9, not self.color)
        if self.Loader.lang:
            self.Loader.Display.ctext('SOUND:', 0, self.y + 21, self.color)
        else:
            self.Loader.Display.ctext('ЗВУК:', 0, self.y + 21, self.color)
        if self.Loader.sound:
            if self.Loader.lang:
                self.Loader.Display.ctext('ON', 50, self.y + 21, self.color)
            else:
                self.Loader.Display.ctext('ВКЫЛ', 50, self.y + 21, self.color)
        else:
            if self.Loader.lang:
                self.Loader.Display.ctext('OFF', 50, self.y + 21, self.color)
            else:
                self.Loader.Display.ctext('ВЫКЛ', 50, self.y + 21, self.color)
        self.color = 1
        
        if self.selsected == 2: self.color = not self.color
        self.Loader.Display.fill_rect(0, self.y + 30, 128, 9, not self.color)
        if self.Loader.lang:
            self.Loader.Display.ctext('LANG: ENGLISH', 0, self.y + 31, self.color)
        else:
            self.Loader.Display.ctext('ЯЗЫК: РУССКИЙ', 0, self.y + 31, self.color)
        self.color = 1
        
        if self.selsected == 3: self.color = not self.color
        self.Loader.Display.fill_rect(0, self.y + 40, 128, 9, not self.color)
        if self.Loader.lang:
            self.Loader.Display.ctext('CONTRAST:', 0, self.y + 41, self.color)
        else:
            self.Loader.Display.ctext('КОНТРАСТ:', 0, self.y + 41, self.color)
        self.Loader.Display.rect(71, self.y + 40, 56, 9, self.color)
        self.Loader.Display.fill_rect(73, self.y + 42, self.Loader.contrast-11, 5, self.color)
        if self.Loader.contrast > 37:
            self.Loader.Display.line(98,43,98,45,not self.color)
        else:
            self.Loader.Display.line(98,43,98,45,self.color)
        self.color = 1
  
        for count, settings in enumerate(self.Loader.settingsgames):
            count+=4
            if self.selsected == count: self.color = not self.color
            self.Loader.Display.fill_rect(0, self.y + 10*(count+1), 128, 9, not self.color)
            self.Loader.Display.ctext(settings, 0, self.y + 10*(count+1)+1, self.color)
            self.color = 1  
        self.Loader.Display.show()
        
    def __savesettings(self):
        settings = open('settings.conf','w')
        settings.write('invert:' + str(self.Loader.invert) + '\n')
        settings.write('sound:' + str(self.Loader.sound) + '\n')
        settings.write('lang:' + str(self.Loader.lang) + '\n')
        settings.write('contrast:' + str(self.Loader.contrast) + '\n')
        settings.close()
        
    def __control(self,command):
        if command == 12:
            if   self.selsected == 0:
                self.Loader.Display.reverse()
                self.Loader.invert = not self.Loader.invert
                self.__savesettings()
            elif self.selsected == 1:
                self.Loader.sound = not self.Loader.sound
                self.Loader.Beeper.isenabled = self.Loader.sound
                if self.Loader.sound:
                    self.Loader.beep([[700,100],[1100,100]])
                self.__showmenu()
                self.__savesettings()
            elif self.selsected == 2:
                self.Loader.lang = not self.Loader.lang
                self.__savesettings()
                import machine
                machine.reset()
            elif self.selsected > 3:
                from temppaths import TempPaths
                TempPaths.start(self.Loader.games[self.selsected-4]+'o',self.Loader)
                del TempPaths
        elif command == 11 and self.selsected == 3:
            if not self.Loader.contrast == 63:
                self.Loader.contrast += 1
                self.Loader.Display.set_contrast(self.Loader.contrast)
                self.__showmenu()
                self.__savesettings()
        elif command == 15 and self.selsected == 3:
            if not self.Loader.contrast == 11: 
                self.Loader.contrast -= 1
                self.Loader.Display.set_contrast(self.Loader.contrast)
                self.__showmenu()
                self.__savesettings()   
        elif command == 3 and self.selsected > 0:
            self.selsected -= 1
            if self.selsected > 4:
                self.y +=10
            self.__showmenu()
        elif command == 7 and not self.selsected == self.selsectors:
            self.selsected += 1
            if self.selsected > 5:
                self.y -=10
            self.__showmenu()
        elif command == 14:
            self.Loader.setdefaultcontrol()
            self.Loader.__showmenu()