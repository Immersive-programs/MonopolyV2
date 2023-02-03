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

# Сreated by Immersive-programs:
#   github: https://github.com/Immersive-programs/micropython-customsymbols
class CustomSymbols:
    """Отображает неподдерживаемые символы"""
    __chars = {}
    __symbols = ""
    
    def ctext(self, string, x, y, col):
        """Отображает на дисплее символы"""
        out = ""
        for count, char in enumerate(string):            
            if char in CustomSymbols.__symbols:
                CustomSymbols.__chars[char].draw(self,x,y,count,col)
                out += ' '
            else:
                out += char
        self.text(out, x, y, col)
    
    def loadallsymbols(self):
        """загружает в память все пользовательские символы"""
        import os
        for name in os.listdir('symbols'):
            symbol = str(name.replace('.py',''), "utf-8")
            self.loadsymbol(symbol)
        del os
    
    def loadsymbols(self,string):
        """загружает в память определённые пользовательские символы"""
        for char in string:
            self.loadsymbol(char)
    
    def loadsymbol(self, char):
        """загружает в память один определенный символ"""
        if not char in CustomSymbols.__symbols:
            try:
                CustomSymbols.__chars[char] = __import__(char).char
                CustomSymbols.__symbols += char
            except:
                print("not found:"+char)
