"""Minimal screen-capture probe for the Linux companion."""
import mss
from PIL import Image

with mss.mss() as sct:
    monitor = sct.monitors[1]  # primary display
    shot = sct.grab(monitor)
    img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
    out = "/tmp/mono-capture.png"
    img.save(out)
    print("saved", out, img.size)
