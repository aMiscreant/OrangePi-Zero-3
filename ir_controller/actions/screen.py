from PIL import Image, ImageDraw, ImageFont
import os
import time

FBDEV = "/dev/fb0"  # adjust if your TFT framebuffer is different
WIDTH, HEIGHT = 320, 480  # adjust for your TFT
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def show_notification(text, duration=2, font_size=18):
    if not os.path.exists(FBDEV):
        print(f"[SCREEN] {text}")
        return

    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, font_size) if os.path.exists(FONT_PATH) else ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((WIDTH - tw) // 2, (HEIGHT - th) // 2), text, font=font, fill="white")

    # Convert to RGB565
    rgb565 = img.convert("RGB").convert("RGB").tobytes("raw", "BGR;16")

    try:
        with open(FBDEV, "wb") as f:
            f.write(rgb565)
    except OSError as e:
        print(f"[SCREEN ERROR] {e}")

    if duration > 0:
        time.sleep(duration)
        blank = Image.new("RGB", (WIDTH, HEIGHT), "black")
        try:
            with open(FBDEV, "wb") as f:
                f.write(blank.convert("RGB").tobytes("raw", "BGR;16"))
        except OSError:
            pass

