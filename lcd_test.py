"""
CircuitPython LCD display demonstration
From: https://www.penguintutor.com/electronics/pico-lcd
Library: https://github.com/dhalbert/CircuitPython_LCD
"""

import board
import busio
import time
from lcd.lcd import LCD, CursorMode
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

i2c_scl = board.GP3
i2c_sda = board.GP2
i2c_address = 0x27

cols = 16
rows = 2

i2c = busio.I2C(scl=i2c_scl, sda=i2c_sda)
interface = I2CPCF8574Interface(i2c, i2c_address)
lcd = LCD(interface, num_rows=rows, num_cols=cols)
lcd.set_cursor_mode(CursorMode.HIDE)

def main():
    lcd.clear()
    lcd.print("Starting...")
    time.sleep(2)
    lcd.clear()
    lcd.print("About to start\nthe timer")
    time.sleep(2)
    count = 0
    while True:
        lcd.clear()
        lcd.print("Counting:\n" + str(count))
        count += 1
        time.sleep(1)

if __name__ == '__main__':
    main()
# Write your code here :-)
