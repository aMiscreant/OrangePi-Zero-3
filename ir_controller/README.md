# OrangePi IR Controller

Python IR remote controller for Orange Pi with TFT display.  
Learn IR codes, store multiple codes per action, and trigger system or custom actions.

---

## Features

- Learn IR codes and assign labels
- Trigger actions: POWER, REBOOT, SHUTDOWN, SAY_HELLO, or custom
- Debounce to prevent repeats
- TFT notifications (fallback to console if headless)
- Multiple codes per action supported

---

## Requirements

- Orange Pi with IR receiver (/dev/lirc0)
- TFT display (/dev/fb0) or HDMI framebuffer
- Python 3.8+
- Pillow (`pip install pillow`)
- LIRC (`sudo apt install lirc`)

---

## Install

```bash
git clone https://github.com/amiscreant/orangepi-ir-controller.git
cd orangepi-ir-controller
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

```python
python3 main.py --start
```

## Learn Codes

```python
python3 main.py --start
```

---

## Config

## IR codes stored in config/ir_codes.json:

    Example:
            
        {
        "B_POWER": ["0xffffff005823000178110000500200012002000048020001"],
        "B_LIGHT_DOWN": ["0x2a0184006023000178110000500200012002000050020001"]
        }

---

Supports multiple codes per label.


---

**TFT Notes**

_Adjust width, height, and font in actions/screen.py
Notifications auto-center, optional duration clear
Prints to console if framebuffer unavailable_