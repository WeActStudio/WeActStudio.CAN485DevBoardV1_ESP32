#  - WeAct Studio Official Link
#  - taobao: weactstudio.taobao.com
#  - aliexpress: weactstudio.aliexpress.com
#  - github: github.com/WeActStudio
#  - gitee: gitee.com/WeAct-TC
#  - blog: www.weact-tc.cn

import machine
import esp

print('CPU Freq.: ' + str(machine.freq()/1000000) + 'Mhz')
print('Flash Size: ' + str(esp.flash_size()/1024) + 'kB')

from utime import sleep,ticks_ms
from machine import Pin

print('led with smooth duty change Example')

DUTY_MAX = 64

duty_u16 = 0
delta_d = 1

from neopixel import NeoPixel
np = NeoPixel(Pin(4, Pin.OUT), 1)

tick = 0
led_tick = 0
while True:
    tick = ticks_ms()
    
    if tick >= led_tick:
        led_tick = tick + 8
        
        np[0] = (0, 0, duty_u16)
        np.write()

        duty_u16 += delta_d
        if duty_u16 >= DUTY_MAX:
            duty_u16 = DUTY_MAX
            delta_d = -delta_d
        elif duty_u16 <= 0:
            duty_u16 = 0
            delta_d = -delta_d
