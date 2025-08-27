import opigpio_patch  # Must be first to monkey-patch RPi.GPIO
import OPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageDraw, ImageFont

GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)

serial = spi(port=1, device=1, gpio_DC="PC6", gpio_RST="PC11", gpio=GPIO)

#device = st7735(serial_interface=serial, gpio=GPIO, width=128, height=160, rotate=0)

device = st7735(
    serial_interface=serial,
    gpio=GPIO,
    gpio_LIGHT="PC9",  # <- This disables backlight control *DO NOT plug in BLK to PC9*
    width=160,
    height=128,
    rotate=0
)

logo = Image.open("logo.jpg").resize((device.width, device.height)).convert("RGB")
device.display(logo)