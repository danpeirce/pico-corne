# Micropython Code for Corne like Keyboard

The design goals are for a DIY keyboard in a Corne like layout. 

1. Keep it Simple. 
    a. The code does not need to be generalized for all keyboards (not using KMK). 
	b. The two halves are to have equal responsibility with minimal interaction. Connect both halves to a USB hub. 
	   Each half to get a Pico board and they both already have on board microB USB connectors.
	c. Pico boards have more than enough GPIO to use one input per switch. There are 21 switches per side and each Pico has 26 
	   GPIO. Diodes are not needed because a matrix is not needed.
	d. The only keys that need to be shared between sides are the layer keys.
	
Micropython Coding a Raspberry Pi Pico board for a split keyboard with 3x6 column staggered keys and 3 thumb keys.
## Reference


[Pico_RP2040_Mech_Keyboard/code.py](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Pico_RP2040_Mech_Keyboard/code.py)
[Adafruit HID Library](https://docs.circuitpython.org/projects/hid/en/latest/)