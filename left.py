# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# RaspberryPi Pico RP2040 Mechanical Keyboard
# Modified by Daniel Peirce B.Sc. 2024 - leftside pico-corne with two layers

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

print("---Leftside Pico-Corne---")

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
    board.GP15,
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19,
    board.GP20,
)

MEDIA = 1
KEY = 2
OTHER = 3

keymap = {
    (0): (KEY, [Keycode.TAB], [Keycode.ESCAPE]),
    (1): (KEY, [Keycode.Q], [Keycode.SIX]),
    (2): (KEY, [Keycode.W], [Keycode.SEVEN]),
    (3): (KEY, [Keycode.E], [Keycode.EIGHT]),
    (4): (KEY, [Keycode.R], [Keycode.NINE]),
    (5): (KEY, [Keycode.T], [Keycode.ZERO]),

    (6): (KEY, [Keycode.ALT], [Keycode.ALT]),
    (7): (KEY, [Keycode.A], [Keycode.ONE]),
    (8): (KEY, [Keycode.S], [Keycode.TWO]),
    (9): (KEY, [Keycode.D], [Keycode.THREE]),
    (10): (KEY, [Keycode.F], [Keycode.FOUR]),
    (11): (KEY, [Keycode.G], [Keycode.FIVE]),

    (12): (KEY, [Keycode.LEFT_SHIFT], [Keycode.LEFT_SHIFT]),
    (13): (KEY, [Keycode.Z], [Keycode.LEFT_BRACKET]),
    (14): (KEY, [Keycode.X], [Keycode.RIGHT_BRACKET]),
    (15): (KEY, [Keycode.C], [Keycode.MINUS]),
    (16): (KEY, [Keycode.V], [Keycode.EQUALS]),
    (17): (KEY, [Keycode.B], [Keycode.BACKSLASH]),

    (18): (KEY, [Keycode.CONTROL], [Keycode.CONTROL]),
    (19): (KEY, [Keycode.ENTER], [Keycode.ENTER]),
    (20): (OTHER, [], []),

}

switches = []
for i in range(len(pins)):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)


switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
layer = 1

while True:
    for button in range(21):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][layer])
                    elif keymap[button][0] == MEDIA:
                        cc.send(keymap[button][layer])
                    else:
                        layer = layer + 1
                        if layer > 2:
                            layer = 1
                except ValueError:  # deals w six key limit

                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][layer])

                except ValueError:
                    pass
                switch_state[button] = 0

    time.sleep(0.01)  # debounce
