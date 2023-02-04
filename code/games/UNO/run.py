class Run:
    def __init__(self,loader):
        self.path = '/games/UNO/'
        loader.ControlCallback = self.__control
        self.Loader = loader
        self.count = 0
        self.stage = 0
        self.selsectors = -1
        self.selsected = 0
        self.color = 1
        self.beinverted = False
        self.inverted = False
        self.scorebuf = 0
        self.scores = []
        self.log = []
        self.created = False
        self.y = 0
        self.ly = 0
        self.Loader.setrgb(0.1, 0.1, 0.1)
        self.Loader.beep([[500,200],[20,50],[800,200],[20,50],[600,200],[20,50],[1100,200]])
        self.__showmenu()
        
    def __unomenu(self):
        self.Loader.Display.fill(0)
        for count, score in enumerate(self.scores):
            if self.selsected == count: self.color = not self.color
            self.Loader.Display.fill_rect(0, self.y + (count+1) * 10, 128, 9, not self.color)
            if self.selsected == count:
                if self.inverted:
                    self.Loader.Display.ctext('         ^', 0, self.y + (count+1) * 10 + 1, self.color)
                else:
                    self.Loader.Display.ctext('         V', 0, self.y + (count+1) * 10 + 1, self.color)
            if self.Loader.lang:
                self.Loader.Display.ctext('PLAYER>' + str(count+1), 0, self.y + (count + 1) * 10 + 1, self.color)
            else:
                self.Loader.Display.ctext('ИГРОК>' + str(count+1), 0, self.y + (count + 1) * 10 + 1, self.color)
            
            self.Loader.Display.ctext(str(self.scores[count]), (17-len(str(self.scores[count]))-1) * 8, self.y + (count+1) * 10 + 1, self.color)
            self.color = 1
            
        self.Loader.Display.fill_rect(0, 0, 128, 9, not self.color)
        if self.Loader.lang:
            self.Loader.Display.ctext('PLAYERS: |SCORES', 0, 1, 1)
        else:
            self.Loader.Display.ctext('ИГРОКИ:  | ОЧКИ', 0, 1, 1)
        
        self.Loader.Display.fill_rect(1,52,126,11,0)
        self.Loader.Display.ctext('>' + str(self.scorebuf), 6, 54, 1)
        self.Loader.Display.rect(1,52,126,11,1)
        self.Loader.Display.rect(0,51,128,13,0)
        self.Loader.Display.show()
        
    def __logmenu(self):
        self.Loader.Display.fill(0)  
        for c in range(6):
            index = len(self.log)-c-self.ly-1
            if index >= 0:
                l = self.log[index]
                if l == [-1,-1,-1,-1,-1]:
                    if self.Loader.lang:
                        self.Loader.Display.ctext('MOVE|PL|SCOR|INV', 0,  1, 1) 
                    else:
                        self.Loader.Display.ctext('ХОД |ИГ|ОЧКИ|ИНВ', 0,  1, 1) 
                else:
                    if c == 0: self.color = not self.color
                    self.Loader.Display.fill_rect(0, c * 10, 128, 9, not self.color)
                    self.Loader.Display.ctext(str(l[0] + 1), 0, c * 10 + 1, self.color)
                    self.Loader.Display.ctext('    :' + str(l[1] + 1), 0, c * 10 + 1, self.color)
                    self.Loader.Display.ctext('       :'+ str(l[2]), 0, c * 10 + 1, self.color)
                    if l[3]:
                        if self.Loader.lang:
                            self.Loader.Display.ctext('            :YES', 0, c * 10 + 1, self.color)
                        else:
                            self.Loader.Display.ctext('            :ДА', 3, c * 10 + 1, self.color)
                    else:
                        if self.Loader.lang:
                            self.Loader.Display.ctext('            :NO', 3, c * 10 + 1, self.color)
                        else:
                            self.Loader.Display.ctext('            :НЕТ', 0, c * 10 + 1, self.color)
                    self.color = 1
        self.Loader.Display.show()
        
    def __showmenu(self):
        self.Loader.Display.fill(0)
        if not self.scorebuf == 0:
            self.Loader.Display.ctext('       '+ str(self.scorebuf), 0, 11, 1)
        if self.Loader.lang:
            self.Loader.Display.ctext('PLAYERS WILL BE', 3, 22, 1)
            self.Loader.Display.ctext('    CREATED', 3, 32, 1)
        else:
            self.Loader.Display.ctext(' ИГРОКОВ БУДЕТ ', 3, 22, 1)
            self.Loader.Display.ctext('    СОЗДАНО', 3, 32, 1)
        self.Loader.Display.ctext('     |>  <|     ', 0, 11, 1)
        self.Loader.Display.line(55, 19, 72, 19, 1)
        self.Loader.Display.show()
        
    def __addnumber(self,number):
        if self.scorebuf == 0:
            self.scorebuf = number
        else:
            newscore = int(str(self.scorebuf)+str(number))
            if self.created:
                if len(str(newscore)) <= 4:
                    self.scorebuf = newscore
            elif len(str(newscore)) <= 2:
                self.scorebuf = newscore
        if self.created:
            self.__unomenu()
        else:
            self.__showmenu()
           
    def __control(self,command):
        if self.stage == 0: 
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
                if len(str(self.scorebuf)) == 1:
                    self.scorebuf = 0
                else:
                    self.scorebuf = int(str(self.scorebuf)[:-1])
                if self.created:
                   self.__unomenu()
                else:
                    self.__showmenu()
                
        if not self.created:
            if   command == 12 and self.scorebuf > 1:
                self.stage = 0
                self.created = True
                for s in range(self.scorebuf):
                    self.scores.append(0)
                self.selsectors = self.scorebuf-1
                self.scorebuf = 0
                self.__unomenu()
            elif command == 15:
                self.Loader.setdefaultcontrol()
                self.Loader.__showmenu()
        else:
            if self.stage == -1:
                if   command == 12:
                    self.Loader.beep([[1000,200],[20,50],[700,200],[20,50],[500,200]])
                    self.Loader.setdefaultcontrol()
                    self.Loader.__showmenu()
                elif command == 14:
                    self.__unomenu()
                    self.stage = 0
            if self.stage == 0:
                if   command == 3:
                    self.inverted = not self.inverted
                    self.__unomenu()
                elif command == 11:
                    self.stage = 1
                    self.ly = 0
                    self.log.append([-1,-1,-1,-1,-1])
                    self.__logmenu()
                elif command == 12:
                    self.scores[self.selsected] += self.scorebuf
                    if not self.inverted == self.beinverted:
                        self.beinverted = self.inverted
                        self.log.append([self.count,self.selsected,self.scorebuf,True,self.y])
                    else:
                        self.log.append([self.count,self.selsected,self.scorebuf,False,self.y])
                        
                    if len(self.log) > 255:
                        self.log.pop(0)
                        
                    self.scorebuf = 0
                                  
                    if self.inverted:
                        if not self.selsected == 0:
                            self.selsected -= 1
                            if self.selsected > 2:
                                self.y += 10
                        else:
                            self.selsected = self.selsectors
                            if self.selsected > 2:
                                self.y = 10 * (self.selsected-3) *-1
                    else:
                        if not self.selsected == self.selsectors:
                            self.selsected += 1
                            if self.selsected > 3:
                                self.y -= 10
                        else:
                            self.selsected = 0
                            self.y = 0
                            
                    self.count += 1         
                    self.__unomenu()
                elif command == 15:
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
            if self.stage == 1:
                if   command == 3 and not self.ly == 0:
                    self.ly -=1
                    self.__logmenu()
                elif command == 7 and not self.ly == len(self.log)-1:
                    self.ly +=1
                    self.__logmenu()
                elif command == 12:
                    self.log.remove([-1,-1,-1,-1,-1])
                    for c in range(self.ly):
                        l = self.log[len(self.log)-1]
                        self.scores[l[1]] -= l[2]
                        if l[3]:
                            self.beinverted = not self.beinverted
                        self.inverted = self.beinverted  
                        self.count -= 1
                        self.selsected = l[1]
                        self.y = l[4]
                        self.log.remove(l)
                    self.stage = 0
                    self.__unomenu()
                elif command == 15:
                    self.stage = 0
                    self.log.remove([-1,-1,-1,-1,-1])
                    self.__unomenu()