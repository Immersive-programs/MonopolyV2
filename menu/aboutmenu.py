class AboutMenu:
    def __init__(self,loader):
        loader.ControlCallback = self.__control
        self.Loader = loader
        self.__showmenu()
        
    def __showmenu(self):
        self.Loader.Display.fill(0)
        if self.Loader.lang:
            self.Loader.Display.ctext('WE: Immersive', 0, 1, 1)
            self.Loader.Display.ctext('    Electronics', 0, 11, 1)
            self.Loader.Display.ctext('AUTHOR: Nikita', 0, 21, 1)
            self.Loader.Display.ctext('PROGTAMMER:', 0, 31, 1)
            self.Loader.Display.ctext('        Denis', 0, 41, 1)
            self.Loader.Display.ctext('EXIT: # OR EQ', 0, 51, 1)
        else:
            self.Loader.Display.ctext('МЫ: Immersive', 0, 1, 1)
            self.Loader.Display.ctext('    Electronics', 0, 11, 1)
            self.Loader.Display.ctext('АВТОР: НИКИТА', 0, 21, 1)
            self.Loader.Display.ctext('ПРОГРАММИСТ:', 0, 31, 1)
            self.Loader.Display.ctext('       ДЕНИС', 0, 41, 1)
            self.Loader.Display.ctext('ВЫЙТИ: # ИЛИ EQ', 0, 51, 1)
        self.Loader.Display.show()
        
    def __control(self,command):
        if command == 14:
            self.Loader.setdefaultcontrol()
            self.Loader.__showmenu()
