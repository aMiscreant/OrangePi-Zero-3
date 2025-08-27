import os
import pty
import select

# Set up pty and fork BEFORE any other complex imports
master_fd, slave_fd = pty.openpty()
pid = os.fork()

if pid == 0:
    # Child: Replace process with a shell
    os.putenv("TERM", "linux")
    os.dup2(slave_fd, 0)
    os.dup2(slave_fd, 1)
    os.dup2(slave_fd, 2)
    os.execv("/bin/bash", ["/bin/bash"])

# ---- PARENT PROCESS ----
import pyte
import time
import threading
from PIL import Image, ImageDraw, ImageFont

import opigpio_patch
import OPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
import sys
import termios
import tty

def read_keyboard_input():
    # Set terminal to raw mode to capture individual keypresses
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    try:
        while True:
            key = os.read(sys.stdin.fileno(), 1)
            os.write(master_fd, key)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

# Setup GPIO + SPI + LCD
GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)
serial = spi(port=1, device=1, gpio_DC="PC6", gpio_RST="PC11", gpio=GPIO)
device = st7735(serial_interface=serial, gpio=GPIO, gpio_LIGHT="PC9", width=160, height=128, rotate=0)

# Load font
font = ImageFont.truetype("FreeMono.ttf", 11)
bbox = font.getbbox("A")
char_width = bbox[2] - bbox[0]
char_height = bbox[3] - bbox[1]

cols = device.width // char_width
rows = device.height // char_height

# Setup pyte screen
screen = pyte.Screen(cols, rows)
stream = pyte.Stream(screen)

# Thread to read shell output
def read_from_shell():
    while True:
        r, _, _ = select.select([master_fd], [], [], 0.1)
        if r:
            output = os.read(master_fd, 1024).decode(errors="ignore")
            stream.feed(output)

# Thread to draw to LCD
def draw_loop():
    while True:
        image = Image.new("RGB", (device.width, device.height), "black")
        draw = ImageDraw.Draw(image)
        for y, line in enumerate(screen.display):
            draw.text((0, y * char_height), line, font=font, fill="white")
        device.display(image)
        time.sleep(0.05)

threading.Thread(target=read_from_shell, daemon=True).start()
threading.Thread(target=read_keyboard_input, daemon=True).start()
draw_loop()
