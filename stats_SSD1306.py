# Install pip3 install adafruit-circuitpython-ssd1306



# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
from pijuice import (PiJuice)
import subprocess

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Use for I2C.
i2c = board.I2C()
WIDTH=128
HEIGHT=32
disp = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=None)

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

pijuice = PiJuice(1, 0x14)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

def getCmdStr(cmd):
    return subprocess.check_output(cmd, shell = True).decode('utf-8').strip()

def checkValue(val):
    val = val['data'] if val['error'] == 'NO_ERROR' else val['error']
    return val

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = getCmdStr(cmd)
    cmd = "uptime | awk '{printf $3 $8 $9 $10}'"
    CPU = getCmdStr(cmd)
    cmd = "free -m | awk 'NR==2{printf \"%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = getCmdStr(cmd)
    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB %s\", $3,$2,$5}'"
    Disk = getCmdStr(cmd)

    charge = checkValue(pijuice.status.GetChargeLevel())
    fault =  checkValue(pijuice.status.GetFaultStatus())
    temp = checkValue(pijuice.status.GetBatteryTemperature())
    vbat = checkValue(pijuice.status.GetBatteryVoltage())
    ibat = checkValue(pijuice.status.GetBatteryCurrent())
    vio =  checkValue(pijuice.status.GetIoVoltage())
    iio = checkValue(pijuice.status.GetIoCurrent())
    print('Charge =',charge,'%,', 'T =', temp, ', Vbat =',vbat, ', Ibat =',ibat, ', Vio =',vio, ', Iio =',iio)


    print(pijuice.status.GetStatus())

    draw.text((x, top),       IP,  font=font, fill=255)
    draw.text((x, top+8),     CPU, font=font, fill=255)
    draw.text((x, top+16),    "M: " + MemUsage,  font=font, fill=255)
    draw.text((x, top+25),    "D: " + Disk,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(.3)
