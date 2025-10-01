# main.py
import argparse
import json
import os
import time

from actions import screen, system
from ir_listener import listen_for_ir
from utils.logger import log
from utils.matcher import match_code, normalize_code

CONFIG_PATH = "config/ir_codes.json"

# Prevent multiple dispatches of same button too fast
_last_triggered = {}
_DEBOUNCE_SECONDS = 0.5  # 0.5 seconds


def load_ir_codes():
    """Load IR codes from JSON file, return dict[label] = list of codes"""
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    # Ensure all values are lists for backward compatibility
    for k, v in data.items():
        if not isinstance(v, list):
            data[k] = [v]
    return data


def save_ir_codes(codes):
    """Save IR codes to JSON file"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(codes, f, indent=4)


def dispatch_action(label):
    """Trigger the action for a given label"""
    log(f"[ACTION] Triggered: {label}")
    if label == "B_POWER":
        screen.show_notification("POWER button pressed")
    elif label == "REBOOT":
        screen.show_notification("Rebooting...")
        system.reboot()
    elif label == "SHUTDOWN":
        screen.show_notification("Shutting down...")
        system.shutdown()

    else:
        log(f"No action mapped for: {label}")


def run_start():
    """Normal mode: listen for codes and dispatch actions"""
    codes = load_ir_codes()
    log("[IR] Starting in RUN mode...")

    while True:
        for raw_code in listen_for_ir():
            now = time.time()
            norm = normalize_code(raw_code)

            # Debounce check
            last_time = _last_triggered.get(norm, 0)
            if now - last_time < _DEBOUNCE_SECONDS:
                continue

            label = match_code(raw_code, codes)
            if label:
                _last_triggered[norm] = now
                dispatch_action(label)
            else:
                log(f"[NEW] Unrecognized code: {raw_code}")


def run_add_codes():
    """Learning mode: add new codes to config"""
    codes = load_ir_codes()
    log("[IR] Starting in ADD-CODES mode... Press buttons to learn.")

    while True:
        for raw_code in listen_for_ir():
            norm = normalize_code(raw_code)

            # Check if code already exists for any label
            already_known = False
            for variants in codes.values():
                if any(normalize_code(v) == norm for v in variants):
                    already_known = True
                    break
            if already_known:
                log(f"[SKIP] Code already known: {raw_code}")
                continue

            log(f"[NEW] Unrecognized code: {raw_code}")
            label = input("Enter label for this IR code (blank to skip): ").strip().upper()
            if not label:
                log("[SKIP] No label entered.")
                continue

            # Add the new code under the label
            if label not in codes:
                codes[label] = []
            codes[label].append(raw_code)
            save_ir_codes(codes)
            log(f"[SAVED] Code '{raw_code}' saved under '{label}'")


def main():
    parser = argparse.ArgumentParser(description="OrangePi IR Controller")
    parser.add_argument("--start", action="store_true", help="Run in normal mode")
    parser.add_argument("--add-codes", action="store_true", help="Learn new IR codes")

    args = parser.parse_args()

    if args.add_codes:
        run_add_codes()
    elif args.start:
        run_start()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
