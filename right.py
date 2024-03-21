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
    board.GP28,
    board.GP27,
    board.GP26,
    board.GP22,
    board.GP21,
    board.GP20,
    board.GP19,
    board.GP18,
    board.GP17,
    board.GP16,
    board.GP6,
    board.GP5,
    board.GP12,
    board.GP11,
    board.GP10,
    board.GP9,
    board.GP8,
    board.GP7,
    board.GP15,
    board.GP14,
    board.GP13,
)

MEDIA = 1
KEY = 2
OTHER = 3

keymap = {
    (0): (KEY, [Keycode.BACKSPACE], [Keycode.BACKSPACE], [Keycode.BACKSPACE]),
    (1): (KEY, [Keycode.P], [Keycode.DELETE], [Keycode.KEYPAD_MINUS]),
    (2): (KEY, [Keycode.O], [Keycode.PAGE_UP], [Keycode.KEYPAD_NINE]),
    (3): (KEY, [Keycode.I], [Keycode.UP_ARROW], [Keycode.KEYPAD_EIGHT]),
    (4): (KEY, [Keycode.U], [Keycode.HOME], [Keycode.KEYPAD_SEVEN]),
    (5): (KEY, [Keycode.Y], [Keycode.PRINT_SCREEN], [Keycode.KEYPAD_FORWARD_SLASH]),

    (6): (KEY, [Keycode.ALT], [Keycode.ALT], [Keycode.RIGHT_ALT]),
    (7): (KEY, [Keycode.SEMICOLON], [Keycode.ENTER], [Keycode.KEYPAD_PLUS]),
    (8): (KEY, [Keycode.L], [Keycode.RIGHT_ARROW], [Keycode.KEYPAD_SIX]),
    (9): (KEY, [Keycode.K], [Keycode.DOWN_ARROW], [Keycode.KEYPAD_FIVE]),
    (10): (KEY, [Keycode.J], [Keycode.LEFT_ARROW], [Keycode.KEYPAD_FOUR]),
    (11): (KEY, [Keycode.H], [Keycode.SCROLL_LOCK], [Keycode.KEYPAD_ASTERISK]),

    (12): (KEY, [Keycode.RIGHT_SHIFT], [Keycode.RIGHT_SHIFT], [Keycode.RIGHT_SHIFT]),
    (13): (KEY, [Keycode.FORWARD_SLASH], [Keycode.APPLICATION], [Keycode.KEYPAD_PERIOD]),
    (14): (KEY, [Keycode.PERIOD], [Keycode.PAGE_DOWN], [Keycode.KEYPAD_THREE]),
    (15): (KEY, [Keycode.COMMA], [Keycode.TAB], [Keycode.KEYPAD_TWO]),
    (16): (KEY, [Keycode.M], [Keycode.END], [Keycode.KEYPAD_ONE]),
    (17): (KEY, [Keycode.N], [Keycode.PAUSE], [Keycode.KEYPAD_ZERO]),

    (18): (KEY, [Keycode.CONTROL], [Keycode.CONTROL], [Keycode.CONTROL]),
    (19): (KEY, [Keycode.SPACEBAR], [Keycode.SPACEBAR], [Keycode.SPACEBAR]),
    (20): (OTHER, [], [], []),

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
                        led.value = False
                        if layer > 3:
                            layer = 1
                            led.value = True
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
