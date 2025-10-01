# utils/logger.py

import datetime

LOG_FILE = "ir.log"
ENABLE_FILE_LOGGING = True

def timestamp():
    """Return current time formatted as a string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, write_to_file=True):
    """Print a timestamped message and optionally log it to a file."""
    tagged = f"[{timestamp()}] {msg}"
    print(tagged)

    if ENABLE_FILE_LOGGING and write_to_file:
        with open(LOG_FILE, "a") as f:
            f.write(tagged + "\n")

def warn(msg):
    """Log a warning."""
    log(f"[WARN] {msg}")

def error(msg):
    """Log an error."""
    log(f"[ERROR] {msg}")

def success(msg):
    """Log a success message."""
    log(f"[OK] {msg}")
