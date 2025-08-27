# opigpio_patch.py
import sys
import OPi.GPIO as GPIO

# Monkey-patch RPi.GPIO as OPi.GPIO
sys.modules['RPi.GPIO'] = GPIO
