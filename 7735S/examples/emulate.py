# A bit hacky but it works?
# script -f /tmp/term.log -c "bash" &
# python3 emulate.py
# may need to type after running the script or cat the term.log

import opigpio_patch  # Must be first
import OPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageDraw, ImageFont
import time
import os
import re

ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

def strip_ansi(line):
    return ansi_escape.sub('', line)

GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)

# SPI Display setup
serial = spi(port=1, device=1, gpio_DC="PC6", gpio_RST="PC11", gpio=GPIO)
device = st7735(
    serial_interface=serial,
    gpio=GPIO,
    gpio_LIGHT="PC9",  # Warning: Disables backlight control
    width=160,
    height=128,
    rotate=0
)

# Font setup (use default for compatibility)
font = ImageFont.load_default()
#line_height = font.getsize("A")[1] + 2
bbox = font.getbbox("A")
line_height = (bbox[3] - bbox[1]) + 2

max_lines = device.height // line_height

# Display logo first
logo = Image.open("logo.jpg").resize((device.width, device.height)).convert("RGB")
device.display(logo)
time.sleep(5)
logo = Image.open("kali.png").resize((device.width, device.height)).convert("RGB")
device.display(logo)
time.sleep(5)

# Tail log and render lines
def tail_log(path):
    with open(path, 'r') as f:
        f.seek(0, os.SEEK_END)
        lines = []
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            #lines.append(line.strip())
            lines.append(strip_ansi(line.strip()))
            lines = lines[-max_lines:]

            # Create image canvas
            img = Image.new("RGB", (device.width, device.height), "black")
            draw = ImageDraw.Draw(img)

            for i, l in enumerate(lines):
                draw.text((0, i * line_height), l, font=font, fill="white")

            device.display(img)

try:
    tail_log("/tmp/term.log")
except KeyboardInterrupt:
    print("Exiting.")
