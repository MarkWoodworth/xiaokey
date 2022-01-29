# xiaoKey

Even yet another electronic iambic keyer. 

It is a minimalist device based on:

* an inexpensive Seeed [Xiao](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html) RP2040 controller board
* [CircuitPython](https://circuitpython.org/) programs and libraries

The `code` directory has the files to be installed on the *Seeed Xiao* device.

The `pcb`directory has the Eagle schematics for a possible carrier board with connectors.

## Features

* Operates as an [iambic type B](http://wb9kzy.com/modeab.pdf) Morse code keyer with a 3.5mm stereo jack to connect to a dual-paddle telegraph key
* Has a configurable side tone transmitted through an on-board piezo buzzer
* Has an open-collector output to a 2.5mm mono jack, which should be able to key most radios
* When connected to a PC over USB appears as two COM ports:
  * One is the *CircuitPython* REPL and console
  * A second port that shows the characters being transmitted, and also transmits Morse code for characters typed into the COM port
* Has three buttons to trigger canned messages
* Speed, sidetone, keyboard operation, and canned messages are configured by editing the code.py file on the *CIRCUITPY:* device
* Can act as a USB keyboard, where keyed characters are also sent to the computer as keystrokes.  

## Software Installation

1. Get the most recent UF2 file for *CircuitPython* on the *Xiao RP2040* [here](https://circuitpython.org/board/seeeduino_xiao_rp2040/).

2. Connect the *Xiao* to a computer using a USB C cable.

3. Follow the instructions for loading *CircuitPython* [here](https://wiki.seeedstudio.com/XIAO-RP2040-with-CircuitPython/).  Basically, you put the *Xiao* in boot loader mode by long-pressing the _BOOT_ button and then copy the UF2 file to the *Xiao* which appears as `RP1-RP2`. The *Xiao* will now reboot itself.

4. Copy `boot.py` and `code.py` to the Xiao, which now appears as drive `CIRCUITPY` on the computer.

5. Copy the required library files (in the repository `lib` directory) to the `lib` directory on the attached *Xiao*.  The files are:

   * `neopixel.mpy`
   * The directory `adafruit_hid`

   The most recent versions of these files can be found [here](https://circuitpython.org/libraries).

6. Press the *REBOOT* button on the Xiao.

## Configuration

The device is configured by editing the source file `code.py` on the *Xiao* device.  The configuration parameters appear near the top.

```python
# user configuration
WPM = 15
SIDETONE = True
SIDEFREQ = 880
KEYBOARD = False

# user messages
MSG1 = "AC9YW"
MSG2 = "CQ CQ CQ DE AC9YW AC9YW AC9YW K"
MSG3 = "73"
```

## Pinout

```
                 +---USB C--+  
  paddle dit in  D0        5V
  paddle dah in  D1       GND
      buzzer pwm D2       3v3
         key out D3       D10 in  button 1
     i2c sda     D4        D9 in  button 2 
     i2c scl     D5        D8 in  button 3
          tx     D6        D7     rx
                 +----------+
```

## Schematic

![schematic](./img/xiaokey.png)

## Assembly

:construction: This part is waiting for the 1.5 inch square boards to appear from the wonderful [OSH Park](https://oshpark.com/).

<img src="./img/top.png" alt="center" style="zoom:20%;" />



## References

The iambic keyer state machine owes a great debt to the [1keyer](https://hackaday.io/project/18841-1keyer/log/50103-state-machine-of-the-union) project by Mark VandeWettering, and the [PIK](https://owenduffy.net/module/pik/pik.htm) project by Owen Duffy.

Larry Kuck (WB7C) has very helpful resources at [Morse Code for the Radio Amateur](https://www.morsecodeclassnet.com/)

