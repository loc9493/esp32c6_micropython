esptool.py --port /dev/tty.usbmodem21101 erase_flash
esptool.py --port /dev/tty.usbmodem21101 --baud 460800 write_flash 0 esp32.bin

