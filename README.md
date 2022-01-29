# xiaoKey

Even yet another electronic iambic keyer.

A minimalist device based on:

* a Seeed [Xiao](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html) RP2040 controller board
* [CircuitPython](https://circuitpython.org/) programs and libraries

The `code` directory has the files that get put on the Seeed Xiao device.

The `pcb`directory has the Eagle schematics for a possible carrier board with connectors.

## Features

* Operates as an iambic type B Morse code keyer with a 3.5mm stereo jack
* Has a configurable side tone through an on-board piezo buzzer
* Has an open-collector output to a 2.5mm mono jack
* Appears as two COM ports:
  * One for code installation and configuration
  * A second port that outputs the keyed characters, and transmits Morse code for characters typed into the COM port
* Has three buttons to trigger canned messages

