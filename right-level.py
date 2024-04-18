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

print("---Rightside Pico-Corne---")

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
    (0): ((KEY, [Keycode.BACKSPACE]), (KEY,  [Keycode.BACKSPACE]),
          (KEY,  [Keycode.BACKSPACE])),
    (1): ((KEY, [Keycode.P]), (KEY,  [Keycode.DELETE]), (KEY,  [Keycode.KEYPAD_MINUS])),
    (2): ((KEY, [Keycode.O]), (KEY,  [Keycode.PAGE_UP]), (KEY,  [Keycode.KEYPAD_NINE])),
    (3): ((KEY, [Keycode.I]), (KEY,  [Keycode.UP_ARROW]),
          (KEY,  [Keycode.KEYPAD_EIGHT])),
    (4): ((KEY, [Keycode.U]), (KEY,  [Keycode.HOME]), (KEY,  [Keycode.KEYPAD_SEVEN])),
    (5): ((KEY, [Keycode.Y]), (KEY,  [Keycode.PRINT_SCREEN]),
          (KEY,  [Keycode.KEYPAD_FORWARD_SLASH])),

    (6): ((KEY, [Keycode.ALT]), (KEY,  [Keycode.ALT]), (KEY,  [Keycode.RIGHT_ALT])),
    (7): ((KEY, [Keycode.SEMICOLON]), (KEY,  [Keycode.ENTER]),
          (KEY,  [Keycode.KEYPAD_PLUS])),
    (8): ((KEY, [Keycode.L]), (KEY,  [Keycode.RIGHT_ARROW]),
          (KEY,  [Keycode.KEYPAD_SIX])),
    (9): ((KEY, [Keycode.K]), (KEY,  [Keycode.DOWN_ARROW]),
          (KEY,  [Keycode.KEYPAD_FIVE])),
    (10): ((KEY, [Keycode.J]), (KEY,  [Keycode.LEFT_ARROW]),
           (KEY,  [Keycode.KEYPAD_FOUR])),
    (11): ((KEY, [Keycode.H]), (KEY,  [Keycode.SCROLL_LOCK]),
           (KEY,  [Keycode.KEYPAD_ASTERISK])),

    (12): ((KEY, [Keycode.RIGHT_SHIFT]), (KEY,  [Keycode.RIGHT_SHIFT]),
           (KEY,  [Keycode.RIGHT_SHIFT])),
    (13): ((KEY, [Keycode.FORWARD_SLASH]), (KEY,  [Keycode.APPLICATION]),
           (KEY,  [Keycode.KEYPAD_PERIOD])),
    (14): ((KEY, [Keycode.PERIOD]), (KEY,  [Keycode.PAGE_DOWN]),
           (KEY,  [Keycode.KEYPAD_THREE])),
    (15): ((KEY, [Keycode.COMMA]), (KEY,  [Keycode.TAB]), (KEY,  [Keycode.KEYPAD_TWO])),
    (16): ((KEY, [Keycode.M]), (KEY,  [Keycode.END]), (KEY,  [Keycode.KEYPAD_ONE])),
    (17): ((KEY, [Keycode.N]), (KEY,  [Keycode.PAUSE]), (KEY,  [Keycode.KEYPAD_ZERO])),

    (18): ((KEY, [Keycode.CONTROL]), (KEY,  [Keycode.CONTROL]),
           (KEY,  [Keycode.CONTROL])),
    (19): ((KEY, [Keycode.SPACEBAR]), (KEY,  [Keycode.SPACEBAR]),
           (KEY,  [Keycode.SPACEBAR])),
    (20): ((OTHER, []), (OTHER,  []), (OTHER,  [])),

}

switches = []
for i in range(len(pins)):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)


switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
layer = 0

while True:
    for button in range(21):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][layer][0] == KEY:
                        kbd.press(*keymap[button][layer][1])
                    elif keymap[button][layer][0] == MEDIA:
                        cc.send(keymap[button][layer][1])
                    else:
                        layer = layer + 1
                        led.value = False
                        if layer > 2:
                            layer = 0
                            led.value = True
                except ValueError:  # deals w six key limit

                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][layer][0] == KEY:
                        kbd.release(*keymap[button][layer][1])

                except ValueError:
                    pass
                switch_state[button] = 0

        if switch_state[12] == 1 and switch_state[20] == 1:
            layer = 0
            led.value = True

    time.sleep(0.01)  # debounce
