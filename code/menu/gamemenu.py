class GameMenu:
    def __init__(self,loader):
        loader.ControlCallback = self.__control
        self.Loader = loader
        self.selsectors = len(self.Loader.games)-1
        self.selsected = -1
        self.color = 1
        self.y = 0
        self.__showmenu()
        
    def __showmenu(self):
        self.Loader.Display.fill(0)
        if self.Loader.lang:
            self.Loader.Display.ctext('CHOOSE A GAME:', 0, self.y + 1, 1)
        else:
            self.Loader.Display.ctext('ВЫБЕРИТЕ ИГРУ:', 0, self.y + 1, 1)
        
        for count, settings in enumerate(self.Loader.games):
            if self.selsected == count: self.color = not self.color
            self.Loader.Display.fill_rect(0, self.y + 10*(count+1), 128, 9, not self.color)
            self.Loader.Display.ctext(settings, 0, self.y + 10*(count+1)+1, self.color)
            self.color = 1 
            
        self.Loader.Display.show()
        
    def __control(self,command):
        if command == 12:
            if not self.selsected == -1:
                from temppaths import TempPaths
                TempPaths.start(self.Loader.games[self.selsected],self.Loader)
                del TempPaths
        if command == 3 and self.selsected > 0:
            self.selsected -= 1
            if self.selsected > 3:
                self.y +=10
            self.__showmenu()
        if command == 7 and not self.selsected == self.selsectors:
            self.selsected += 1
            if self.selsected > 4:
                self.y -=10
            self.__showmenu()
        if command == 14:
            self.Loader.setdefaultcontrol()
            self.Loader.__showmenu()