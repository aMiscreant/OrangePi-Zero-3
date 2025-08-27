# Working gif display
import opigpio_patch
import OPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageSequence
import time

GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)

serial = spi(port=1, device=1, gpio_DC="PC6", gpio_RST="PC11", gpio=GPIO)

device = st7735(
    serial_interface=serial,
    gpio=GPIO,
    gpio_LIGHT="PC9",
    width=160,
    height=128,
    rotate=0
)

gif = Image.open("smaller_kali.gif")

while True:  # Infinite loop to replay
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGB").resize((device.width, device.height))
        # frame_delay = frame.info.get("duration", 100) / 1000.0
        device.display(frame)
        time.sleep(gif.info.get('duration', 100) / 1000.0)
