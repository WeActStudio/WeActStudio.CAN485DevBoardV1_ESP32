import machine
import sdcard
import os

spi = machine.SPI(1, sck=machine.Pin(14), mosi=machine.Pin(15), miso=machine.Pin(2))
spi.init()
sd = sdcard.SDCard(spi, machine.Pin(13))
vfs = os.VfsFat(sd)
os.mount(vfs, "/fc")