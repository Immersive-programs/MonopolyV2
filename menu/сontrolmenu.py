class ControlMenu:
    def __init__(self,loader):
        loader.ControlCallback = self.__control
        self.Loader = loader
        self.y = 0
        self.__showmenu()
        
    def __showmenu(self):
        self.Loader.Display.fill(0)
        if self.Loader.lang:
            self.Loader.Display.ctext('A/+UP B/-DOWN'   , 0, self.y + 1 , 1)
            self.Loader.Display.ctext('CONTROLLING:'    , 0, self.y + 11, 1)
            self.Loader.Display.ctext('# = EQ   >  BACK', 0, self.y + 21, 1)
            self.Loader.Display.ctext('* =PLAY>TRANSFER', 0, self.y + 31, 1)
            self.Loader.Display.ctext('A = +  >  APPEND', 0, self.y + 41, 1)
            self.Loader.Display.ctext('B = -  >  REDUCE', 0, self.y + 51, 1)
            self.Loader.Display.ctext('C = NEXT  > NEXT', 0, self.y + 61, 1)
            self.Loader.Display.ctext('D = PREV  > EXIT', 0, self.y + 71, 1)
            self.Loader.Display.ctext('NUMBERS > VALUES', 0, self.y + 81, 1)
        else:
            self.Loader.Display.ctext('A/+ВВЕРХ B/-ВНИЗ', 0, self.y + 1 , 1)
            self.Loader.Display.ctext('УПРАВЛЕНИЕ:'     , 0, self.y + 11, 1)
            self.Loader.Display.ctext('# = EQ >ОТМЕНИТЬ', 0, self.y + 21, 1)
            self.Loader.Display.ctext('* = PLAY>ПЕРЕВОД', 0, self.y + 31, 1)
            self.Loader.Display.ctext('A = + > ДОБАВИТЬ', 0, self.y + 41, 1)
            self.Loader.Display.ctext('B = - >  УБАВИТЬ', 0, self.y + 51, 1)
            self.Loader.Display.ctext('C = NEXT> ВПЕРЁД', 0, self.y + 61, 1)
            self.Loader.Display.ctext('D = PREV > ВЫЙТИ', 0, self.y + 71, 1)
            self.Loader.Display.ctext('ЦИФРЫ > ЗНАЧЕНИЯ', 0, self.y + 81, 1)
        self.Loader.Display.show()
        
    def __control(self,command):
        if command == 3 and not self.y == 0:
            self.y += 10
            self.__showmenu()
        if command == 7 and not self.y == -30:
            self.y -= 10
            self.__showmenu()
        if command == 14:
            self.Loader.setdefaultcontrol()
            self.Loader.__showmenu()