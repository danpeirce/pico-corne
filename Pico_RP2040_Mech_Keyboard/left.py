# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# RaspberryPi Pico RP2040 Mechanical Keyboard

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

print("---Pico Pad Keyboard---")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# list of pins to use 
pins = (
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15,`
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19,
    board.GP20,
)

MEDIA = 1
KEY = 2

keymap = {
    (0): (KEY, [Keycode.TAB]),
    (1): (KEY, [Keycode.Q]),
    (2): (KEY, [Keycode.W]),
    (3): (KEY, [Keycode.E]),
    (4): (KEY, [Keycode.R]),
    (5): (KEY, [Keycode, T]),
    
    (6): (KEY, [Keycode.ALT]),
    (7): (KEY, [Keycode.A]),
    (8): (KEY, [Keycode.S]),
    (9): (KEY, [Keycode.D]),
    (10): (KEY, [Keycode.F]),
    (11): (KEY, [Keycode.G]),  
    
    (12): (KEY, [Keycode.LEFT_SHIFT]),
    (13): (KEY, [Keycode.Z]),
    (14): (KEY, [Keycode.X]),
    (15): (KEY, [Keycode.C]),
    (16): (KEY, [Keycode.V]),
    (17): (KEY, [Keycode.B]),
    
    (18): (KEY, [Keycode.CONTROL]),
    (19): (KEY, [Keycode.ENTER]),
    (20): (KEY, [Keycode.J]),

}

switches = []
for i in range(len(pins)):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)


switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while True:
    for button in range(21):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                    else:
                        cc.send(keymap[button][1])
                except ValueError:  # deals w six key limit
                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])

                except ValueError:
                    pass
                switch_state[button] = 0

    time.sleep(0.01)  # debounce
