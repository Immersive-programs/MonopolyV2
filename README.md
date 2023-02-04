# Monopoly Terminal V2

# English:

<details>
<summary> <b></b> (<i>click to expand</i>)</summary>

## The project of an electronic terminal for the game Monopoly

Video on YouTube:

### Terminal Features:
- Support for RFID cards;
- 128x64 display;
- IR Contactless input;
- Keyboard input;
- Sound indication;
- Light indication;
- Adding your own games.

### Component base:
- Raspberry Pi Pico Controller;
- 12864 LCD DISPLAY(128x64,SPI);
- Matrix keyboard(4x4);
- RFID PN532 Wireless module;
- RFID cards;
- Three-color LED(RGB);
- IR(NEC) Signal receiver;
- IR remote control "Car MP3 TZT";
- Passive buzzer 3.3V;
- Step-down module 3.3V.

<details>
<summary> <b>Connecting components</b> (<i>click to expand</i>)</summary>

- Display:
  Contact name| I/O port
  --- |---
  RSE | 1
  SCL | 2
  SI | 3
  RS | 4
  CS | 5

- PN532:
  Contact name| I/O port
  --- |---
  SCK|6
  MOSI | 7
  MISO | 8
  SS | 9

- Matrix keyboard:
  Contact name| I/O port
  --- |---
  Pin 1 IN | 10
  Pin 2 IN | 11
  Pin 3 IN | 12
  Pin 4 IN | 13
  Pin 5 OUT | 14
  Pin 6 OUT | 15
  Pin 7 OUT | 17
  Pin 8 OUT | 16

- IR:
  Contact name| I/O port
  --- | ---
  DATA | 28

- Buzzer:
  Contact name| I/O port
  --- | ---
  Power | 0
  
    <details>
    <summary> <b>Scheme</b> (<i>click to expand</i>)</summary>
  
    ![f](https://user-images.githubusercontent.com/80697141/216764820-6227f769-2010-4c46-a848-6ea7723754f7.png)
    </details>
  </details>
  
  <details>
  <summary> <b>Adding your game</b> (<i>click to expand</i>)</summary>
  
 #### 
 1. Create a new directory with the name of your game in the <b><i>games</i></b> folder;
 2. In this directory, create a file <b><i>run.py</i></b> ;
 3. Copy the code below into <b><i>run.py</i></b>:
 ```Python
 class Run:
    def __init__(self,loader):
      loader.ControlCallback = self.__control
      self.Loader = loader
      #Your game initialization code
      ''' Example:'''
      self.Loader.Display.fill(0)
      self.Loader.Display.ctext('Hello!', 0, 1, 1)  
      self.Loader.Display.show()
    
    def __control(self,command):
      if command == 14:
        self.Loader.setdefaultcontrol()
        self.Loader.__showmenu()
      #Your command processing code
 ```
 4. You can start implementing your idea!
 5. If you need to add settings, create a file <b> <i> options.py </i> </b> in the catalog of your game;
 6. Copy the above code in <b> <i> options.py </i> </b>
 ```Python
  import os
  class Options:
    def __init__(self,loader):
      loader.ControlCallback = self.__control
      self.Loader = loader
      self.path = '/games/<Game Name>/'
      #Your settings initialization code
      ''' Example:'''
      self.Loader.Display.fill(0)
      self.Loader.Display.ctext('SETTINGS!', 0, 1, 1)  
      self.Loader.Display.show()
    
    def __control(self,command):
      if command == 14:
        self.Loader.setdefaultcontrol()
        self.Loader.__showmenu()
      #Your command processing code
 ```
 7. Create the options you need;
 8. After restarting the terminal, play your game will appear in the point and if you have a file <b> <i> options.py </i> </b> a new option with the name of your game will appear in the settings point
</details>
  
### Libraries used:
- Immersive-programs:
  - micropython-buzzer: https://github.com/Immersive-programs/micropython-buzzer
  - micropython-customsymbols: https://github.com/Immersive-programs/micropython-customsymbols
  - micropython-matrixkeyboard: https://github.com/Immersive-programs/micropython-matrixkeyboard
  - micropython-st7565(fork): https://github.com/Immersive-programs/micropython-st7565
- Carglglz: 
  - NFC_PN532: https://github.com/Carglglz/NFC_PN532_SPI
- peterhinch:
  - micropython_ir: https://github.com/peterhinch/micropython_ir
  
### Notes:
- Development was carried out in the Thonny IDE;
- Workability tested on: "MicroPython v1.19.1 on 2022-06-18";
- It is recommended to use Rshell to load the code: https://github.com/dhylands/rshell 

### Creators:
- Author of the ideaa: Nikita
- Code author: Denis
</details>

# Русский:

<details>
<summary> <b></b> (<i>нажмите, чтобы развернуть</i>)</summary>

## Проект электронного терминала для игры Monopoly

Ролик на YouTube:

### Особенности терминала:
- Поддержка RFID карт;
- Дисплей 128x64;
- IR Бесконтактный ввод;
- Клавиатурный ввод;
- Звуковая индикация;
- Световая индикация;
- Добавление своих игр. 

### Компонентная база:
- Контроллер Raspberry Pi Pico;
- 12864 LCD дисплей(128x64,SPI);
- Матричная клавиатура(4x4);
- Беспроводной модуль RFID PN532;
- RFID карты;
- Трёхцветный светодиод(RGB);
- IR(NEC) Приёмник сигнала;
- IR пульт "Car MP3 TZT";
- Пассивный зуммер 3.3V;
- Понижающий модуль 3.3V.

<details>
  <summary> <b>Подключение компонентов</b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
- Дисплей:
  Название контакта| I/O порт
  --- | ---
  RSE | 1
  SCL | 2
  SI | 3
  RS | 4
  CS | 5
  
- PN532:
  Название контакта| I/O порт
  --- | ---
  SCK | 6
  MOSI | 7
  MISO | 8
  SS | 9
  
- Матричная клавиатура:
  Название контакта| I/O порт
  --- | ---
  Pin 1 IN | 10
  Pin 2 IN | 11
  Pin 3 IN | 12
  Pin 4 IN | 13
  Pin 5 OUT | 14
  Pin 6 OUT | 15
  Pin 7 OUT | 17
  Pin 8 OUT | 16
  
- IR:
  Название контакта | I/O порт
  --- | ---
  DATA | 28
 
- Buzzer:
  Название контакта | I/O порт
  --- | ---
  Power | 0
  
  <details>
  <summary> <b>Схема</b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
  ![f](https://user-images.githubusercontent.com/80697141/216764820-6227f769-2010-4c46-a848-6ea7723754f7.png)
  </details>
</details>

<details>
  <summary> <b>Добавления своей игры</b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
 #### 
 1. Создайте новый каталог с именем вашей игры в папке <b><i>games</i></b>;
 2. В этом каталоге создайте файл <b><i>run.py</i></b> ;
 3. Скопируйте ниже приведённый код в <b><i>run.py</i></b>
 ```Python
 class Run:
    def __init__(self,loader):
      loader.ControlCallback = self.__control
      self.Loader = loader
      #Ваш код инициализации игры
      ''' Пример:'''
      self.Loader.Display.fill(0)
      self.Loader.Display.ctext('ЗДРАСТИ!', 0, 1, 1)  
      self.Loader.Display.show()
    
    def __control(self,command):
      if command == 14:
        self.Loader.setdefaultcontrol()
        self.Loader.__showmenu()
      #Ваш код обработки команд
 ```
 4. Можете приступать к реализации вашей идеи!
 5. Если необходимо добавить настройки, создайте файл <b><i>options.py</i></b> в каталоге вашей игры;
 6. Скопируйте ниже приведённый код в <b><i>options.py</i></b>
 ```Python
  import os
  class Options:
    def __init__(self,loader):
      loader.ControlCallback = self.__control
      self.Loader = loader
      self.path = '/games/<Game Name>/'
      #Ваш код инициализации настроек
      ''' Пример:'''
      self.Loader.Display.fill(0)
      self.Loader.Display.ctext('НАСТРОЙКИ!', 0, 1, 1)  
      self.Loader.Display.show()
    
    def __control(self,command):
      if command == 14:
        self.Loader.setdefaultcontrol()
        self.Loader.__showmenu()
      #Ваш код обработки команд
 ```
 7. Создайте необходимые вам опции; 
 8. После перезапуска терминала в пункте играть появится ваша игра и при наличии файла <b><i>options.py</i></b> в пункте настройки появиться новая опция с названием вашей игры(Если невидно листайте ниже)
</details>

### Используемые библиотеки:
- Immersive-programs:
  - micropython-buzzer: https://github.com/Immersive-programs/micropython-buzzer
  - micropython-customsymbols: https://github.com/Immersive-programs/micropython-customsymbols
  - micropython-matrixkeyboard: https://github.com/Immersive-programs/micropython-matrixkeyboard
  - micropython-st7565(fork): https://github.com/Immersive-programs/micropython-st7565
- Carglglz: 
  - NFC_PN532: https://github.com/Carglglz/NFC_PN532_SPI
- peterhinch:
  - micropython_ir: https://github.com/peterhinch/micropython_ir

 ### Примечания:
  - Разработка велась в Thonny IDE V4.0.2;
  - Работоспособность проверена на: "MicroPython v1.19.1 on 2022-06-18";
  - Для загрузки кода рекомендуется использовать Rshell: https://github.com/dhylands/rshell 

 ### Создатели:
 - Автор идеи: Никита
 - Автор кода: Денис
</details>
