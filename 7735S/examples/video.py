import cv2
from PIL import Image
import opigpio_patch  # Must be first
import OPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.lcd.device import st7735

# Setup GPIO and SPI
GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)
serial = spi(port=1, device=1, gpio_DC="PC6", gpio_RST="PC11", gpio=GPIO)

device = st7735(
    serial_interface=serial,
    gpio=GPIO,
    gpio_LIGHT="PC9",  # Optional: remove if you want auto backlight control
    width=160,
    height=128,
    rotate=0
)

# Open video
cap = cv2.VideoCapture('resized.mp4')

# Blit as fast as possible
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_resized = cv2.resize(frame, (device.width, device.height))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    frame_image = Image.fromarray(frame_rgb)
    device.display(frame_image)  # <- Main bottleneck (SPI writes)

cap.release()
