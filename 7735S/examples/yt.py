import subprocess
from PIL import Image
import opigpio_patch
import OPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.lcd.device import st7735

# GPIO/SPI setup
GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)
serial = spi(port=1, device=1, gpio_DC="PC6", gpio_RST="PC11", gpio=GPIO)
device = st7735(serial_interface=serial, gpio=GPIO, gpio_LIGHT="PC9", width=160, height=128, rotate=0)

# Start ffmpeg to stream from stdin (from yt-dlp)
ffmpeg_cmd = [
    'yt-dlp', '-f', 'best', '-o', '-', 'https://www.youtube.com/watch?v=XXXX'
]
ffmpeg = subprocess.Popen(
    ['ffmpeg', '-i', 'pipe:0', '-vf', 'scale=160:128', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE
)

ytdlp = subprocess.Popen(ffmpeg_cmd, stdout=ffmpeg.stdin)

# Read and display
frame_size = 160 * 128 * 3  # width * height * RGB
try:
    while True:
        raw_frame = ffmpeg.stdout.read(frame_size)
        if len(raw_frame) != frame_size:
            break

        image = Image.frombytes("RGB", (160, 128), raw_frame)
        device.display(image)
except KeyboardInterrupt:
    pass
finally:
    ffmpeg.kill()
    ytdlp.kill()
