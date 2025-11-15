import sys
from machine import Pin, SPI
from tft7789 import ST7789, color565
from xglcd_font import XglcdFont
# ruff: noqa: E402
sys.path.append("")

from micropython import const

import asyncio, machine
import aioble
import bluetooth
from aioble import core
import random
import struct
import time
from notification import *

noti_flag = asyncio.ThreadSafeFlag()
notificationService = NotificationService(noti_flag)
display = ST7789(
            SPI(baudrate=40000000, miso=Pin(11), mosi=Pin(19, Pin.OUT), sck=Pin(21, Pin.OUT) ),
            240, 320,
            rst=machine.Pin(22, machine.Pin.OUT),
            dc=machine.Pin(23, machine.Pin.OUT),
            cs=machine.Pin(15, machine.Pin.OUT),
        )
# Run both tasks.
async def main():
    t1 = asyncio.create_task(render())
    t2 = asyncio.create_task(notificationService.registerBLE())
    #t1 = asyncio.create_task(notificationService.main())
    await asyncio.gather(t2, t1)

async def render():
    while True:
        await noti_flag.wait()
        noti = notificationService.notifications[0]
        #display.draw_text(5, 0, noti['attributes'][1], neato, color565(255, 255, 0), landscape= False)
        print("Notifications: ", len(notificationService.notifications))
        print("noti: ", noti)
        
display.fill(0x00)
neato = XglcdFont('fonts/neato.c', 5, 8)
display._set_mem_access_mode(4, False, False, True)
display.draw_text(5, 0, 'set the first trời ơi đất pixel to white', neato, color565(255, 255, 0), landscape= False)
asyncio.run(main())
