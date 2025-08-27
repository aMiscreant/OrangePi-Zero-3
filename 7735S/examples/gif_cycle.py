import opigpio_patch
import OPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageSequence
import time
import itertools

# --- GPIO Setup ---
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

# --- GIF List ---
gif_files = ["smaller_kali.gif", "smaller_got.gif",
             "smaller_cat.gif", "smaller_matrix.gif",
             "smaller_meme.gif", "smaller_hackerman.gif",
             "smaller_enhance.gif", "smaller_crap.gif"]  # Add more as needed
display_duration = 15  # seconds per full gif cycle

# --- Function to display GIF for a duration ---
def play_gif(gif_path, duration=15):
    try:
        gif = Image.open(gif_path)
        start_time = time.time()

        while time.time() - start_time < duration:
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGB").resize((device.width, device.height))
                frame_delay = frame.info.get("duration", 100) / 1000.0
                device.display(frame)
                time.sleep(frame_delay)

                # Check time again mid-sequence
                if time.time() - start_time >= duration:
                    break
    except Exception as e:
        print(f"Error with {gif_path}: {e}")

# --- Main Loop ---
for gif_path in itertools.cycle(gif_files):
    print(f"Displaying: {gif_path}")
    play_gif(gif_path, display_duration)
