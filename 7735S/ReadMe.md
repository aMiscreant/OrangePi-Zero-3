# 🛠️ Orange Pi Zero 3 + ST7735 SPI Display Guide (Kali Linux, 2025)

> This guide takes you from **zero to a working Python-powered SPI display** on the **Orange Pi Zero 3** using a **ST7735 TFT screen**.

Tired of vague forum posts and blogs? This is **tested**, **documented**, and **confirmed working** with Kali Linux 2024/2025.

---

## 📦 Prerequisites

- ✅ **Orange Pi Zero 3**
- ✅ **Kali Linux 2024/2025** (or any Armbian/Ubuntu image with recent kernel)
- ✅ **ST7735 SPI TFT display** (128x160 or 128x128 resolution)
- ✅ Wires for SPI:
  - `DC` → PC6
  - `RST` → PC11
  - `BL` (Backlight, optional) → PC9
- ✅ Python 3.9+ with `venv` enabled

---

## ⚙️ Enable SPI1 via Device Tree Overlay

### 1. Decompile the DTB

```bash
dtc -I dtb -O dts -o opi.dts /boot/dtb/sun50i-h618-orangepi-zero3.dtb

2. Edit opi.dts

Find this block:

```
&spi1 {
    status = "disabled";
};

And replace it with this example configuration (adjust if needed):

&spi1 {
    status = "okay";

    spidev@0 {
        compatible = "spidev";
        reg = <0>;
        spi-max-frequency = <32000000>;
    };
};
```
💡 This is a visual example. Your real .dts may differ. You're enabling SPI1 + a device under it.
3. Recompile the DTS

dtc -I dts -O dtb -o sun50i-h618-orangepi-zero3.dtb opi.dts

4. Backup and Replace Original DTB

sudo cp /boot/dtb/sun50i-h618-orangepi-zero3.dtb /boot/dtb/sun50i-h618-orangepi-zero3.dtb.bak
sudo cp sun50i-h618-orangepi-zero3.dtb /boot/dtb/

5. Reboot & Verify SPI Node

ls -l /dev/spidev*

Expected output:

/dev/spidev0.0
/dev/spidev1.1

Test the device with:

sudo ./spidev_test -D /dev/spidev1.1 -v

Expected output:

spi mode: 0x0
bits per word: 8
max speed: 500000 Hz (500 kHz)
TX | ... @ 00 00 00 ... |
RX | FF FF FF FF FF FF ... |

🎯 You’re good if you see data flowing!
🧪 Python SPI Display: "Hello World" on ST7735
1. Create Virtual Environment & Install Requirements

python3 -m venv venv
source venv/bin/activate
pip install luma.lcd Pillow OrangePi.GPIO

2. Monkeypatch RPi.GPIO (needed by luma.lcd)

Create a file: opigpio_patch.py

import sys
import OPi.GPIO as GPIO
sys.modules['RPi.GPIO'] = GPIO

3. Display Script (screen.py)

import opigpio_patch  # Must be first!
import OPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageDraw, ImageFont
import subprocess

GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)

serial = spi(port=1, device=1, gpio_DC="PC6", gpio_RST="PC11", gpio=GPIO)

device = st7735(
    serial_interface=serial,
    gpio=GPIO,
    gpio_LIGHT="PC9",  # optional backlight pin
    width=160,
    height=128,
    rotate=0
)

font = ImageFont.load_default()

while True:
    img = Image.new('RGB', (160, 128), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    output = subprocess.getoutput("uptime")
    draw.text((5, 5), output, font=font, fill=(255, 255, 255))
    device.display(img)

📂 Share the Following Files

Make these available to your repo, flash drive, or offline setup:
    opi.dts — your modified source file
    sun50i-h618-orangepi-zero3.dtb — compiled DTB
    opigpio_patch.py
    screen.py
    requirements.txt:

luma.lcd
Pillow
OrangePi.GPIO

🎉 Done!

You now have a Python-powered live SPI display running on your Orange Pi Zero 3 under Kali Linux 2025.

    Tip: Expand the script to display weather, IP address, CPU temp, etc. The possibilities are endless.

Made for real Orange Pi hackers.


---


