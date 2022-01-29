# xiaoKey

Even yet another electronic iambic keyer.

It is a minimalist device based on:

* a Seeed [Xiao](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html) RP2040 controller board
* [CircuitPython](https://circuitpython.org/) programs and libraries

The `code` directory has the files to be installed on the Seeed Xiao device.

The `pcb`directory has the Eagle schematics for a possible carrier board with connectors.

## Features

* Operates as an iambic type B Morse code keyer with a 3.5mm stereo jack
* Has a configurable side tone transmitted through an on-board piezo buzzer
* Has an open-collector output to a 2.5mm mono jack
* When connected to a PC over USB appears as two COM ports:
  * One for code installation and configuration
  * A second port that shows the characters being transmitted, and also transmits Morse code for characters typed into the COM port
* Has three buttons to trigger canned messages
* Can act as a USB keyboard, where keyed characters are also sent to the PC a keystrokes.  

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



## References

The iambic keyer state machine owes a great debt to the [1keyer](https://hackaday.io/project/18841-1keyer/log/50103-state-machine-of-the-union) project by Mark VandeWettering.
