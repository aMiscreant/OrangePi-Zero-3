# actions/system.py
import os
from utils.logger import log, error
from ..utils.logger import log,error

def reboot():
    log("[SYSTEM] Rebooting system...")
    try:
        os.system("sudo reboot")
    except Exception as e:
        error(f"Failed to reboot: {e}")

def shutdown():
    log("[SYSTEM] Shutting down system...")
    try:
        os.system("sudo shutdown now")
    except Exception as e:
        error(f"Failed to shut down: {e}")

def run_shell_command(command):
    log(f"[SYSTEM] Running shell command: {command}")
    try:
        result = os.popen(command).read()
        log(f"[SHELL OUTPUT] {result.strip()}")
    except Exception as e:
        error(f"Shell command failed: {e}")
