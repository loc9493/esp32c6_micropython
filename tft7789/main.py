# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
"""
ESP32-C6 LED Blink Example for MicroPython
Simple LED blinking program for ESP32-C6 development board
"""

import machine
import time
from machine import Pin, SPI
from neopixel import NeoPixel
import asyncio
from tft7789 import ST7789, color565
from xglcd_font import XglcdFont


# Configure the built-in LED pin
# ESP32-C6 typically has LED on GPIO 8 (check your board documentation)
pin = Pin(8, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 1)   # create NeoPixel driver on GPIO0 for 8 pixels
TFT_CS = 15
TFT_RST        = 22
TFT_DC         = 23

async def blink_led(duration=0.5):
    """Blink the LED once"""
    np[0] = (255, 255, 255) # set the first pixel to white
    np.write()              # write data to all pixels
    time.sleep(duration)
    np[0] = (255, 0, 0) # set the first pixel to white
    np.write()              # write data to all pixels
    time.sleep(duration)

async def main():
    display = ST7789(
            SPI(baudrate=40000000, miso=Pin(11), mosi=Pin(19, Pin.OUT), sck=Pin(21, Pin.OUT) ),
            240, 320,
            rst=machine.Pin(22, machine.Pin.OUT),
            dc=machine.Pin(23, machine.Pin.OUT),
            cs=machine.Pin(15, machine.Pin.OUT),
        )
    display.fill(0x00)
    neato = XglcdFont('fonts/neato.c', 5, 8)
    display._set_mem_access_mode(4, False, False, True)
    display.draw_text(5, 0, 'set the first pixel to white', neato, color565(255, 255, 0), landscape= False)
    display._set_mem_access_mode(1, False, True, True)
    display.draw_image('panda.raw', 0, 0, 240, 320)
    #display.text((0, 0), 'set the first pixel to white', color565(255, 255, 0), neato)
    try:
        while True:
            asyncio.create_task(blink_led())
            await asyncio.sleep_ms(1000)
            
    except KeyboardInterrupt:
        print("\nStopping LED blink...")
        print("Done!")



asyncio.run(main())
