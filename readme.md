# CircuitPython Code for Corne like Keyboard

The design goals are for a DIY keyboard in a Corne like layout. 

1. Split keyboard with 3x6 column staggered keys and 3 thumb keys. 
    1. The idea here is to have home keys plus keys no more than one row or column away from the home position 
	   to avoid issues with reaching farther.
	2. Keep close to an open source design for the 3D printed case. The Corne layout has a track record. Adjustments are being made
	   so that a RPi Pico can be used. These boards are inexpensive, have lots of GPIO and can handle CircuitPython.
2. Keep it Simple. 
    1. The code does not need to be generalized for all keyboards (not using KMK). 
	2. The two halves are to have equal responsibility. Connect both halves to a USB hub. 
	   Each half to get a Pico board and they both already have on board microB USB connectors.
	3. Pico boards have more than enough GPIO to use one input per switch. There are 21 switches per side and each Pico has 26 
	   GPIO. Diodes are not needed because a matrix is not needed.
3. Keep cost down. 
    1. Use FDM 3D printer for parts that can be printed.
	2. Use point to point wiring - no PCB. This is more work but it avoids ordering custom parts and shipping costs.
4.  Using CircuitPython makes firmware changes easy. One just copies a text file to the Pico file system!
	

## Reference

* [Pico_RP2040_Mech_Keyboard/code.py](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Pico_RP2040_Mech_Keyboard/code.py)
* [www.raspberrypi.com/.../pico-pinout.svg](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg)
* [Adafruit code tutorial](https://learn.adafruit.com/diy-pico-mechanical-keyboard-with-fritzing-circuitpython/code-the-pico-keyboard)
* [Adafruit HID Library](https://docs.circuitpython.org/projects/hid/en/latest/)

## Implementation Progress

### Left Side

* The base layer 1 does the alphabetic characters.
* layer 2 does the numerals and much of the punctuation.
* layer 3 does Function keys, left over punctuation and cap-lock.

### Right Side

* The base layer 1 does the alphabetic characters.
* layer 2 does navigation.
* layer 3 numpad characters.

There is no direct connection between the left and right keyboards. Each half has a Layer key. When a layer key is pressed the active layer on 
that side is incremented by one.

On the left side the combination **left-shift + left-Layer** switches to layer1.


![](Layer1.png)  ![](Layer1R.png)

![](Layer2.png)  ![](Layer2R.png)

![](Layer3.png)  ![](Layer3R.png)

media

![](Layer3media.png)


### Left side keymap dictionary

There are two versions of the left side keymap.

* left.py contains twelve function keys on the third level. 
* left-media.py has media keys in place of some of the function keys.

Either file can be copied to code.py on the CIRCUITPY drive for the left keyboard to change to the other layout. I don't use
function keys often and almost never use the function keys past F5.

The format of the two left keymaps is different because the original format used was not adequate for the addition of media 
controls which were first used in **left-media.py**.

#### From left.py

~~~~python {}[left.py]
keymap = {
    (0): (KEY, [Keycode.TAB], [Keycode.ESCAPE], [Keycode.F7]),
    (1): (KEY, [Keycode.Q], [Keycode.SIX], [Keycode.F8]),
    (2): (KEY, [Keycode.W], [Keycode.SEVEN], [Keycode.F9]),
    (3): (KEY, [Keycode.E], [Keycode.EIGHT], [Keycode.F10]),
    (4): (KEY, [Keycode.R], [Keycode.NINE], [Keycode.F11]),
    (5): (KEY, [Keycode.T], [Keycode.ZERO], [Keycode.F12]),

    (6): (KEY, [Keycode.ALT], [Keycode.ALT], [Keycode.F1]),
    (7): (KEY, [Keycode.A], [Keycode.ONE], [Keycode.F2]),
    (8): (KEY, [Keycode.S], [Keycode.TWO], [Keycode.F3]),
    (9): (KEY, [Keycode.D], [Keycode.THREE], [Keycode.F4]),
    (10): (KEY, [Keycode.F], [Keycode.FOUR], [Keycode.F5]),
    (11): (KEY, [Keycode.G], [Keycode.FIVE], [Keycode.F6]),

    (12): (KEY, [Keycode.LEFT_SHIFT], [Keycode.LEFT_SHIFT], [Keycode.LEFT_SHIFT]),
    (13): (KEY, [Keycode.Z], [Keycode.LEFT_BRACKET], [Keycode.GRAVE_ACCENT]),
    (14): (KEY, [Keycode.X], [Keycode.RIGHT_BRACKET], [Keycode.ALT]),
    (15): (KEY, [Keycode.C], [Keycode.MINUS], [Keycode.WINDOWS]),
    (16): (KEY, [Keycode.V], [Keycode.EQUALS], [Keycode.QUOTE]),
    (17): (KEY, [Keycode.B], [Keycode.BACKSLASH], [Keycode.CAPS_LOCK]),

    (18): (KEY, [Keycode.CONTROL], [Keycode.CONTROL], [Keycode.CONTROL]),
    (19): (KEY, [Keycode.ENTER], [Keycode.ENTER], [Keycode.ENTER]),
    (20): (OTHER, [], [], []),

}
~~~~

#### From left-media.py

~~~~python
keymap = {
    (0): ((KEY, [Keycode.TAB]), (KEY, [Keycode.ESCAPE]), (KEY, [Keycode.F7])),
    (1): ((KEY, [Keycode.Q]), (KEY, [Keycode.SIX]), (MEDIA, ConsumerControlCode.MUTE)),
    # (1): ((KEY, [Keycode.Q]), (KEY, [Keycode.SIX]), (KEY, [Keycode.F8])),
    (2): ((KEY, [Keycode.W]), (KEY, [Keycode.SEVEN]),
          (MEDIA, ConsumerControlCode.VOLUME_DECREMENT)),
    # (2): ((KEY, [Keycode.W]), (KEY, [Keycode.SEVEN]), (KEY, [Keycode.F9])),
    (3): ((KEY, [Keycode.E]), (KEY, [Keycode.EIGHT]),
          (MEDIA, ConsumerControlCode.VOLUME_INCREMENT)),
    # (3): ((KEY, [Keycode.E]), (KEY, [Keycode.EIGHT]), (KEY, [Keycode.F10])),
    (4): ((KEY, [Keycode.R]), (KEY, [Keycode.NINE]),
          (MEDIA, ConsumerControlCode.PLAY_PAUSE)),
    # (4): ((KEY, [Keycode.R]), (KEY, [Keycode.NINE]), (KEY, [Keycode.F11])),
    (5): ((KEY, [Keycode.T]), (KEY, [Keycode.ZERO]), (KEY, [Keycode.F12])),

    (6): ((KEY, [Keycode.ALT]), (KEY, [Keycode.ALT]), (KEY, [Keycode.F1])),
    (7): ((KEY, [Keycode.A]), (KEY, [Keycode.ONE]), (KEY, [Keycode.F2])),
    (8): ((KEY, [Keycode.S]), (KEY, [Keycode.TWO]), (KEY, [Keycode.F3])),
    (9): ((KEY, [Keycode.D]), (KEY, [Keycode.THREE]), (KEY, [Keycode.F4])),
    (10): ((KEY, [Keycode.F]), (KEY, [Keycode.FOUR]), (KEY, [Keycode.F5])),
    (11): ((KEY, [Keycode.G]), (KEY, [Keycode.FIVE]),
           (MEDIA, ConsumerControlCode.STOP)),
    # (11): ((KEY, [Keycode.G]), (KEY, [Keycode.FIVE]), (KEY, [Keycode.F6])),

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
~~~~

### Pin Assignment Left

~~~~python
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
~~~~

### Right side keymap dictionary

~~~~python
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
~~~~

### Pin Assignment Right

~~~~python
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
~~~~

## Hard Wiring the Keyboard

### Left Side (bottom view)

![](img/pico-corne-left-build05-und.png)

![](img/pico.png)

![](img/pico-corne-left-build04-und-w.png)

### Right side (bottom view)

![](img/LayerRw.png)

# The 3D Printed Case

See https://github.com/danpeirce/scad-keyboard-cases?tab=readme-ov-file#corne-inspired-keyboard-case-modified-to-use-a-raspberry-pi-pico
