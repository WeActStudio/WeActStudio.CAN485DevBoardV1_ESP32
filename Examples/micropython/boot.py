# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from machine import Pin
from neopixel import NeoPixel
np = NeoPixel(Pin(4, Pin.OUT), 1)
np[0] = (0, 0, 0)
np.write()
del np

import network
ap = network.WLAN(network.AP_IF)
ap.active(False)
del ap
