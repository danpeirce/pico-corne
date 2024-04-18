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
    (0): ((KEY, [Keycode.TAB]), (KEY, [Keycode.ESCAPE]), (KEY, [Keycode.F7])),
    # (1): ((KEY, [Keycode.Q]), (KEY, [Keycode.SIX]),
    #     (MEDIA, ConsumerControlCode.MUTE)),
    (1): ((KEY, [Keycode.Q]), (KEY, [Keycode.SIX]), (KEY, [Keycode.F8])),
    # (2): ((KEY, [Keycode.W]), (KEY, [Keycode.SEVEN]),
    #     (MEDIA, ConsumerControlCode.VOLUME_DECREMENT)),
    (2): ((KEY, [Keycode.W]), (KEY, [Keycode.SEVEN]), (KEY, [Keycode.F9])),
    # (3): ((KEY, [Keycode.E]), (KEY, [Keycode.EIGHT]),
    #     (MEDIA, ConsumerControlCode.VOLUME_INCREMENT)),
    (3): ((KEY, [Keycode.E]), (KEY, [Keycode.EIGHT]), (KEY, [Keycode.F10])),
    # (4): ((KEY, [Keycode.R]), (KEY, [Keycode.NINE]),
    #      (MEDIA, ConsumerControlCode.PLAY_PAUSE)),
    (4): ((KEY, [Keycode.R]), (KEY, [Keycode.NINE]), (KEY, [Keycode.F11])),
    (5): ((KEY, [Keycode.T]), (KEY, [Keycode.ZERO]), (KEY, [Keycode.F12])),

    (6): ((KEY, [Keycode.ALT]), (KEY, [Keycode.ALT]), (KEY, [Keycode.F1])),
    (7): ((KEY, [Keycode.A]), (KEY, [Keycode.ONE]), (KEY, [Keycode.F2])),
    (8): ((KEY, [Keycode.S]), (KEY, [Keycode.TWO]), (KEY, [Keycode.F3])),
    (9): ((KEY, [Keycode.D]), (KEY, [Keycode.THREE]), (KEY, [Keycode.F4])),
    (10): ((KEY, [Keycode.F]), (KEY, [Keycode.FOUR]), (KEY, [Keycode.F5])),
    # (11): ((KEY, [Keycode.G]), (KEY, [Keycode.FIVE]),
    #       (MEDIA, ConsumerControlCode.STOP)),
    (11): ((KEY, [Keycode.G]), (KEY, [Keycode.FIVE]), (KEY, [Keycode.F6])),

    (12): ((KEY, [Keycode.LEFT_SHIFT]),
           (KEY, [Keycode.LEFT_SHIFT]), (KEY, [Keycode.LEFT_SHIFT])),
    (13): ((KEY, [Keycode.Z]),
           (KEY, [Keycode.LEFT_BRACKET]), (KEY, [Keycode.GRAVE_ACCENT])),
    (14): ((KEY, [Keycode.X]), (KEY, [Keycode.RIGHT_BRACKET]), (KEY, [Keycode.ALT])),
    (15): ((KEY, [Keycode.C]), (KEY, [Keycode.MINUS]), (KEY, [Keycode.WINDOWS])),
    (16): ((KEY, [Keycode.V]), (KEY, [Keycode.EQUALS]), (KEY, [Keycode.QUOTE])),
    (17): ((KEY, [Keycode.B]), (KEY, [Keycode.BACKSLASH]), (KEY, [Keycode.CAPS_LOCK])),

    (18): ((KEY, [Keycode.CONTROL]),
           (KEY, [Keycode.CONTROL]), (KEY, [Keycode.CONTROL])),
    (19): ((KEY, [Keycode.ENTER]), (KEY, [Keycode.ENTER]), (KEY, [Keycode.ENTER])),
    (20): ((OTHER, []), (OTHER, []), (OTHER, [])),

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
