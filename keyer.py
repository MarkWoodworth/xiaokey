# keyer.py
#
# (C) Copyright 2022 Mark Woodworth AC9YW All Rights Reserved
#
#               seed xiao rp2040
#
#                 +---USB C--+  
#  paddle dit in  D0        5V
#  paddle dah in  D1       GND
#      buzzer pwm D2       3v3
#         key out D3       D10 in  button 1
#     i2c sda     D4        D9 in  button 2 
#     i2c scl     D5        D8 in  button 3
#          tx     D6        D7     rx
#                 +----------+

# imports
import time
import board
import pwmio
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import usb_cdc
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# configuration
WPM = 15
SIDETONE = True
SIDEFREQ = 880
KEYBOARD = False

# messages
MSG1 = "AC9YW"
MSG2 = "CQ CQ CQ DE AC9YW AC9YW AC9YW K"
MSG3 = "73"


# setup leds (false = on)
pixel = neopixel.NeoPixel(board.NEOPIXEL,1)
red   = DigitalInOut(board.LED_RED)
red.direction = Direction.OUTPUT
red.value = True
green = DigitalInOut(board.LED_GREEN)
green.direction = Direction.OUTPUT
green.value = True
blue  = DigitalInOut(board.LED_BLUE)
blue.direction = Direction.OUTPUT
blue.value = True

# setup buzzer (set duty cycle to ON to sound)
buzzer = pwmio.PWMOut(board.D2,variable_frequency=True)
buzzer.frequency = SIDEFREQ
OFF = 0
ON = 2**15

# setup keyer output
key = DigitalInOut(board.D3) ;
key.direction = Direction.OUTPUT

# setup paddle inputs
dit_key = DigitalInOut(board.D1)
dit_key.direction = Direction.INPUT
dit_key.pull = Pull.UP
dah_key = DigitalInOut(board.D0)
dah_key.direction = Direction.INPUT
dah_key.pull = Pull.UP

# setup push buttons
b1 = DigitalInOut(board.D10)
b1.direction = Direction.INPUT
b1.pull = Pull.UP
b2 = DigitalInOut(board.D9)
b2.direction = Direction.INPUT
b2.pull = Pull.UP
b3 = DigitalInOut(board.D8)
b3.direction = Direction.INPUT
b3.pull = Pull.UP

# setup usb serial
serial = usb_cdc.data

# setup keyboard output
time.sleep(1)  
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# setup encode and decode
encodings = {}
def encode(char):
    global encodings
    if char in encodings:
        return encodings[char]
    elif char.lower() in encodings:
        return encodings[char.lower()]
    else:
        return ''

decodings = {}
def decode(char):
    global decodings
    if char in decodings:
        return decodings[char]
    else:
        return '('+char+'?)'

def morse(pattern,letter):
    decodings[pattern] = letter
    encodings[letter ] = pattern
    
morse('.-'   ,'a')
morse('-...' ,'b')
morse('-.-.' ,'c')
morse('-..'  ,'d')
morse('.'    ,'e')
morse('..-.' ,'f')
morse('--.'  ,'g')
morse('....' ,'h')
morse('..'   ,'i')
morse('.---' ,'j')
morse('-.-'  ,'k')
morse('.-..' ,'l')
morse('--'   ,'m')
morse('-.'   ,'n')
morse('---'  ,'o')
morse('.--.' ,'p')
morse('--.-' ,'q')
morse('.-.'  ,'r')
morse('...'  ,'s')
morse('-'    ,'t')
morse('..-'  ,'u')
morse('...-' ,'v')
morse('.--'  ,'w')
morse('-..-' ,'x')
morse('-.--' ,'y')
morse('--..' ,'z')
              
morse('.----','1')
morse('..---','2')
morse('...--','3')
morse('....-','4')
morse('.....','5')
morse('-....','6')
morse('--...','7')
morse('---..','8')
morse('----.','9')
morse('-----','0')

morse('...---...','!')

# key down and up
def cw(on):
    if on:
        key.value = True
        if SIDETONE:
           buzzer.duty_cycle = ON
        pixel.fill((0,0,30))
    else:
        key.value = False
        buzzer.duty_cycle = OFF
        pixel.fill((0,0,0))
        
# timing
def dit_time():
    global WPM
    PARIS = 50 
    return 60.0 / WPM / PARIS

# send to computer
def send(c):
#   print(c,end='')
    if serial.connected:
       serial.write(str.encode(c))
    if KEYBOARD:
        keyboard_layout.write(c)
        
# transmit pattern
def play(pattern):
    for sound in pattern:
        if sound == '.':
            cw(True)
            time.sleep(dit_time())
            cw(False)
            time.sleep(dit_time())
        elif sound == '-':
            cw(True)
            time.sleep(3*dit_time())
            cw(False)
            time.sleep(dit_time())
        elif sound == ' ':
            time.sleep(4*dit_time())
    time.sleep(2*dit_time())

# send and play message
def xmit(message):
    for letter in message:
        send(letter)
        play(encode(letter))
    play(' ')
    
# send and play memories on button presses
def buttons():
    global b1, b2, b3
    if not b1.value:
        xmit(MSG1)
    if not b2.value:
        xmit(MSG2)
    if not b3.value:
        xmit(MSG3)
        
# receive, send, and play keystrokes from computer
def serials():
    if serial.connected:
        if serial.in_waiting > 0:
            letter = serial.read().decode('utf-8')
            send(letter)
            play(encode(letter))

# decode iambic b paddles
class Iambic:
    def __init__(self,dit_key,dah_key):
        self.dit_key = dit_key
        self.dah_key = dah_key
        self.dit = False
        self.dah = False
        self.SPACE    = 0
        self.DIT      = 1
        self.DIT_WAIT = 2
        self.DAH      = 3
        self.DAH_WAIT = 4
        self.state = self.SPACE
        self.in_char = False
        self.in_word = False
        self.start = 0
        self.char = ''
    def hack(self):
        self.start = time.monotonic()
    def elapsed(self):
        return time.monotonic() - self.start
    def set_state(self, new_state):
        self.hack()
        self.state = new_state
    def latch_paddles(self):
        if not self.dit_key.value:
            self.dit = True
        if not self.dah_key.value:
            self.dah = True
    def start_dit(self):
        self.dit = False
        self.dah = False
        self.in_char = True
        self.in_word = True
        self.char += "."
        cw(True)
        self.set_state(self.DIT)
    def start_dah(self):
        self.dit = False
        self.dah = False
        self.in_char = True
        self.in_word = True
        self.char += "-"
        cw(True)
        self.set_state(self.DAH)        
    def cycle(self):
        self.latch_paddles()
        if self.state == self.SPACE:
            if self.dit:
                self.start_dit()
            elif self.dah:
                self.start_dah()
            elif self.in_char and self.elapsed()>2*dit_time():
                self.in_char = False
                send(decode(self.char))
                self.char = ""
            elif self.in_word and self.elapsed()>6*dit_time():
                self.in_word = False
                send(" ") 
        elif self.state == self.DIT:
            if self.elapsed() > dit_time():
                cw(False)
                self.dit = False
                self.set_state(self.DIT_WAIT)
        elif self.state == self.DIT_WAIT:
            if self.elapsed() > dit_time():
                if self.dah:
                    self.start_dah()
                elif self.dit:
                    self.start_dit()
                else:
                    self.set_state(self.SPACE)
        elif self.state == self.DAH:
            if self.elapsed() > 3*dit_time():
                cw(False)
                self.dah = False
                self.set_state(self.DAH_WAIT)
        elif self.state == self.DAH_WAIT:
            if self.elapsed() > dit_time():
                if self.dit:
                    self.start_dit()
                elif self.dah:
                    self.start_dah()
                else:
                    self.set_state(self.SPACE)              

# paddle instance
iambic = Iambic(dit_key,dah_key)

# turn on green run light
green.value = False

# run
while True:
    buttons()
    serials()
    iambic.cycle()

            