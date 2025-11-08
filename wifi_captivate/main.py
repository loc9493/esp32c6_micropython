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
from machine import Pin
from neopixel import NeoPixel

# Configure the built-in LED pin
# ESP32-C6 typically has LED on GPIO 8 (check your board documentation)
pin = Pin(8, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 1)   # create NeoPixel driver on GPIO0 for 8 pixels


def blink_led(duration=0.5):
    """Blink the LED once"""
    np[0] = (255, 255, 255) # set the first pixel to white
    np.write()              # write data to all pixels
    time.sleep(duration)
    np[0] = (255, 0, 0) # set the first pixel to white
    np.write()              # write data to all pixels
    time.sleep(duration)

def main():
    """Main loop - blink LED continuously"""
    print("ESP32-C6 LED Blink Started")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            blink_led()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping LED blink...")
        print("Done!")

if __name__ == "__main__":
    main()

