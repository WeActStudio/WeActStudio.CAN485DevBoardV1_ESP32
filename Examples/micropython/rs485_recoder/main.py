from machine import Pin
from neopixel import NeoPixel
import machine
import os
import sdcard

from machine import UART, Pin
import time
import binascii
import micropython

class MessageQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, message):
        self.queue.append(message)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


class RS485_Recorder:
    def __init__(self):
        self.uart_mq = MessageQueue()

        self.np = NeoPixel(
            Pin(4, Pin.OUT), 1
        )
        self.np[0] = (20, 0, 0)
        self.np.write()

        self.button = Pin(0, Pin.IN, Pin.PULL_UP)

        self.RS485_DE = Pin(17, Pin.OUT, 0)

        self.spi = machine.SPI(
            1, sck=machine.Pin(14), mosi=machine.Pin(15), miso=machine.Pin(2)
        )
        self.spi.init()
        self.sd = sdcard.SDCard(self.spi, machine.Pin(13))
        self.vfs = os.VfsFat(self.sd)
        os.mount(self.vfs, "/fc")

        self.led_set_color((0, 20, 0))

    def led_set_color(self, color):
        self.np[0] = color
        self.np.write()

    def rs485_init(self):
        self.uart = UART(
            1, baudrate=115200, bits=8, parity=None, stop=2, tx=machine.Pin(22), rx=machine.Pin(21)
        )
        self.uart.init()
        self.uart.irq(self.uart_rxidle_irq, self.uart.IRQ_RXIDLE)

    def rs485_deinit(self):
        self.uart.deinit()
        self.RS485_DE.value(0)

    def uart_rxidle_irq(self, t):
        self.uart_mq.enqueue(self.uart.read())

    def find_new_file_name(self):
        file_list = os.listdir("/fc")
        max_file_num = 0
        for file_name in file_list:
            if file_name.endswith(".txt"):
                file_name = file_name[:-4]
                if file_name.isdigit():
                    file_name = int(file_name)
                    if file_name > max_file_num:
                        max_file_num = file_name
        return max_file_num + 1
    
    def run(self):
        tick_blink = 0
        blink_step = 0

        button_tick = 0
        button_press_count = 0

        record_start = False
        recode_step = 1
        recode_file_name = ""
        tick_record = 0
        green = 20
        green_add = False
        while True:
            tick_now = time.ticks_ms()
            if tick_now > tick_blink:
                tick_blink = tick_now + 200
                if record_start:
                    if blink_step:
                        self.led_set_color((0, 20, 0))
                        blink_step = 0
                    else:
                        self.led_set_color((0, 0, 20))
                        blink_step = 1
                else:
                    self.led_set_color((0, green, 0))
                    if green_add:
                        green = green + 2
                        if green > 20:
                            green_add = False
                            green = 18
                    else:
                        green = green - 2
                        if green <= 0:
                            green_add = True
                            green = 2

            if tick_now > button_tick:
                button_tick = tick_now + 1
                if self.button.value() == 0:
                    button_press_count = button_press_count + 1
                    if button_press_count > 1000:
                        button_press_count = 0
                        self.led_set_color((20, 10, 0))
                        break
                else:
                    if button_press_count > 30:
                        record_start = not record_start
                        recode_step = 0
                    button_press_count = 0

            if record_start:
                if recode_step == 0:
                    recode_file_name = "/fc/" + str(self.find_new_file_name()) + ".txt"
                    # print("start record:", recode_file_name)
                    recode_step = 1
                    self.rs485_init()
                    tick_record = tick_now
                    with open(recode_file_name, "a") as f:
                        f.write("time,data\r\n")
                if recode_step == 1:
                    if not self.uart_mq.is_empty():
                        with open(recode_file_name, "a") as f:
                            w = ''
                            t_w = str(tick_now - tick_record) + ','
                            # print(tick_now - tick_record)
                            while not self.uart_mq.is_empty():
                                data = self.uart_mq.dequeue()
                                if data is not None:
                                    hex_data = binascii.hexlify(data).decode()
                                    spaced_hex_data = " ".join(
                                        hex_data[i : i + 2] for i in range(0, len(hex_data), 2)
                                    )
                                    t = t_w + spaced_hex_data + "\r\n"
                                    w = w + t
                            f.write(w)
            else:
                if recode_step == 0:
                    self.rs485_deinit()
                    # print("stop record:", recode_file_name)
                    recode_step = 1

r = RS485_Recorder()
r.run()

