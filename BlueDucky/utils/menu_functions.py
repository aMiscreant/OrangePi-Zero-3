import logging
import logging as log
import os
import re
import subprocess
import time
import bluetooth

#############################
# UI Redesign by aMiscreant #
#############################

log = logging.getLogger(__name__)

def get_target_address():
    blue = "\033[94m"
    reset = "\033[0m"
    print(f"\nWhat is the target address{blue}? {reset}Leave blank and we will scan for you{blue}!{reset}")
    target_address = input(f"\n {blue}> {reset}").strip()

    if target_address == "":
        devices = scan_for_devices()
        if devices:
            if len(devices) == 1 and isinstance(devices[0], tuple) and len(devices[0]) == 2:
                confirm = input(f"\nWould you like to register this device{blue}:\n{reset}{devices[0][1]} {devices[0][0]}{blue}? {blue}({reset}y{blue}/{reset}n{blue}) {reset}").strip().lower()
                if confirm in ('y', 'yes'):
                    return devices[0][0]
                else:
                    return None
            else:
                for idx, (addr, name) in enumerate(devices):
                    print(f"{reset}[{blue}{idx + 1}{reset}] {blue}Device Name{reset}: {blue}{name}, {blue}Address{reset}: {blue}{addr}")
                try:
                    selection = int(input(f"\n{reset}Select a device by number{blue}: {reset}")) - 1
                    if 0 <= selection < len(devices):
                        return devices[selection][0]
                    else:
                        print(f"{reset}Invalid selection. Exiting.")
                        return None
                except ValueError:
                    print(f"{reset}Invalid input. Must be a number.")
                    return None
        else:
            return None
    elif not is_valid_mac_address(target_address):
        print("\nInvalid MAC address format. Please enter a valid MAC address.")
        return None

    return target_address

def restart_bluetooth_daemon():
    run(["sudo", "service", "bluetooth", "restart"])
    time.sleep(0.5)

def run(command):
    assert isinstance(command, list)
    log.info("executing '%s'" % " ".join(command))
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def print_fancy_ascii_art():
    ascii_art = """ 
     	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣀⠤⠄⠒⠒⠒⠒⠒⠒⠂⠠⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠁⠀⠀⠀⠀⣀⡤⠴⠒⠒⠒⠒⠦⠤⣀⠀⠀⠀⠙⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠀⢰⠋⠀⠀⠀⣠⠖⠋⢀⣄⣀⡀⠀⠀⠀⠀⠀⠀⠉⠲⣄⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⢀⡼⠁⠀⣴⣿⡛⠻⣿⣧⡀⠀⠀⠀⠀⠀⠀⠈⠳⡄⡿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⣼⣀⣀⣀⡜⠀⠀⠀⣿⣿⣿⣿⣿⣿⡧⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⣀⡤⠟⠁⠀⠈⠙⡶⣄⡀⠈⠻⢿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⣤⣤⠖⠖⠛⠉⠈⣀⣀⠀⠴⠊⠀⠀⣹⣷⣶⡏⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⣀⡀⠀⠀
	⠘⠿⣿⣷⣶⣶⣶⣶⣤⣶⣶⣶⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⠤⠖⠒⠋⠉⠁⠙⣆⠀
	⠀⠀⠀⠀⠉⠉⠉⠉⠙⠿⣍⣩⠟⠋⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣖⣶⣶⢾⠯⠽⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡄
	⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠚⠁⠀⠀⠀⠀⠈⠓⠤⠀⠀⠀⠀⠀⠀⠐⠒⠚⠉⠉⠁⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⣀⢀⠀⠀⠀⠀⠀⠀⠀⣇
	⠀⠀⠀⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠤⠤⠖⠒⠚⠉⠉⠁⠀⠀⠀⢸⢸⣦⠀⠀⠀⠀⠀⠀⢸
	⠀⠀⠀⠀⠀⢠⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡠⠤⠴⠒⠒⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⣸⡏⠇⠀⠀⠀⠀⠀⢸
	⠀⠀⠀⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠞⢠⡿⠀⠀⠀⠀⠀⠀⠀⢸
	⠀⠀⠀⠀⣾⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⣠⡟⠀⠀⠀⠀⠀⠀⠀⠀⡏
	⠀⠀⠀⠀⡏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠖⠉⢀⣴⠏⠠⠀⠀⠀⠀⠀⠀⠀⣸⠁
	⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠒⠢⠤⠄⠀⠀⠀⠀⠀⠈⠁⠀⣠⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀
	⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠃⠀⠀
	⠀⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡶⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠳⣄⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠖⣪⡵⠋⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠫⠭⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣭⣭⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡴⠶⠛⠉⠀⠀⠀⠀⠀⠀"""
    print("\033[94m" + ascii_art + "\033[0m")

def clear_screen():
    os.system('clear')

def save_devices_to_file(devices, filename='known_devices.txt'):
    with open(filename, 'w') as file:
        for addr, name in devices:
            file.write(f"{addr},{name}\n")

def load_known_devices(filename='known_devices.txt'):
    devices = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                if ',' in line:
                    addr, name = line.strip().split(',', 1)
                    devices.append((addr.strip(), name.strip()))
    return devices

def is_valid_mac_address(addr):
    return bool(re.match(r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$', addr))

def scan_for_devices():
    clear_screen()
    print_fancy_ascii_art()

    blue = "\033[94m"
    reset = "\033[0m"

    known_devices = load_known_devices()
    if known_devices:
        print(f"\n{reset}Known devices{blue}:")
        for idx, (addr, name) in enumerate(known_devices):
            print(f"{blue}{idx + 1}{reset}: Device Name: {blue}{name}, Address: {blue}{addr}")

        use_known = input(f"\n{reset}Do you want to use one of these known devices{blue}? {blue}({reset}yes{blue}/{reset}no{blue}){reset}: ").strip().lower()
        if use_known in ('yes', 'y'):
            return known_devices

    print(f"\n{reset}Scanning for Bluetooth devices...{blue}")
    time.sleep(1)
    nearby_devices = bluetooth.discover_devices(duration=12, lookup_names=True)
    print(f"\n{reset}Found {len(nearby_devices)} device(s):")

    for idx, (addr, name) in enumerate(nearby_devices):
        print(f"{blue}{idx + 1}{reset}: Device Name: {blue}{name}, Address: {blue}{addr}")

    save_devices_to_file(nearby_devices)
    return nearby_devices

# Terminal UI colors
BLUE = '\033[94m'
RESET = '\033[0m'

def get_terminal_width():
    """Get the current terminal width."""
    try:
        size = os.get_terminal_size()
        return size.columns
    except OSError:
        return 80  # Fallback width for non-interactive environments

def print_menu():
    """Print the main banner/menu with color and centered formatting."""
    title = "BlueDucky - Bluetooth Device Attacker"
    version = "Ver 2.1"
    motd1 = "Remember, you can still attack devices without visibility.."
    motd2 = "If you have their MAC address.."

    width = get_terminal_width()
    separator = "=" * width

    print(BLUE + separator)
    print(RESET + title.center(width))
    print(BLUE + version.center(width))
    print(BLUE + separator)
    print(RESET + motd1.center(width))
    print(motd2.center(width))
    print(BLUE + separator + RESET)

def main_menu():
    """Clear screen, display ASCII art and main menu."""
    clear_screen()
    print_fancy_ascii_art()
    print_menu()

def read_duckyscript(filename):
    """Read DuckyScript from a file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    else:
        log.warning(f"File {filename} not found. Skipping DuckyScript.")
        return None